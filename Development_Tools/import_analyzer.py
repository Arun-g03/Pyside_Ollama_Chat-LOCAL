#!/usr/bin/env python3
from pyside_chat.core.shared_imports.pyside_imports import *
"""
Import Analyzer Tool

This tool analyzes the pyside_chat codebase to:
1. Identify all import statements across the codebase
2. Detect circular dependencies
3. Suggest shared import files to reduce duplication
4. Generate dependency graphs
5. Provide recommendations for import optimization
"""

import os
import sys
import ast
import json
import networkx as nx
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from collections import defaultdict, Counter
import re
from dataclasses import dataclass, asdict
from datetime import datetime

# Add the project root to the path so we can import from pyside_chat
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from pyside_chat.core.logging.logger import CustomLogger
    logger = CustomLogger.get_logger(__name__)
except ImportError:
    # Fallback logger if the main logger isn't available
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

@dataclass
class ImportInfo:
    """Information about a single import statement"""
    module: str
    imports: List[str]
    line_number: int
    import_type: str  # 'import', 'from_import', 'from_import_as'
    alias: Optional[str] = None
    relative_level: int = 0

@dataclass
class FileAnalysis:
    """Analysis results for a single file"""
    file_path: str
    imports: List[ImportInfo]
    functions: List[str]
    classes: List[str]
    dependencies: Set[str]
    circular_dependencies: List[str]
    total_lines: int
    import_lines: int

@dataclass
class SharedImportGroup:
    """A group of commonly imported modules that could be shared"""
    modules: List[str]
    frequency: int
    files: List[str]
    category: str
    suggested_shared_file: str

class ImportAnalyzer:
    """Main analyzer class for processing import statements"""
    
    def __init__(self, codebase_path: str = "pyside_chat"):
        self.codebase_path = Path(codebase_path)
        self.all_files: Dict[str, FileAnalysis] = {}
        self.dependency_graph = nx.DiGraph()
        self.import_frequency = Counter()
        self.shared_imports: List[SharedImportGroup] = []
        self.circular_dependencies: List[List[str]] = []
        
    def scan_codebase(self) -> Dict[str, FileAnalysis]:
        """Scan the entire codebase for Python files and analyze imports"""
        logger.info(f"Scanning codebase at: {self.codebase_path}")
        
        python_files = list(self.codebase_path.rglob("*.py"))
        logger.info(f"Found {len(python_files)} Python files")
        
        for file_path in python_files:
            try:
                analysis = self.analyze_file(file_path)
                if analysis:
                    self.all_files[str(file_path)] = analysis
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        logger.info(f"Successfully analyzed {len(self.all_files)} files")
        return self.all_files
    
    def analyze_file(self, file_path: Path) -> Optional[FileAnalysis]:
        """Analyze a single Python file for imports and dependencies"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            imports = []
            functions = []
            classes = []
            dependencies = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(ImportInfo(
                            module=alias.name,
                            imports=[alias.name],
                            line_number=node.lineno,
                            import_type='import',
                            alias=alias.asname
                        ))
                        dependencies.add(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    relative_level = node.level
                    
                    for alias in node.names:
                        imports.append(ImportInfo(
                            module=module,
                            imports=[alias.name],
                            line_number=node.lineno,
                            import_type='from_import',
                            alias=alias.asname,
                            relative_level=relative_level
                        ))
                        dependencies.add(f"{module}.{alias.name}" if module else alias.name)
                
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
            
            return FileAnalysis(
                file_path=str(file_path),
                imports=imports,
                functions=functions,
                classes=classes,
                dependencies=dependencies,
                circular_dependencies=[],
                total_lines=len(content.splitlines()),
                import_lines=len([imp for imp in imports])
            )
            
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return None
    
    def build_dependency_graph(self):
        """Build a directed graph of module dependencies"""
        logger.info("Building dependency graph...")
        
        for file_path, analysis in self.all_files.items():
            module_name = self.get_module_name(file_path)
            self.dependency_graph.add_node(module_name)
            
            for import_info in analysis.imports:
                if import_info.import_type == 'from_import' and import_info.relative_level > 0:
                    # Handle relative imports
                    target_module = self.resolve_relative_import(file_path, import_info)
                    if target_module:
                        self.dependency_graph.add_edge(module_name, target_module)
                elif import_info.module.startswith('pyside_chat'):
                    # Handle internal imports
                    self.dependency_graph.add_edge(module_name, import_info.module)
        
        logger.info(f"Dependency graph built with {self.dependency_graph.number_of_nodes()} nodes and {self.dependency_graph.number_of_edges()} edges")
    
    def get_module_name(self, file_path: str) -> str:
        """Convert file path to module name"""
        rel_path = Path(file_path).relative_to(self.codebase_path)
        return str(rel_path).replace(os.sep, '.').replace('.py', '')
    
    def resolve_relative_import(self, file_path: str, import_info: ImportInfo) -> Optional[str]:
        """Resolve relative import to absolute module name"""
        try:
            current_dir = Path(file_path).parent
            target_path = current_dir
            
            # Navigate up the directory tree based on relative level
            for _ in range(import_info.relative_level - 1):
                target_path = target_path.parent
            
            # Add the module path
            if import_info.module:
                target_path = target_path / import_info.module.replace('.', os.sep)
            
            # Convert to module name
            rel_path = target_path.relative_to(self.codebase_path)
            return str(rel_path).replace(os.sep, '.')
        except Exception:
            return None
    
    def detect_circular_dependencies(self) -> List[List[str]]:
        """Detect circular dependencies in the codebase"""
        logger.info("Detecting circular dependencies...")
        
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            self.circular_dependencies = cycles
            
            if cycles:
                logger.warning(f"Found {len(cycles)} circular dependency cycles:")
                for cycle in cycles:
                    logger.warning(f"  {' -> '.join(cycle)} -> {cycle[0]}")
            else:
                logger.info("No circular dependencies detected")
            
            return cycles
        except Exception as e:
            logger.error(f"Error detecting circular dependencies: {e}")
            return []
    
    def analyze_import_frequency(self):
        """Analyze frequency of imports across the codebase"""
        logger.info("Analyzing import frequency...")
        
        for file_path, analysis in self.all_files.items():
            for import_info in analysis.imports:
                if import_info.import_type == 'from_import':
                    module_key = f"{import_info.module}.{import_info.imports[0]}"
                else:
                    module_key = import_info.module
                
                self.import_frequency[module_key] += 1
    
    def identify_shared_imports(self, min_frequency: int = 3) -> List[SharedImportGroup]:
        """Identify commonly imported modules that could be shared"""
        logger.info("Identifying shared imports...")
        
        # Group imports by category
        categories = {
            'logging': ['logging', 'pyside_chat.core.logging.logger', 'pyside_chat.core.logging.helpers'],
            'qt_core': ['PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui', 'PySide6.QtMultimedia'],
            'typing': ['typing', 'dataclasses'],
            'os_sys': ['os', 'sys', 'pathlib', 'tempfile'],
            'json_time': ['json', 'time', 'datetime'],
            'threading': ['threading', 'concurrent.futures'],
            'audio': ['pyaudio', 'sounddevice', 'soundfile', 'librosa'],
            'ml_ai': ['torch', 'transformers', 'sentence_transformers', 'sklearn'],
            'requests': ['requests', 'urllib'],
            'numpy': ['numpy', 'scipy'],
        }
        
        shared_groups = []
        
        for category, modules in categories.items():
            category_imports = []
            files_using_category = []
            
            for module in modules:
                if module in self.import_frequency:
                    category_imports.append(module)
                    # Find files that import this module
                    for file_path, analysis in self.all_files.items():
                        for import_info in analysis.imports:
                            if (import_info.module == module or 
                                (import_info.import_type == 'from_import' and 
                                 f"{import_info.module}.{import_info.imports[0]}" == module)):
                                files_using_category.append(file_path)
            
            if len(category_imports) >= min_frequency:
                shared_groups.append(SharedImportGroup(
                    modules=category_imports,
                    frequency=len(set(files_using_category)),
                    files=list(set(files_using_category)),
                    category=category,
                    suggested_shared_file=f"pyside_chat/core/shared_imports/{category}_imports.py"
                ))
        
        self.shared_imports = shared_groups
        return shared_groups
    
    def generate_shared_import_files(self, output_dir: str = "pyside_chat/core/shared_imports"):
        """Generate shared import files based on analysis"""
        logger.info(f"Generating shared import files in {output_dir}")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for group in self.shared_imports:
            if group.frequency >= 3:  # Only create files for frequently used imports
                self.create_shared_import_file(group, output_path)
    
    def create_shared_import_file(self, group: SharedImportGroup, output_path: Path):
        """Create a shared import file for a group of imports"""
        file_path = output_path / f"{group.category}_imports.py"
        
        content = f'''"""
Shared imports for {group.category}

This file contains commonly used imports for {group.category} functionality.
Generated by ImportAnalyzer on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Usage:
    from pyside_chat.core.shared_imports.{group.category}_imports import *
"""

'''
        
        # Add imports based on category
        if group.category == 'logging':
            content += '''import logging
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.logging.helpers import LoggingHelpers

# Common logging setup
def get_logger(name: str):
    """Get a logger instance for the given name"""
    return CustomLogger.get_logger(name)
'''
        elif group.category == 'qt_core':
            content += '''from PySide6.QtCore import (
    Qt, Signal, QTimer, QThread, QMutex, QWaitCondition, QEvent, QObject, QUrl
)

'''
        elif group.category == 'typing':
            content += '''from typing import List, Dict, Optional, Tuple, Set, Any, Callable, Generator
from dataclasses import dataclass, asdict
'''
        elif group.category == 'os_sys':
            content += '''import os
import sys
import tempfile
from pathlib import Path
'''
        elif group.category == 'json_time':
            content += '''import json
import time
from datetime import datetime, timedelta
'''
        elif group.category == 'threading':
            content += '''import threading
import traceback
from concurrent.futures import ThreadPoolExecutor
'''
        elif group.category == 'audio':
            content += '''import pyaudio
import sounddevice as sd
import soundfile as sf
import librosa
'''
        elif group.category == 'ml_ai':
            content += '''try:
    import torch
    import torchaudio
    from transformers import AutoTokenizer, AutoModel
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
'''
        elif group.category == 'requests':
            content += '''import requests
import urllib.request
import urllib.parse
'''
        elif group.category == 'numpy':
            content += '''import numpy as np
import scipy
'''
        
        # Add statistics about usage
        content += f'''

# Statistics:
# - Used in {group.frequency} files
# - Files: {', '.join(group.files[:5])}{'...' if len(group.files) > 5 else ''}
'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created shared import file: {file_path}")
    
    def generate_report(self, output_file: str = "import_analysis_report.json"):
        """Generate a comprehensive analysis report"""
        logger.info(f"Generating analysis report: {output_file}")
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'codebase_path': str(self.codebase_path),
            'summary': {
                'total_files': len(self.all_files),
                'total_imports': sum(len(analysis.imports) for analysis in self.all_files.values()),
                'circular_dependencies': len(self.circular_dependencies),
                'shared_import_groups': len(self.shared_imports),
                'most_common_imports': self.import_frequency.most_common(20)
            },
            'circular_dependencies': self.circular_dependencies,
            'shared_imports': [asdict(group) for group in self.shared_imports],
            'file_analysis': {
                file_path: {
                    'imports': [asdict(imp) for imp in analysis.imports],
                    'functions': analysis.functions,
                    'classes': analysis.classes,
                    'dependencies': list(analysis.dependencies),
                    'total_lines': analysis.total_lines,
                    'import_lines': analysis.import_lines
                }
                for file_path, analysis in self.all_files.items()
            },
            'recommendations': self.generate_recommendations()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Report saved to: {output_file}")
        return report
    
    def generate_recommendations(self) -> Dict[str, Any]:
        """Generate recommendations for import optimization"""
        recommendations = {
            'shared_import_files': [],
            'circular_dependency_fixes': [],
            'import_optimizations': []
        }
        
        # Recommendations for shared import files
        for group in self.shared_imports:
            if group.frequency >= 3:
                recommendations['shared_import_files'].append({
                    'file': group.suggested_shared_file,
                    'category': group.category,
                    'modules': group.modules,
                    'files_affected': group.files,
                    'potential_savings': len(group.files) * len(group.modules)
                })
        
        # Recommendations for circular dependencies
        for cycle in self.circular_dependencies:
            recommendations['circular_dependency_fixes'].append({
                'cycle': cycle,
                'suggestion': 'Consider using dependency injection or moving shared code to a separate module'
            })
        
        # General import optimizations
        unused_imports = self.find_unused_imports()
        if unused_imports:
            recommendations['import_optimizations'].append({
                'type': 'unused_imports',
                'files': unused_imports
            })
        
        return recommendations
    
    def find_unused_imports(self) -> Dict[str, List[str]]:
        """Find potentially unused imports (basic analysis)"""
        unused = {}
        
        for file_path, analysis in self.all_files.items():
            unused_in_file = []
            
            for import_info in analysis.imports:
                # Basic check - if import name is not in functions or classes
                import_name = import_info.imports[0] if import_info.imports else import_info.module
                
                if (import_name not in analysis.functions and 
                    import_name not in analysis.classes):
                    # This is a basic check - could be used in other ways
                    unused_in_file.append(import_name)
            
            if unused_in_file:
                unused[file_path] = unused_in_file
        
        return unused
    
    def print_summary(self):
        """Print a summary of the analysis"""
        print("\n" + "="*60)
        print("IMPORT ANALYSIS SUMMARY")
        print("="*60)
        
        print(f"📁 Codebase: {self.codebase_path}")
        print(f"📄 Files analyzed: {len(self.all_files)}")
        print(f"📦 Total imports: {sum(len(analysis.imports) for analysis in self.all_files.values())}")
        print(f"🔄 Circular dependencies: {len(self.circular_dependencies)}")
        print(f"📋 Shared import groups: {len(self.shared_imports)}")
        
        if self.circular_dependencies:
            print("\n⚠️  CIRCULAR DEPENDENCIES:")
            for cycle in self.circular_dependencies:
                print(f"   {' -> '.join(cycle)} -> {cycle[0]}")
        
        if self.shared_imports:
            print("\n📋 SHARED IMPORT GROUPS:")
            for group in self.shared_imports:
                print(f"   {group.category}: {len(group.modules)} modules, {group.frequency} files")
        
        print("\n🔝 MOST COMMON IMPORTS:")
        for module, count in self.import_frequency.most_common(10):
            print(f"   {module}: {count} times")
        
        print("="*60)

def main():
    """Main function to run the import analyzer"""
    print("🔍 PySide Chat Import Analyzer")
    print("="*40)
    
    analyzer = ImportAnalyzer("pyside_chat")
    
    # Scan the codebase
    analyzer.scan_codebase()
    
    # Build dependency graph
    analyzer.build_dependency_graph()
    
    # Detect circular dependencies
    analyzer.detect_circular_dependencies()
    
    # Analyze import frequency
    analyzer.analyze_import_frequency()
    
    # Identify shared imports
    analyzer.identify_shared_imports()
    
    # Generate shared import files
    analyzer.generate_shared_import_files()
    
    # Generate report
    analyzer.generate_report()
    
    # Print summary
    analyzer.print_summary()
    
    print("\n✅ Analysis complete! Check the generated files and report for details.")

if __name__ == "__main__":
    main() 