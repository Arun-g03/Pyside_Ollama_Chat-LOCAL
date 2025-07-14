#!/usr/bin/env python3
"""
Refactoring Analyzer Utility
Scans the codebase and provides recommendations for refactoring and modularization.
Ignores chat_env directory as requested.
"""

import os
import ast
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    path: str
    size_bytes: int
    size_kb: float
    line_count: int
    class_count: int
    function_count: int
    import_count: int
    complexity_score: float
    has_main_function: bool
    has_gui_code: bool
    has_business_logic: bool
    has_data_access: bool
    duplicate_functions: List[str]
    duplicate_classes: List[str]
    issues: List[str]
    recommendations: List[str]

@dataclass
class DirectoryAnalysis:
    """Analysis results for a directory"""
    path: str
    file_count: int
    total_lines: int
    total_size_kb: float
    largest_files: List[Tuple[str, float]]
    most_complex_files: List[Tuple[str, float]]
    issues: List[str]
    recommendations: List[str]

@dataclass
class RefactoringReport:
    """Complete refactoring analysis report"""
    timestamp: str
    total_files: int
    total_lines: int
    total_size_kb: float
    files_needing_refactoring: List[FileAnalysis]
    directories_needing_refactoring: List[DirectoryAnalysis]
    high_priority_files: List[str]
    medium_priority_files: List[str]
    low_priority_files: List[str]
    duplicate_functions: List[Tuple[str, List[str]]]
    duplicate_classes: List[Tuple[str, List[str]]]
    architectural_issues: List[str]
    general_recommendations: List[str]

class CodeAnalyzer:
    """Analyzes Python code for complexity and structure"""
    
    def __init__(self):
        self.ignore_dirs = {'chat_env', '__pycache__', '.git', '.vscode', 'node_modules', 'OLD', 'Tools'}
        self.ignore_files = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.md'}
        self.ignore_specific_files = {
            'voice_ring_animation.py',  # Specific filename to ignore
            'pyside_chat/ui/Audio_visualisers/voice_ring_animation.py',  # Full path
            'OLD/chat_tab_backup.py',  # Files in OLD directory
            'OLD/ollama_chat_old.py',
            
        }
        self.ignore_file_patterns = [
            r'.*\.md$',  # All markdown files
            r'.*_backup\.py$',  # All backup files
            r'.*_old\.py$',  # All old files
        ]
        self.duplicate_detector = DuplicateDetector()
        
    def analyze_file(self, file_path: str) -> FileAnalysis:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic file stats
            size_bytes = os.path.getsize(file_path)
            size_kb = size_bytes / 1024
            line_count = len(content.splitlines())
            
            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content)
                analyzer = ASTAnalyzer()
                ast_analysis = analyzer.analyze_ast(tree)
                
                # Add to duplicate detector
                self.duplicate_detector.add_file_analysis(
                    file_path, 
                    ast_analysis.get('functions', []), 
                    ast_analysis.get('classes', [])
                )
                
                # Determine file type based on content analysis
                has_gui_code = self._detect_gui_code(content)
                has_business_logic = self._detect_business_logic(content)
                has_data_access = self._detect_data_access(content)
                has_main_function = self._detect_main_function(content)
                
                # Calculate complexity score
                complexity_score = self._calculate_complexity_score(
                    line_count, ast_analysis['function_count'], 
                    ast_analysis['class_count'], ast_analysis['nesting_depth']
                )
                
                # Get duplicate information for this file
                duplicate_functions, duplicate_classes = self.duplicate_detector.get_file_duplicates(file_path)
                
                # Identify issues
                issues = self._identify_issues(file_path, content, ast_analysis, size_kb)
                
                # Generate recommendations
                recommendations = self._generate_recommendations(
                    file_path, size_kb, line_count, ast_analysis, 
                    has_gui_code, has_business_logic, has_data_access
                )
                
                return FileAnalysis(
                    path=file_path,
                    size_bytes=size_bytes,
                    size_kb=size_kb,
                    line_count=line_count,
                    class_count=ast_analysis['class_count'],
                    function_count=ast_analysis['function_count'],
                    import_count=ast_analysis['import_count'],
                    complexity_score=complexity_score,
                    has_main_function=has_main_function,
                    has_gui_code=has_gui_code,
                    has_business_logic=has_business_logic,
                    has_data_access=has_data_access,
                    duplicate_functions=duplicate_functions,
                    duplicate_classes=duplicate_classes,
                    issues=issues,
                    recommendations=recommendations
                )
                
            except SyntaxError as e:
                logger.warning(f"Syntax error in {file_path}: {e}")
                return FileAnalysis(
                    path=file_path,
                    size_bytes=size_bytes,
                    size_kb=size_kb,
                    line_count=line_count,
                    class_count=0,
                    function_count=0,
                    import_count=0,
                    complexity_score=0,
                    has_main_function=False,
                    has_gui_code=False,
                    has_business_logic=False,
                    has_data_access=False,
                    duplicate_functions=[],
                    duplicate_classes=[],
                    issues=[f"Syntax error: {e}"],
                    recommendations=["Fix syntax errors before refactoring"]
                )
                
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            return FileAnalysis(
                path=file_path,
                size_bytes=0,
                size_kb=0,
                line_count=0,
                class_count=0,
                function_count=0,
                import_count=0,
                complexity_score=0,
                has_main_function=False,
                has_gui_code=False,
                has_business_logic=False,
                has_data_access=False,
                duplicate_functions=[],
                duplicate_classes=[],
                issues=[f"Error reading file: {e}"],
                recommendations=["Check file permissions and encoding"]
            )
    
    def _detect_gui_code(self, content: str) -> bool:
        """Detect if file contains GUI code"""
        gui_patterns = [
            r'from PySide6\.QtWidgets',
            r'from PySide6\.QtCore',
            r'from PySide6\.QtGui',
            r'QMainWindow',
            r'QWidget',
            r'QDialog',
            r'QPushButton',
            r'QLabel',
            r'QTextEdit',
            r'QVBoxLayout',
            r'QHBoxLayout'
        ]
        return any(re.search(pattern, content) for pattern in gui_patterns)
    
    def _detect_business_logic(self, content: str) -> bool:
        """Detect if file contains business logic"""
        logic_patterns = [
            r'def\s+\w+',
            r'class\s+\w+',
            r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',
            r'import\s+\w+',
            r'from\s+\w+\s+import'
        ]
        return any(re.search(pattern, content) for pattern in logic_patterns)
    
    def _detect_data_access(self, content: str) -> bool:
        """Detect if file contains data access code"""
        data_patterns = [
            r'open\(',
            r'json\.',
            r'pickle\.',
            r'sqlite',
            r'pandas',
            r'pymongo',
            r'psycopg2',
            r'mysql'
        ]
        return any(re.search(pattern, content) for pattern in data_patterns)
    
    def _detect_main_function(self, content: str) -> bool:
        """Detect if file has a main function or entry point"""
        main_patterns = [
            r'if\s+__name__\s*==\s*[\'"]__main__[\'"]',
            r'def\s+main\(',
            r'def\s+__main__\('
        ]
        return any(re.search(pattern, content) for pattern in main_patterns)
    
    def _calculate_complexity_score(self, lines: int, functions: int, classes: int, nesting: int) -> float:
        """Calculate a complexity score for the file"""
        # Base complexity from line count
        base_complexity = min(lines / 100, 1.0)
        
        # Function complexity
        function_complexity = min(functions / 20, 1.0)
        
        # Class complexity
        class_complexity = min(classes / 5, 1.0)
        
        # Nesting complexity
        nesting_complexity = min(nesting / 5, 1.0)
        
        # Weighted average
        complexity = (base_complexity * 0.4 + 
                     function_complexity * 0.3 + 
                     class_complexity * 0.2 + 
                     nesting_complexity * 0.1)
        
        return min(complexity, 1.0)
    
    def _identify_issues(self, file_path: str, content: str, ast_analysis: Dict, size_kb: float) -> List[str]:
        """Identify potential issues in the file"""
        issues = []
        
        # Size issues
        if size_kb > 50:
            issues.append(f"File is very large ({size_kb:.1f}KB) - consider splitting")
        elif size_kb > 20:
            issues.append(f"File is large ({size_kb:.1f}KB) - consider modularization")
        
        # Line count issues
        if ast_analysis['line_count'] > 1000:
            issues.append(f"Very long file ({ast_analysis['line_count']} lines) - needs refactoring")
        elif ast_analysis['line_count'] > 500:
            issues.append(f"Long file ({ast_analysis['line_count']} lines) - consider splitting")
        
        # Function count issues
        if ast_analysis['function_count'] > 20:
            issues.append(f"Too many functions ({ast_analysis['function_count']}) - consider class-based organization")
        
        # Class count issues
        if ast_analysis['class_count'] > 10:
            issues.append(f"Too many classes ({ast_analysis['class_count']}) - consider splitting into modules")
        
        # Nesting issues
        if ast_analysis['nesting_depth'] > 5:
            issues.append(f"Deep nesting ({ast_analysis['nesting_depth']} levels) - consider simplifying logic")
        
        # Import issues
        if ast_analysis['import_count'] > 15:
            issues.append(f"Many imports ({ast_analysis['import_count']}) - consider organizing imports")
        
        # Mixed responsibilities
        has_gui = self._detect_gui_code(content)
        has_logic = self._detect_business_logic(content)
        has_data = self._detect_data_access(content)
        
        responsibility_count = sum([has_gui, has_logic, has_data])
        if responsibility_count > 1:
            issues.append(f"Mixed responsibilities detected - GUI: {has_gui}, Logic: {has_logic}, Data: {has_data}")
        
        # Duplicate detection (will be populated after all files are analyzed)
        # This is handled in the main analysis loop
        
        return issues
    
    def _generate_recommendations(self, file_path: str, size_kb: float, line_count: int, 
                                ast_analysis: Dict, has_gui: bool, has_logic: bool, has_data: bool) -> List[str]:
        """Generate refactoring recommendations"""
        recommendations = []
        
        # Size-based recommendations
        if size_kb > 50:
            recommendations.append("Split into multiple smaller files")
            recommendations.append("Extract classes into separate modules")
            recommendations.append("Create a dedicated module for this functionality")
        elif size_kb > 20:
            recommendations.append("Consider extracting large functions into separate modules")
            recommendations.append("Group related functionality into classes")
        
        # Responsibility-based recommendations
        if has_gui and has_logic:
            recommendations.append("Separate GUI code from business logic using MVC pattern")
            recommendations.append("Create separate UI and controller modules")
        
        if has_logic and has_data:
            recommendations.append("Separate business logic from data access using repository pattern")
            recommendations.append("Create dedicated service layer")
        
        if has_gui and has_data:
            recommendations.append("Separate GUI code from data access")
            recommendations.append("Use data binding or observer pattern")
        
        # Function-based recommendations
        if ast_analysis['function_count'] > 20:
            recommendations.append("Group related functions into classes")
            recommendations.append("Create separate utility modules")
        
        # Class-based recommendations
        if ast_analysis['class_count'] > 10:
            recommendations.append("Split classes into separate modules")
            recommendations.append("Use inheritance to reduce code duplication")
        
        # Complexity-based recommendations
        if ast_analysis['nesting_depth'] > 5:
            recommendations.append("Simplify nested conditions using early returns")
            recommendations.append("Extract complex logic into separate functions")
        
        # Duplicate-based recommendations (will be populated after all files are analyzed)
        # This is handled in the main analysis loop
        
        return recommendations

class ASTAnalyzer:
    """Analyzes Python AST for detailed metrics"""
    
    def __init__(self):
        self.max_nesting_depth = 0
        self.current_nesting = 0
    
    def analyze_ast(self, tree: ast.AST) -> Dict:
        """Analyze AST and return metrics"""
        self.max_nesting_depth = 0
        self.current_nesting = 0
        
        visitor = ASTVisitor()
        visitor.visit(tree)
        
        return {
            'line_count': self._count_lines(tree),
            'function_count': visitor.function_count,
            'class_count': visitor.class_count,
            'import_count': visitor.import_count,
            'nesting_depth': visitor.max_nesting_depth,
            'variable_count': visitor.variable_count,
            'method_count': visitor.method_count,
            'functions': visitor.functions,
            'classes': visitor.classes
        }
    
    def _count_lines(self, tree: ast.AST) -> int:
        """Count actual code lines (excluding comments and empty lines)"""
        lines = set()
        for node in ast.walk(tree):
            if hasattr(node, 'lineno'):
                lines.add(node.lineno)
        return len(lines)

class ASTVisitor(ast.NodeVisitor):
    """AST visitor for counting various code elements"""
    
    def __init__(self):
        self.function_count = 0
        self.class_count = 0
        self.import_count = 0
        self.variable_count = 0
        self.method_count = 0
        self.max_nesting_depth = 0
        self.current_nesting = 0
        self.functions = []
        self.classes = []
    
    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        
        # Extract function signature for duplicate detection
        func_signature = self._extract_function_signature(node)
        self.functions.append(func_signature)
        
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_ClassDef(self, node):
        self.class_count += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        
        # Extract class signature for duplicate detection
        class_signature = self._extract_class_signature(node)
        self.classes.append(class_signature)
        
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_Import(self, node):
        self.import_count += 1
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        self.import_count += 1
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        self.variable_count += 1
        self.generic_visit(node)
    
    def visit_If(self, node):
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_For(self, node):
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_While(self, node):
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_Try(self, node):
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def _extract_function_signature(self, node):
        """Extract a normalized function signature for duplicate detection"""
        # Get function name
        name = node.name
        
        # Get argument names (normalized)
        args = []
        if node.args.args:
            for arg in node.args.args:
                args.append(arg.arg)
        
        # Get return type hint if available
        return_type = ""
        if node.returns:
            return_type = ast.unparse(node.returns) if hasattr(ast, 'unparse') else str(node.returns)
        
        # Create normalized signature with 'def' keyword
        signature = f"def {name}({','.join(args)})"
        if return_type:
            signature += f" -> {return_type}"
        
        return signature
    
    def _extract_class_signature(self, node):
        """Extract a normalized class signature for duplicate detection"""
        # Get class name
        name = node.name
        
        # Get base classes
        bases = []
        if node.bases:
            for base in node.bases:
                if hasattr(ast, 'unparse'):
                    bases.append(ast.unparse(base))
                else:
                    bases.append(str(base))
        
        # Get class methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        
        # Create normalized signature with 'class' keyword
        signature = f"class {name}"
        if bases:
            signature += f"({','.join(bases)})"
        signature += f" methods:[{','.join(methods)}]"
        
        return signature

class DuplicateDetector:
    """Detects duplicate functions and classes across the codebase"""
    
    def __init__(self):
        self.function_signatures = {}  # signature -> [file_paths]
        self.class_signatures = {}     # signature -> [file_paths]
    
    def add_file_analysis(self, file_path: str, functions: List[str], classes: List[str]):
        """Add function and class signatures from a file"""
        for func_sig in functions:
            if func_sig not in self.function_signatures:
                self.function_signatures[func_sig] = []
            self.function_signatures[func_sig].append(file_path)
        
        for class_sig in classes:
            if class_sig not in self.class_signatures:
                self.class_signatures[class_sig] = []
            self.class_signatures[class_sig].append(file_path)
    
    def get_duplicate_functions(self) -> List[Tuple[str, List[str]]]:
        """Get functions that appear in multiple files"""
        duplicates = []
        for signature, file_paths in self.function_signatures.items():
            if len(file_paths) > 1:
                duplicates.append((signature, file_paths))
        return sorted(duplicates, key=lambda x: len(x[1]), reverse=True)
    
    def get_duplicate_classes(self) -> List[Tuple[str, List[str]]]:
        """Get classes that appear in multiple files"""
        duplicates = []
        for signature, file_paths in self.class_signatures.items():
            if len(file_paths) > 1:
                duplicates.append((signature, file_paths))
        return sorted(duplicates, key=lambda x: len(x[1]), reverse=True)
    
    def get_file_duplicates(self, file_path: str) -> Tuple[List[str], List[str]]:
        """Get duplicate functions and classes for a specific file"""
        file_duplicate_functions = []
        file_duplicate_classes = []
        
        for signature, file_paths in self.function_signatures.items():
            if file_path in file_paths and len(file_paths) > 1:
                file_duplicate_functions.append(signature)
        
        for signature, file_paths in self.class_signatures.items():
            if file_path in file_paths and len(file_paths) > 1:
                file_duplicate_classes.append(signature)
        
        return file_duplicate_functions, file_duplicate_classes

class RefactoringAnalyzer:
    """Main analyzer class that coordinates the analysis"""
    
    def __init__(self, root_path: str = "."):
        self.root_path = Path(root_path)
        self.code_analyzer = CodeAnalyzer()
        
    def analyze_codebase(self) -> RefactoringReport:
        """Analyze the entire codebase and generate recommendations"""
        logger.info("Starting codebase analysis...")
        
        # Find all Python files
        python_files = self._find_python_files()
        logger.info(f"Found {len(python_files)} Python files")
        
        # Analyze each file
        file_analyses = []
        for file_path in python_files:
            analysis = self.code_analyzer.analyze_file(str(file_path))
            file_analyses.append(analysis)
        
        # Analyze directories
        directory_analyses = self._analyze_directories(file_analyses)
        
        # Get duplicate information
        duplicate_functions = self.code_analyzer.duplicate_detector.get_duplicate_functions()
        duplicate_classes = self.code_analyzer.duplicate_detector.get_duplicate_classes()
        
        # Categorize files by priority
        high_priority = self._get_high_priority_files(file_analyses)
        medium_priority = self._get_medium_priority_files(file_analyses)
        low_priority = self._get_low_priority_files(file_analyses)
        
        # Generate architectural issues
        architectural_issues = self._identify_architectural_issues(file_analyses, directory_analyses)
        
        # Generate general recommendations
        general_recommendations = self._generate_general_recommendations(file_analyses, directory_analyses)
        
        # Update file analyses with duplicate information
        self._update_file_analyses_with_duplicates(file_analyses)
        
        # Create report
        report = RefactoringReport(
            timestamp=datetime.now().isoformat(),
            total_files=len(python_files),
            total_lines=sum(f.line_count for f in file_analyses),
            total_size_kb=sum(f.size_kb for f in file_analyses),
            files_needing_refactoring=[f for f in file_analyses if f.issues],
            directories_needing_refactoring=[d for d in directory_analyses if d.issues],
            high_priority_files=high_priority,
            medium_priority_files=medium_priority,
            low_priority_files=low_priority,
            duplicate_functions=duplicate_functions,
            duplicate_classes=duplicate_classes,
            architectural_issues=architectural_issues,
            general_recommendations=general_recommendations
        )
        
        logger.info("Analysis complete!")
        return report
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase"""
        python_files = []
        
        for root, dirs, files in os.walk(self.root_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.code_analyzer.ignore_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    # Check if file should be ignored
                    if self._should_ignore_file(file_path):
                        continue
                    
                    python_files.append(file_path)
        
        return python_files
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if a file should be ignored based on various ignore rules"""
        # Convert to string for easier comparison
        file_str = str(file_path)
        file_name = file_path.name
        
        # Check file extensions
        for ext in self.code_analyzer.ignore_files:
            if file_name.endswith(ext):
                return True
        
        # Check specific files (by name or full path)
        for ignore_file in self.code_analyzer.ignore_specific_files:
            if file_name == ignore_file or file_str.endswith(ignore_file):
                return True
        
        # Check file patterns
        for pattern in self.code_analyzer.ignore_file_patterns:
            if re.match(pattern, file_str):
                return True
        
        return False
    
    def add_ignore_file(self, file_path: str):
        """Add a specific file to ignore list"""
        self.code_analyzer.ignore_specific_files.add(file_path)
    
    def add_ignore_pattern(self, pattern: str):
        """Add a regex pattern to ignore list"""
        self.code_analyzer.ignore_file_patterns.append(pattern)
    
    def add_ignore_directory(self, dir_name: str):
        """Add a directory to ignore list"""
        self.code_analyzer.ignore_dirs.add(dir_name)
    
    def get_ignore_info(self) -> Dict[str, List[str]]:
        """Get information about what's being ignored"""
        return {
            'ignored_directories': list(self.code_analyzer.ignore_dirs),
            'ignored_file_extensions': list(self.code_analyzer.ignore_files),
            'ignored_specific_files': list(self.code_analyzer.ignore_specific_files),
            'ignored_file_patterns': self.code_analyzer.ignore_file_patterns
        }
    
    def _analyze_directories(self, file_analyses: List[FileAnalysis]) -> List[DirectoryAnalysis]:
        """Analyze directories for patterns and issues"""
        directory_analyses = []
        
        # Group files by directory
        dir_files = {}
        for analysis in file_analyses:
            dir_path = str(Path(analysis.path).parent)
            if dir_path not in dir_files:
                dir_files[dir_path] = []
            dir_files[dir_path].append(analysis)
        
        # Analyze each directory
        for dir_path, files in dir_files.items():
            total_lines = sum(f.line_count for f in files)
            total_size = sum(f.size_kb for f in files)
            
            # Find largest files
            largest_files = sorted([(f.path, f.size_kb) for f in files], 
                                 key=lambda x: x[1], reverse=True)[:5]
            
            # Find most complex files
            most_complex = sorted([(f.path, f.complexity_score) for f in files], 
                                key=lambda x: x[1], reverse=True)[:5]
            
            # Identify directory issues
            issues = self._identify_directory_issues(dir_path, files)
            
            # Generate directory recommendations
            recommendations = self._generate_directory_recommendations(dir_path, files)
            
            analysis = DirectoryAnalysis(
                path=dir_path,
                file_count=len(files),
                total_lines=total_lines,
                total_size_kb=total_size,
                largest_files=largest_files,
                most_complex_files=most_complex,
                issues=issues,
                recommendations=recommendations
            )
            
            directory_analyses.append(analysis)
        
        return directory_analyses
    
    def _identify_directory_issues(self, dir_path: str, files: List[FileAnalysis]) -> List[str]:
        """Identify issues specific to a directory"""
        issues = []
        
        # Check for mixed responsibilities
        gui_files = [f for f in files if f.has_gui_code]
        logic_files = [f for f in files if f.has_business_logic]
        data_files = [f for f in files if f.has_data_access]
        
        if gui_files and logic_files and len(gui_files) + len(logic_files) > len(files) * 0.7:
            issues.append("Directory contains mixed GUI and business logic - consider separation")
        
        if logic_files and data_files and len(logic_files) + len(data_files) > len(files) * 0.7:
            issues.append("Directory contains mixed business logic and data access - consider separation")
        
        # Check for large files
        large_files = [f for f in files if f.size_kb > 20]
        if len(large_files) > len(files) * 0.3:
            issues.append("Directory contains many large files - consider modularization")
        
        # Check for complex files
        complex_files = [f for f in files if f.complexity_score > 0.7]
        if len(complex_files) > len(files) * 0.3:
            issues.append("Directory contains many complex files - consider simplification")
        
        return issues
    
    def _generate_directory_recommendations(self, dir_path: str, files: List[FileAnalysis]) -> List[str]:
        """Generate recommendations for a directory"""
        recommendations = []
        
        # Check directory structure
        gui_files = [f for f in files if f.has_gui_code]
        logic_files = [f for f in files if f.has_business_logic]
        data_files = [f for f in files if f.has_data_access]
        
        if gui_files and logic_files:
            recommendations.append("Create separate 'ui' and 'logic' subdirectories")
        
        if logic_files and data_files:
            recommendations.append("Create separate 'services' and 'data' subdirectories")
        
        # Check for large files
        large_files = [f for f in files if f.size_kb > 20]
        if large_files:
            recommendations.append("Split large files into smaller, focused modules")
        
        # Check for complex files
        complex_files = [f for f in files if f.complexity_score > 0.7]
        if complex_files:
            recommendations.append("Simplify complex files by extracting helper functions")
        
        return recommendations
    
    def _get_high_priority_files(self, file_analyses: List[FileAnalysis]) -> List[str]:
        """Get files that need immediate refactoring attention"""
        high_priority = []
        
        for analysis in file_analyses:
            if (analysis.size_kb > 50 or 
                analysis.line_count > 1000 or 
                analysis.complexity_score > 0.8 or
                len(analysis.issues) > 3):
                high_priority.append(analysis.path)
        
        return high_priority
    
    def _get_medium_priority_files(self, file_analyses: List[FileAnalysis]) -> List[str]:
        """Get files that need refactoring but are not urgent"""
        medium_priority = []
        
        for analysis in file_analyses:
            if (20 < analysis.size_kb <= 50 or 
                500 < analysis.line_count <= 1000 or 
                0.6 < analysis.complexity_score <= 0.8 or
                1 < len(analysis.issues) <= 3):
                medium_priority.append(analysis.path)
        
        return medium_priority
    
    def _get_low_priority_files(self, file_analyses: List[FileAnalysis]) -> List[str]:
        """Get files that could benefit from minor improvements"""
        low_priority = []
        
        for analysis in file_analyses:
            if (analysis.size_kb > 10 or 
                analysis.line_count > 200 or 
                analysis.complexity_score > 0.4):
                low_priority.append(analysis.path)
        
        return low_priority
    
    def _identify_architectural_issues(self, file_analyses: List[FileAnalysis], 
                                     directory_analyses: List[DirectoryAnalysis]) -> List[str]:
        """Identify architectural issues across the codebase"""
        issues = []
        
        # Check for monolithic files
        large_files = [f for f in file_analyses if f.size_kb > 50]
        if large_files:
            issues.append(f"Found {len(large_files)} very large files - consider breaking into modules")
        
        # Check for mixed responsibilities
        mixed_files = [f for f in file_analyses if f.has_gui_code and f.has_business_logic]
        if mixed_files:
            issues.append(f"Found {len(mixed_files)} files with mixed GUI and business logic - consider MVC pattern")
        
        # Check for deep nesting
        complex_files = [f for f in file_analyses if f.complexity_score > 0.8]
        if complex_files:
            issues.append(f"Found {len(complex_files)} highly complex files - consider simplifying logic")
        
        # Check directory structure
        large_dirs = [d for d in directory_analyses if d.total_size_kb > 500]
        if large_dirs:
            issues.append(f"Found {len(large_dirs)} very large directories - consider reorganization")
        
        # Check for duplicates
        duplicate_functions = self.code_analyzer.duplicate_detector.get_duplicate_functions()
        duplicate_classes = self.code_analyzer.duplicate_detector.get_duplicate_classes()
        
        if duplicate_functions:
            issues.append(f"Found {len(duplicate_functions)} duplicate functions across the codebase - consider consolidation")
        
        if duplicate_classes:
            issues.append(f"Found {len(duplicate_classes)} duplicate classes across the codebase - consider consolidation")
        
        return issues
    
    def _generate_general_recommendations(self, file_analyses: List[FileAnalysis], 
                                        directory_analyses: List[DirectoryAnalysis]) -> List[str]:
        """Generate general refactoring recommendations"""
        recommendations = []
        
        # Overall statistics
        total_files = len(file_analyses)
        large_files = len([f for f in file_analyses if f.size_kb > 20])
        complex_files = len([f for f in file_analyses if f.complexity_score > 0.6])
        
        if large_files > total_files * 0.2:
            recommendations.append("Many large files detected - implement consistent file size limits")
        
        if complex_files > total_files * 0.3:
            recommendations.append("Many complex files detected - implement complexity guidelines")
        
        # Architecture recommendations
        gui_files = [f for f in file_analyses if f.has_gui_code]
        logic_files = [f for f in file_analyses if f.has_business_logic]
        
        if gui_files and logic_files:
            recommendations.append("Consider implementing MVC or MVVM pattern for better separation")
        
        # Code organization recommendations
        recommendations.append("Create consistent naming conventions for files and directories")
        recommendations.append("Implement dependency injection for better testability")
        recommendations.append("Consider using design patterns to reduce code duplication")
        
        # Duplicate-related recommendations
        duplicate_functions = self.code_analyzer.duplicate_detector.get_duplicate_functions()
        duplicate_classes = self.code_analyzer.duplicate_detector.get_duplicate_classes()
        
        if duplicate_functions:
            recommendations.append("Create a shared utilities module for common functions")
            recommendations.append("Implement a common library for frequently used functionality")
        
        if duplicate_classes:
            recommendations.append("Create base classes for common functionality")
            recommendations.append("Use composition over inheritance where appropriate")
        
        return recommendations
    
    def _update_file_analyses_with_duplicates(self, file_analyses: List[FileAnalysis]):
        """Update file analyses with duplicate-related issues and recommendations"""
        duplicate_functions = self.code_analyzer.duplicate_detector.get_duplicate_functions()
        duplicate_classes = self.code_analyzer.duplicate_detector.get_duplicate_classes()
        
        for analysis in file_analyses:
            # Get duplicates for this file
            file_duplicate_functions, file_duplicate_classes = self.code_analyzer.duplicate_detector.get_file_duplicates(analysis.path)
            
            # Add duplicate-related issues
            if file_duplicate_functions:
                analysis.issues.append(f"Contains {len(file_duplicate_functions)} duplicate functions that could be consolidated")
            
            if file_duplicate_classes:
                analysis.issues.append(f"Contains {len(file_duplicate_classes)} duplicate classes that could be consolidated")
            
            # Add duplicate-related recommendations
            if file_duplicate_functions:
                analysis.recommendations.append("Extract duplicate functions into a shared utility module")
                analysis.recommendations.append("Consider creating a common library for shared functionality")
            
            if file_duplicate_classes:
                analysis.recommendations.append("Extract duplicate classes into a shared base module")
                analysis.recommendations.append("Consider using inheritance to reduce code duplication")

def save_report_as_markdown(report: RefactoringReport, output_path: str = "Development_Tools/Reports/refactoring_report.md"):
    """Save the refactoring report as a markdown file"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Codebase Refactoring Analysis Report\n\n")
        f.write(f"**Generated:** {report.timestamp}\n\n")
        
        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"- **Total Files:** {report.total_files}\n")
        f.write(f"- **Total Lines:** {report.total_lines:,}\n")
        f.write(f"- **Total Size:** {report.total_size_kb:.1f} KB\n")
        f.write(f"- **Files Needing Refactoring:** {len(report.files_needing_refactoring)}\n")
        f.write(f"- **Directories Needing Refactoring:** {len(report.directories_needing_refactoring)}\n\n")
        
        # High Priority Files
        if report.high_priority_files:
            f.write("## 🔴 High Priority Files\n\n")
            f.write("These files need immediate refactoring attention:\n\n")
            for file_path in report.high_priority_files:
                f.write(f"- `{file_path}`\n")
            f.write("\n")
        
        # Medium Priority Files
        if report.medium_priority_files:
            f.write("## 🟡 Medium Priority Files\n\n")
            f.write("These files need refactoring but are not urgent:\n\n")
            for file_path in report.medium_priority_files:
                f.write(f"- `{file_path}`\n")
            f.write("\n")
        
        # Low Priority Files
        if report.low_priority_files:
            f.write("## 🟢 Low Priority Files\n\n")
            f.write("These files could benefit from minor improvements:\n\n")
            for file_path in report.low_priority_files:
                f.write(f"- `{file_path}`\n")
            f.write("\n")
        
        # Duplicate Functions
        if report.duplicate_functions:
            f.write("## 🔄 Duplicate Functions\n\n")
            f.write("These functions appear in multiple files and could be consolidated:\n\n")
            for signature, file_paths in report.duplicate_functions:
                f.write(f"### `{signature}`\n")
                f.write(f"**Found in:** {len(file_paths)} files\n")
                f.write("**Files:**\n")
                for file_path in file_paths:
                    f.write(f"- `{file_path}`\n")
                f.write("\n")
        
        # Duplicate Classes
        if report.duplicate_classes:
            f.write("## 🔄 Duplicate Classes\n\n")
            f.write("These classes appear in multiple files and could be consolidated:\n\n")
            for signature, file_paths in report.duplicate_classes:
                f.write(f"### `{signature}`\n")
                f.write(f"**Found in:** {len(file_paths)} files\n")
                f.write("**Files:**\n")
                for file_path in file_paths:
                    f.write(f"- `{file_path}`\n")
                f.write("\n")
        
        # Detailed File Analysis
        if report.files_needing_refactoring:
            f.write("## 📋 Detailed File Analysis\n\n")
            for analysis in report.files_needing_refactoring:
                f.write(f"### {analysis.path}\n\n")
                f.write(f"- **Size:** {analysis.size_kb:.1f} KB ({analysis.line_count} lines)\n")
                f.write(f"- **Classes:** {analysis.class_count}\n")
                f.write(f"- **Functions:** {analysis.function_count}\n")
                f.write(f"- **Complexity Score:** {analysis.complexity_score:.2f}\n")
                f.write(f"- **Responsibilities:** GUI: {analysis.has_gui_code}, Logic: {analysis.has_business_logic}, Data: {analysis.has_data_access}\n\n")
                
                if analysis.duplicate_functions:
                    f.write("**Duplicate Functions:**\n")
                    for func_sig in analysis.duplicate_functions:
                        f.write(f"- `{func_sig}`\n")
                    f.write("\n")
                
                if analysis.duplicate_classes:
                    f.write("**Duplicate Classes:**\n")
                    for class_sig in analysis.duplicate_classes:
                        f.write(f"- `{class_sig}`\n")
                    f.write("\n")
                
                if analysis.issues:
                    f.write("**Issues:**\n")
                    for issue in analysis.issues:
                        f.write(f"- {issue}\n")
                    f.write("\n")
                
                if analysis.recommendations:
                    f.write("**Recommendations:**\n")
                    for rec in analysis.recommendations:
                        f.write(f"- {rec}\n")
                    f.write("\n")
        
        # Directory Analysis
        if report.directories_needing_refactoring:
            f.write("## 📁 Directory Analysis\n\n")
            for analysis in report.directories_needing_refactoring:
                f.write(f"### {analysis.path}\n\n")
                f.write(f"- **Files:** {analysis.file_count}\n")
                f.write(f"- **Total Lines:** {analysis.total_lines:,}\n")
                f.write(f"- **Total Size:** {analysis.total_size_kb:.1f} KB\n\n")
                
                if analysis.largest_files:
                    f.write("**Largest Files:**\n")
                    for file_path, size in analysis.largest_files:
                        f.write(f"- `{file_path}` ({size:.1f} KB)\n")
                    f.write("\n")
                
                if analysis.most_complex_files:
                    f.write("**Most Complex Files:**\n")
                    for file_path, complexity in analysis.most_complex_files:
                        f.write(f"- `{file_path}` (complexity: {complexity:.2f})\n")
                    f.write("\n")
                
                if analysis.issues:
                    f.write("**Issues:**\n")
                    for issue in analysis.issues:
                        f.write(f"- {issue}\n")
                    f.write("\n")
                
                if analysis.recommendations:
                    f.write("**Recommendations:**\n")
                    for rec in analysis.recommendations:
                        f.write(f"- {rec}\n")
                    f.write("\n")
        
        # Architectural Issues
        if report.architectural_issues:
            f.write("## 🏗️ Architectural Issues\n\n")
            for issue in report.architectural_issues:
                f.write(f"- {issue}\n")
            f.write("\n")
        
        # General Recommendations
        if report.general_recommendations:
            f.write("## 💡 General Recommendations\n\n")
            for rec in report.general_recommendations:
                f.write(f"- {rec}\n")
            f.write("\n")
        
        # Implementation Plan
        f.write("## 📋 Implementation Plan\n\n")
        f.write("### Phase 1: High Priority Files\n")
        f.write("1. Start with the largest and most complex files\n")
        f.write("2. Separate GUI code from business logic\n")
        f.write("3. Extract large functions into smaller, focused functions\n")
        f.write("4. Create dedicated modules for related functionality\n\n")
        
        f.write("### Phase 2: Medium Priority Files\n")
        f.write("1. Address files with mixed responsibilities\n")
        f.write("2. Implement consistent naming conventions\n")
        f.write("3. Reduce complexity through refactoring\n\n")
        
        f.write("### Phase 3: Low Priority Files\n")
        f.write("1. Apply minor improvements and optimizations\n")
        f.write("2. Standardize code style and formatting\n")
        f.write("3. Add documentation where needed\n\n")
        
        f.write("### Phase 4: Architectural Improvements\n")
        f.write("1. Implement design patterns (MVC, Repository, etc.)\n")
        f.write("2. Create proper separation of concerns\n")
        f.write("3. Improve testability and maintainability\n\n")
        
        f.write("### Phase 5: Duplicate Consolidation\n")
        f.write("1. Identify and consolidate duplicate functions into shared utilities\n")
        f.write("2. Create base classes for duplicate class functionality\n")
        f.write("3. Implement common libraries for frequently used code\n")
        f.write("4. Update imports to use consolidated modules\n\n")
    
    print(f"Report saved to: {output_path}")

def main():
    """Main function to run the refactoring analyzer"""
    print("🔍 Starting Codebase Refactoring Analysis...")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = RefactoringAnalyzer()
    
    # Example: Add additional ignore rules programmatically
    # analyzer.add_ignore_file("specific_file.py")
    # analyzer.add_ignore_pattern(r".*_test\.py$")
    # analyzer.add_ignore_directory("test_dir")
    
    # Run analysis
    report = analyzer.analyze_codebase()
    
    # Print ignore information for debugging
    ignore_info = analyzer.get_ignore_info()
    print("\n📋 Ignore Rules:")
    print(f"   Ignored Directories: {len(ignore_info['ignored_directories'])}")
    print(f"   Ignored File Extensions: {len(ignore_info['ignored_file_extensions'])}")
    print(f"   Ignored Specific Files: {len(ignore_info['ignored_specific_files'])}")
    print(f"   Ignored File Patterns: {len(ignore_info['ignored_file_patterns'])}")
    
    # Save report
    save_report_as_markdown(report)
    
    # Print summary
    print("\n📊 Analysis Summary:")
    print(f"   Total Files: {report.total_files}")
    print(f"   Total Lines: {report.total_lines:,}")
    print(f"   Total Size: {report.total_size_kb:.1f} KB")
    print(f"   Files Needing Refactoring: {len(report.files_needing_refactoring)}")
    print(f"   High Priority Files: {len(report.high_priority_files)}")
    print(f"   Medium Priority Files: {len(report.medium_priority_files)}")
    print(f"   Low Priority Files: {len(report.low_priority_files)}")
    print(f"   Duplicate Functions: {len(report.duplicate_functions)}")
    print(f"   Duplicate Classes: {len(report.duplicate_classes)}")
    
    if report.high_priority_files:
        print("\n🔴 High Priority Files:")
        for file_path in report.high_priority_files[:5]:  # Show top 5
            print(f"   - {file_path}")
        if len(report.high_priority_files) > 5:
            print(f"   ... and {len(report.high_priority_files) - 5} more")
    
    print(f"\n✅ Report saved to: Development_Tools/Reports/refactoring_report.md")

if __name__ == "__main__":
    main() 