#!/usr/bin/env python3
"""
Import Scanner - Detects potentially broken imports in a codebase

This script scans Python files in a codebase and reports imports that may be broken
by checking if the imported modules actually exist in the expected locations.
"""

import os
import ast
import sys
import importlib
import argparse
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import sysconfig
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


@dataclass
class ImportIssue:
    """Represents an import issue found in the codebase."""
    file_path: str
    line_number: int
    import_statement: str
    issue_type: str
    description: str
    suggested_fix: Optional[str] = None


class ImportScanner:
    """Scans a codebase for potentially broken imports."""
    
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues: List[ImportIssue] = []
        self.python_files: Set[str] = set()
        self.module_cache: Dict[str, bool] = {}
        self.project_modules: Set[str] = set()
        
    def scan_codebase(self) -> List[ImportIssue]:
        """Scan the entire codebase for import issues."""
        print(f"Scanning codebase at: {self.root_path}")
        
        # Find all Python files
        self._find_python_files()
        print(f"Found {len(self.python_files)} Python files")
        
        # Index all project modules for fast lookup
        self._index_project_modules()
        
        # Scan each file for import issues
        if TQDM_AVAILABLE:
            for file_path in tqdm(self.python_files, desc="Scanning files", unit="file"):
                self._scan_file(file_path)
        else:
            for file_path in self.python_files:
                self._scan_file(file_path)
            
        return self.issues

    def _index_project_modules(self):
        """Index all project modules for fast lookup."""
        if TQDM_AVAILABLE:
            for file_path in tqdm(self.python_files, desc="Indexing modules", unit="file"):
                self._add_module_to_index(file_path)
        else:
            for file_path in self.python_files:
                self._add_module_to_index(file_path)
    
    def _add_module_to_index(self, file_path: str):
        """Add a single file to the module index."""
        rel_path = os.path.relpath(file_path, self.root_path)
        parts = Path(rel_path).with_suffix('').parts
        # Add as dotted module path
        if parts[-1] == '__init__':
            module = '.'.join(parts[:-1])
        else:
            module = '.'.join(parts)
        if module:
            self.project_modules.add(module)
    
    def _find_python_files(self):
        """Find all Python files in the codebase."""
        for root, dirs, files in os.walk(self.root_path):
            # Skip common directories that shouldn't be scanned
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'env', 'node_modules', 'chat_env', 'OLD']]
            
            for file in files:
                if file.endswith('.py'):
                    self.python_files.add(os.path.join(root, file))
    
    def _scan_file(self, file_path: str):
        """Scan a single Python file for import issues."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            tree = ast.parse(content)
            visitor = ImportVisitor(file_path, self.root_path, self.project_modules)
            visitor.visit(tree)
            
            # Add issues found in this file
            self.issues.extend(visitor.issues)
            
        except SyntaxError as e:
            self.issues.append(ImportIssue(
                file_path=file_path,
                line_number=e.lineno or 0,
                import_statement="",
                issue_type="syntax_error",
                description=f"Syntax error: {e.msg}",
                suggested_fix="Fix the syntax error in the file"
            ))
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
    
    def generate_report(self) -> str:
        """Generate a comprehensive report of all import issues."""
        if not self.issues:
            return "✅ No import issues found!"
        
        # Group issues by type
        issues_by_type = defaultdict(list)
        for issue in self.issues:
            issues_by_type[issue.issue_type].append(issue)
        
        report = []
        report.append("🔍 IMPORT SCANNER REPORT")
        report.append("=" * 50)
        report.append(f"Total issues found: {len(self.issues)}")
        report.append("")
        
        # Summary by type
        report.append("📊 SUMMARY BY ISSUE TYPE:")
        for issue_type, issues in issues_by_type.items():
            report.append(f"  {issue_type}: {len(issues)} issues")
        report.append("")
        
        # Detailed report by type
        for issue_type, issues in issues_by_type.items():
            report.append(f"📋 {issue_type.upper()} ISSUES:")
            report.append("-" * 30)
            
            for issue in issues:
                report.append(f"File: {issue.file_path}")
                report.append(f"Line: {issue.line_number}")
                report.append(f"Import: {issue.import_statement}")
                report.append(f"Description: {issue.description}")
                if issue.suggested_fix:
                    report.append(f"Suggested fix: {issue.suggested_fix}")
                report.append("")
        
        # Add final count at the end
        report.append("=" * 50)
        report.append(f"📈 FINAL COUNT: {len(self.issues)} total import issues found")
        
        return "\n".join(report)


class ImportVisitor(ast.NodeVisitor):
    """AST visitor that analyzes import statements."""
    
    def __init__(self, file_path: str, root_path: Path, project_modules: Set[str]):
        self.file_path = file_path
        self.root_path = root_path
        self.issues: List[ImportIssue] = []
        self.current_line = 0
        self.project_modules = project_modules
        self.stdlib_modules = self._get_stdlib_modules()
    
    def _get_stdlib_modules(self) -> Set[str]:
        """Get a set of standard library module names."""
        stdlib = set()
        stdlib_path = sysconfig.get_paths()["stdlib"]
        for root, dirs, files in os.walk(stdlib_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    mod = file[:-3]
                    stdlib.add(mod)
            for dir in dirs:
                stdlib.add(dir)
        # Add some built-ins
        stdlib.update(sys.builtin_module_names)
        return stdlib
    
    def visit(self, node):
        self.current_line = getattr(node, 'lineno', self.current_line)
        return super().visit(node)
    
    def visit_Import(self, node):
        """Handle 'import x' statements."""
        for alias in node.names:
            module_name = alias.name
            self._check_import(module_name, alias.asname, node.lineno)
    
    def visit_ImportFrom(self, node):
        """Handle 'from x import y' statements."""
        if node.module:
            module_name = node.module
            self._check_import(module_name, None, node.lineno)
    
    def _check_import(self, module_name: str, alias: Optional[str], line_number: int):
        """Check if an import is potentially broken."""
        import_statement = f"import {module_name}"
        if alias:
            import_statement += f" as {alias}"
        
        # Skip standard library modules
        if self._is_standard_library(module_name):
            return
        
        # Check if it's a relative import
        if module_name.startswith('.'):
            self._check_relative_import(module_name, line_number, import_statement)
            return
        
        # Check if it's an absolute import within the project
        if self._is_project_import(module_name):
            # If it's a project import and not found, flag it
            if module_name not in self.project_modules:
                self.issues.append(ImportIssue(
                    file_path=self.file_path,
                    line_number=line_number,
                    import_statement=import_statement,
                    issue_type="missing_project_module",
                    description=f"Project module '{module_name}' not found",
                    suggested_fix=f"Check if the module exists at the expected location"
                ))
            return
        
        # Check if it's an external package
        if not self._is_installed_package(module_name):
            self.issues.append(ImportIssue(
                file_path=self.file_path,
                line_number=line_number,
                import_statement=import_statement,
                issue_type="missing_external_package",
                description=f"External package '{module_name}' may not be installed",
                suggested_fix=f"Install the package: pip install {module_name}"
            ))
    
    def _is_standard_library(self, module_name: str) -> bool:
        """Check if a module is part of Python's standard library."""
        root_mod = module_name.split('.')[0]
        return root_mod in self.stdlib_modules
    
    def _is_project_import(self, module_name: str) -> bool:
        """Check if an import is likely a project module."""
        return module_name in self.project_modules
    
    def _check_project_import(self, module_name: str, line_number: int, import_statement: str):
        """Check if a project import is valid."""
        module_parts = module_name.split('.')
        
        # Try to find the module file
        found = False
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                if file.endswith('.py') and file[:-3] == module_parts[-1]:
                    rel_path = os.path.relpath(root, self.root_path)
                    if rel_path == '.':
                        rel_path = ''
                    
                    path_parts = rel_path.split(os.sep) if rel_path else []
                    if path_parts == module_parts[:-1]:
                        found = True
                        break
            if found:
                break
        
        if not found:
            self.issues.append(ImportIssue(
                file_path=self.file_path,
                line_number=line_number,
                import_statement=import_statement,
                issue_type="missing_project_module",
                description=f"Project module '{module_name}' not found",
                suggested_fix=f"Check if the module exists at the expected location"
            ))
    
    def _check_relative_import(self, module_name: str, line_number: int, import_statement: str):
        """Check if a relative import is valid."""
        # Get the directory of the current file
        current_dir = os.path.dirname(self.file_path)
        rel_path = os.path.relpath(current_dir, self.root_path)
        
        # Calculate the expected module path
        dots = len([c for c in module_name if c == '.'])
        module_name_clean = module_name.lstrip('.')
        
        if module_name_clean:
            # This is a relative import with a module name
            # For now, just flag it as potentially problematic
            self.issues.append(ImportIssue(
                file_path=self.file_path,
                line_number=line_number,
                import_statement=import_statement,
                issue_type="relative_import",
                description=f"Relative import '{module_name}' - verify path is correct",
                suggested_fix="Check if the relative path is correct"
            ))
    
    def _is_installed_package(self, module_name: str) -> bool:
        """Check if a package is installed."""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False


def main():
    """Main function to run the import scanner."""
    parser = argparse.ArgumentParser(description="Scan a codebase for broken imports")
    parser.add_argument("path", nargs="?", default=".", help="Path to the codebase to scan")
    parser.add_argument("--output", "-o", help="Output file for the report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Validate the path
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    # Create scanner and run
    scanner = ImportScanner(args.path)
    issues = scanner.scan_codebase()
    
    # Generate and display report
    report = scanner.generate_report()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)
    
    # Exit with error code if issues found
    if issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main() 