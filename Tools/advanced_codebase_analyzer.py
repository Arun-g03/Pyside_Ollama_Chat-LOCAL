#!/usr/bin/env python3
"""
Advanced Codebase Relationship Analyzer
Enhanced version that analyzes relationships between functions and classes with detailed dependency tracking.
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict
import json
from datetime import datetime
import networkx as nx


class AdvancedCodebaseAnalyzer:
    def __init__(self, root_path: str = "pyside_chat"):
        self.root_path = Path(root_path)
        self.classes = {}
        self.functions = {}
        self.imports = {}
        self.relationships = defaultdict(set)
        self.file_structure = {}
        self.dependency_graph = nx.DiGraph()
        self.function_calls = defaultdict(set)
        self.class_instantiations = defaultdict(set)
        self.method_calls = defaultdict(set)
        
    def analyze_codebase(self):
        """Main analysis method that walks through the codebase."""
        print("🔍 Starting advanced codebase analysis...")
        
        # Walk through all Python files
        for file_path in self.root_path.rglob("*.py"):
            if "__pycache__" in str(file_path):
                continue
                
            relative_path = file_path.relative_to(self.root_path)
            print(f"📄 Analyzing: {relative_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse the AST
                tree = ast.parse(content)
                
                # Analyze this file
                file_classes, file_functions, file_imports = self._analyze_file(tree, str(relative_path))
                
                # Analyze function calls and dependencies
                self._analyze_dependencies(tree, str(relative_path))
                
                # Store results
                self.file_structure[str(relative_path)] = {
                    'classes': file_classes,
                    'functions': file_functions,
                    'imports': file_imports
                }
                
            except Exception as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")
        
        # Build relationships
        self._build_relationships()
        
        # Build dependency graph
        self._build_dependency_graph()
        
        print(f"✅ Analysis complete! Found {len(self.classes)} classes and {len(self.functions)} functions")
    
    def _analyze_file(self, tree: ast.AST, file_path: str) -> Tuple[Dict, Dict, Dict]:
        """Analyze a single Python file."""
        classes = {}
        functions = {}
        imports = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, file_path)
                classes[node.name] = class_info
                self.classes[f"{file_path}.{node.name}"] = class_info
                
            elif isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node, file_path)
                functions[node.name] = func_info
                self.functions[f"{file_path}.{node.name}"] = func_info
                
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports[alias.name] = {
                        'asname': alias.asname,
                        'lineno': node.lineno
                    }
                    
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports[f"{module}.{alias.name}"] = {
                        'asname': alias.asname,
                        'lineno': node.lineno
                    }
        
        return classes, functions, imports
    
    def _analyze_dependencies(self, tree: ast.AST, file_path: str):
        """Analyze function calls and dependencies within a file."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                self._analyze_call_node(node, file_path)
            elif isinstance(node, ast.ClassDef):
                self._analyze_class_dependencies(node, file_path)
    
    def _analyze_call_node(self, node: ast.Call, file_path: str):
        """Analyze a function call node."""
        if isinstance(node.func, ast.Name):
            # Direct function call
            func_name = node.func.id
            self.function_calls[file_path].add(func_name)
            
        elif isinstance(node.func, ast.Attribute):
            # Method call or attribute access
            full_name = self._get_full_name(node.func)
            if '.' in full_name:
                # This is likely a method call
                self.method_calls[file_path].add(full_name)
            else:
                self.function_calls[file_path].add(full_name)
    
    def _analyze_class_dependencies(self, node: ast.ClassDef, file_path: str):
        """Analyze class dependencies and instantiations."""
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                # Analyze method calls within the class
                for call_node in ast.walk(item):
                    if isinstance(call_node, ast.Call):
                        self._analyze_call_node(call_node, file_path)
    
    def _extract_class_info(self, node: ast.ClassDef, file_path: str) -> Dict:
        """Extract information about a class."""
        methods = []
        bases = []
        
        # Get base classes
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(self._get_full_name(base))
        
        # Get methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append({
                    'name': item.name,
                    'lineno': item.lineno,
                    'args': [arg.arg for arg in item.args.args],
                    'decorators': [self._get_decorator_name(d) for d in item.decorator_list]
                })
        
        return {
            'file': file_path,
            'lineno': node.lineno,
            'bases': bases,
            'methods': methods,
            'docstring': ast.get_docstring(node),
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
        }
    
    def _extract_function_info(self, node: ast.FunctionDef, file_path: str) -> Dict:
        """Extract information about a function."""
        return {
            'file': file_path,
            'lineno': node.lineno,
            'args': [arg.arg for arg in node.args.args],
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
            'docstring': ast.get_docstring(node),
            'returns': self._get_return_type(node)
        }
    
    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return self._get_full_name(decorator)
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return self._get_full_name(decorator.func)
        return str(decorator)
    
    def _get_full_name(self, node: ast.Attribute) -> str:
        """Get the full name of an attribute (e.g., 'module.submodule.name')."""
        parts = []
        current = node
        
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
            
        if isinstance(current, ast.Name):
            parts.append(current.id)
        
        return '.'.join(reversed(parts))
    
    def _get_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Extract return type annotation."""
        if node.returns:
            if isinstance(node.returns, ast.Name):
                return node.returns.id
            elif isinstance(node.returns, ast.Attribute):
                return self._get_full_name(node.returns)
        return None
    
    def _build_relationships(self):
        """Build relationships between classes and functions."""
        print("🔗 Building relationships...")
        
        # Find inheritance relationships
        for file_path, file_info in self.file_structure.items():
            for class_name, class_info in file_info['classes'].items():
                for base in class_info['bases']:
                    # Find the base class in our analyzed classes
                    for other_file, other_info in self.file_structure.items():
                        if base in other_info['classes']:
                            self.relationships[f"{file_path}.{class_name}"].add(
                                f"inherits_from:{other_file}.{base}"
                            )
        
        # Find function dependencies
        for file_path, calls in self.function_calls.items():
            for func_name in calls:
                # Find where this function is defined
                for other_file, other_info in self.file_structure.items():
                    if func_name in other_info['functions']:
                        self.relationships[f"{file_path}"].add(
                            f"calls_function:{other_file}.{func_name}"
                        )
        
        # Find method dependencies
        for file_path, method_calls in self.method_calls.items():
            for method_name in method_calls:
                # Parse method calls like "class.method" or "module.class.method"
                parts = method_name.split('.')
                if len(parts) >= 2:
                    class_name = parts[-2] if len(parts) > 2 else parts[0]
                    method_name_short = parts[-1]
                    
                    # Find the class and method
                    for other_file, other_info in self.file_structure.items():
                        if class_name in other_info['classes']:
                            class_info = other_info['classes'][class_name]
                            for method in class_info['methods']:
                                if method['name'] == method_name_short:
                                    self.relationships[f"{file_path}"].add(
                                        f"calls_method:{other_file}.{class_name}.{method_name_short}"
                                    )
    
    def _build_dependency_graph(self):
        """Build a networkx dependency graph."""
        print("📊 Building dependency graph...")
        
        # Add nodes for all files
        for file_path in self.file_structure.keys():
            self.dependency_graph.add_node(file_path)
        
        # Add edges based on relationships
        for source, relationships in self.relationships.items():
            for rel in relationships:
                if rel.startswith('calls_function:'):
                    target = rel.split(':', 1)[1]
                    target_file = target.split('.')[0]
                    self.dependency_graph.add_edge(source, target_file)
                elif rel.startswith('calls_method:'):
                    target = rel.split(':', 1)[1]
                    target_file = target.split('.')[0]
                    self.dependency_graph.add_edge(source, target_file)
                elif rel.startswith('inherits_from:'):
                    target = rel.split(':', 1)[1]
                    target_file = target.split('.')[0]
                    self.dependency_graph.add_edge(source, target_file)
    
    def generate_markdown_report(self, output_file: str = "Reports/advanced_codebase_analysis.md"):
        """Generate a comprehensive markdown report."""
        print(f"📝 Generating advanced markdown report: {output_file}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self._generate_header())
            f.write(self._generate_summary())
            f.write(self._generate_dependency_analysis())
            f.write(self._generate_file_structure())
            f.write(self._generate_classes_section())
            f.write(self._generate_functions_section())
            f.write(self._generate_relationships_section())
            f.write(self._generate_imports_section())
            f.write(self._generate_call_analysis())
            f.write(self._generate_statistics())
        
        print(f"✅ Advanced report generated: {output_file}")
    
    def _generate_header(self) -> str:
        """Generate the header section."""
        return f"""# Advanced Codebase Analysis Report

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Root Path:** {self.root_path}  
**Total Files Analyzed:** {len(self.file_structure)}

---

"""
    
    def _generate_summary(self) -> str:
        """Generate the summary section."""
        total_classes = len(self.classes)
        total_functions = len(self.functions)
        total_files = len(self.file_structure)
        
        # Count by directory
        dir_stats = defaultdict(int)
        for file_path in self.file_structure.keys():
            dir_name = str(Path(file_path).parent)
            dir_stats[dir_name] += 1
        
        summary = f"""## 📊 Summary

- **Total Classes:** {total_classes}
- **Total Functions:** {total_functions}
- **Total Files:** {total_files}

### Files by Directory

"""
        
        for dir_name, count in sorted(dir_stats.items()):
            if dir_name == ".":
                dir_name = "Root"
            summary += f"- `{dir_name}/`: {count} files\n"
        
        return summary + "\n---\n\n"
    
    def _generate_dependency_analysis(self) -> str:
        """Generate dependency analysis section."""
        content = "## 🔗 Dependency Analysis\n\n"
        
        # Find files with most dependencies
        in_degree = dict(self.dependency_graph.in_degree())
        out_degree = dict(self.dependency_graph.out_degree())
        
        content += "### Most Dependent Files (High In-Degree)\n\n"
        sorted_in = sorted(in_degree.items(), key=lambda x: x[1], reverse=True)[:10]
        for file_path, degree in sorted_in:
            content += f"- `{file_path}`: {degree} dependencies\n"
        
        content += "\n### Most Influential Files (High Out-Degree)\n\n"
        sorted_out = sorted(out_degree.items(), key=lambda x: x[1], reverse=True)[:10]
        for file_path, degree in sorted_out:
            content += f"- `{file_path}`: {degree} dependents\n"
        
        # Find circular dependencies
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            if cycles:
                content += "\n### ⚠️ Circular Dependencies\n\n"
                for cycle in cycles[:5]:  # Limit to first 5 cycles
                    content += f"- {' → '.join(cycle)} → {cycle[0]}\n"
            else:
                content += "\n### ✅ No Circular Dependencies Found\n\n"
        except Exception as e:
            content += f"\n### ⚠️ Error analyzing cycles: {e}\n\n"
        
        return content + "\n---\n\n"
    
    def _generate_file_structure(self) -> str:
        """Generate the file structure section."""
        content = "## 📁 File Structure\n\n"
        
        for file_path, file_info in sorted(self.file_structure.items()):
            content += f"### `{file_path}`\n\n"
            
            if file_info['classes']:
                content += "**Classes:**\n"
                for class_name, class_info in file_info['classes'].items():
                    content += f"- `{class_name}` (line {class_info['lineno']})\n"
                content += "\n"
            
            if file_info['functions']:
                content += "**Functions:**\n"
                for func_name, func_info in file_info['functions'].items():
                    content += f"- `{func_name}` (line {func_info['lineno']})\n"
                content += "\n"
            
            content += "---\n\n"
        
        return content
    
    def _generate_classes_section(self) -> str:
        """Generate the classes section."""
        content = "## 🏗️ Classes\n\n"
        
        for class_path, class_info in sorted(self.classes.items()):
            content += f"### `{class_path}`\n\n"
            content += f"- **File:** `{class_info['file']}`\n"
            content += f"- **Line:** {class_info['lineno']}\n"
            
            if class_info['bases']:
                content += f"- **Bases:** {', '.join(class_info['bases'])}\n"
            
            if class_info['decorators']:
                content += f"- **Decorators:** {', '.join(class_info['decorators'])}\n"
            
            if class_info['docstring']:
                content += f"- **Docstring:** {class_info['docstring'][:100]}...\n"
            
            if class_info['methods']:
                content += "\n**Methods:**\n"
                for method in class_info['methods']:
                    content += f"- `{method['name']}` (line {method['lineno']})\n"
            
            content += "\n---\n\n"
        
        return content
    
    def _generate_functions_section(self) -> str:
        """Generate the functions section."""
        content = "## ⚙️ Functions\n\n"
        
        for func_path, func_info in sorted(self.functions.items()):
            content += f"### `{func_path}`\n\n"
            content += f"- **File:** `{func_info['file']}`\n"
            content += f"- **Line:** {func_info['lineno']}\n"
            content += f"- **Arguments:** {', '.join(func_info['args'])}\n"
            
            if func_info['returns']:
                content += f"- **Returns:** {func_info['returns']}\n"
            
            if func_info['decorators']:
                content += f"- **Decorators:** {', '.join(func_info['decorators'])}\n"
            
            if func_info['docstring']:
                content += f"- **Docstring:** {func_info['docstring'][:100]}...\n"
            
            content += "\n---\n\n"
        
        return content
    
    def _generate_relationships_section(self) -> str:
        """Generate the relationships section."""
        content = "## 🔗 Relationships\n\n"
        
        if not self.relationships:
            content += "No relationships found.\n\n"
            return content
        
        for item, relationships in sorted(self.relationships.items()):
            content += f"### `{item}`\n\n"
            for rel in relationships:
                content += f"- {rel}\n"
            content += "\n"
        
        return content
    
    def _generate_call_analysis(self) -> str:
        """Generate function call analysis section."""
        content = "## 📞 Function Call Analysis\n\n"
        
        for file_path, calls in sorted(self.function_calls.items()):
            if calls:
                content += f"### `{file_path}`\n\n"
                content += "**Function Calls:**\n"
                for call in sorted(calls):
                    content += f"- `{call}`\n"
                content += "\n"
        
        content += "\n### Method Calls\n\n"
        for file_path, method_calls in sorted(self.method_calls.items()):
            if method_calls:
                content += f"**`{file_path}`:**\n"
                for method_call in sorted(method_calls):
                    content += f"- `{method_call}`\n"
                content += "\n"
        
        return content + "\n---\n\n"
    
    def _generate_imports_section(self) -> str:
        """Generate the imports section."""
        content = "## 📦 Imports\n\n"
        
        all_imports = defaultdict(set)
        for file_path, file_info in self.file_structure.items():
            for import_name, import_info in file_info['imports'].items():
                all_imports[file_path].add(import_name)
        
        for file_path, imports in sorted(all_imports.items()):
            content += f"### `{file_path}`\n\n"
            for import_name in sorted(imports):
                content += f"- `{import_name}`\n"
            content += "\n"
        
        return content
    
    def _generate_statistics(self) -> str:
        """Generate statistics section."""
        content = "## 📈 Statistics\n\n"
        
        # Class statistics
        class_by_dir = defaultdict(int)
        for class_path in self.classes.keys():
            file_path = class_path.split('.')[0]
            dir_name = str(Path(file_path).parent)
            class_by_dir[dir_name] += 1
        
        content += "### Classes by Directory\n\n"
        for dir_name, count in sorted(class_by_dir.items()):
            if dir_name == ".":
                dir_name = "Root"
            content += f"- `{dir_name}/`: {count} classes\n"
        
        content += "\n### Functions by Directory\n\n"
        func_by_dir = defaultdict(int)
        for func_path in self.functions.keys():
            file_path = func_path.split('.')[0]
            dir_name = str(Path(file_path).parent)
            func_by_dir[dir_name] += 1
        
        for dir_name, count in sorted(func_by_dir.items()):
            if dir_name == ".":
                dir_name = "Root"
            content += f"- `{dir_name}/`: {count} functions\n"
        
        # Call statistics
        total_calls = sum(len(calls) for calls in self.function_calls.values())
        total_method_calls = sum(len(calls) for calls in self.method_calls.values())
        
        content += f"\n### Call Statistics\n\n"
        content += f"- **Total Function Calls:** {total_calls}\n"
        content += f"- **Total Method Calls:** {total_method_calls}\n"
        content += f"- **Files with Function Calls:** {len(self.function_calls)}\n"
        content += f"- **Files with Method Calls:** {len(self.method_calls)}\n"
        
        return content
    
    def export_dependency_graph(self, output_file: str = "dependency_graph.json"):
        """Export the dependency graph as JSON."""
        graph_data = {
            'nodes': list(self.dependency_graph.nodes()),
            'edges': list(self.dependency_graph.edges()),
            'in_degree': dict(self.dependency_graph.in_degree()),
            'out_degree': dict(self.dependency_graph.out_degree())
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"📊 Dependency graph exported: {output_file}")


def main():
    """Main function to run the analysis."""
    print("🚀 Starting Advanced Codebase Relationship Analyzer")
    print("=" * 60)
    
    # Create analyzer
    analyzer = AdvancedCodebaseAnalyzer()
    
    # Run analysis
    analyzer.analyze_codebase()
    
    # Generate report
    analyzer.generate_markdown_report()
    
    # Export dependency graph
    analyzer.export_dependency_graph()
    
    print("\n🎉 Advanced analysis complete!")
    print("📄 Check 'advanced_codebase_analysis.md' for the detailed report")
    print("📊 Check 'dependency_graph.json' for the dependency graph data")


if __name__ == "__main__":
    main() 