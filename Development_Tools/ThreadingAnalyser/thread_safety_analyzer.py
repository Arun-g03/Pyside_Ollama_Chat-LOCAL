#!/usr/bin/env python3
"""
Thread Safety Analyzer for PySide6 Chat Application

Detects and warns about UI access from background threads in the current codebase.
This tool helps identify potential threading issues and ensures proper thread-safe UI updates.
"""

import sys
import os
import threading
import inspect
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from PySide6.QtCore import QThread, QObject, Signal, Slot, QMetaObject, Qt
from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QPushButton, QProgressBar, QSlider, QApplication

# Add at the top:
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import application modules
try:
    from pyside_chat.core.logging.logger import CustomLogger
    logger = CustomLogger.get_logger(__name__)
except ImportError:
    # Fallback logger if custom logger not available
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)


class ThreadSafetyAnalyzer:
    """Analyzes thread safety in the application"""
    
    def __init__(self):
        self.main_thread = None
        self.ui_methods = set()
        self.thread_violations = []
        self.safe_patterns = set()
        self.unsafe_patterns = set()
        
        # Common UI methods that should only be called from main thread
        self.ui_methods = {
            'setText', 'setValue', 'setEnabled', 'setVisible', 'setStyleSheet',
            'clear', 'append', 'insert', 'setPlainText', 'setHtml',
            'setMaximum', 'setMinimum', 'setRange', 'setSliderPosition',
            'addItem', 'removeItem', 'setCurrentIndex', 'setCurrentText',
            'setChecked', 'setIcon', 'setPixmap', 'setWindowTitle',
            'show', 'hide', 'close', 'raise_', 'lower',
            'update', 'repaint', 'updateGeometry', 'adjustSize',
            'setFocus', 'clearFocus', 'setCursor', 'setToolTip',
            'setStatusTip', 'setWhatsThis', 'setAccessibleName',
            'setWindowIcon', 'setWindowState', 'setWindowFlags'
        }
        
        # Safe patterns that are already thread-safe
        self.safe_patterns = {
            'QTimer.singleShot', 'QMetaObject.invokeMethod', 'safe_ui_update',
            'QueuedConnection', 'Qt.ConnectionType.QueuedConnection',
            '_render_chat_display_safe', '_update_eq_widget_safe',
            '_append_response_chunk_safe', '_stop_streaming_safe',
            '_handle_voice_input_safe', '_update_audio_level_ui_safe'
        }
        
        # Unsafe patterns that indicate potential issues
        self.unsafe_patterns = {
            'processEvents', 'QApplication.processEvents',
            'threading.Thread', 'threading.start_new_thread',
            'concurrent.futures.ThreadPoolExecutor'
        }
    
    def ensure_main_thread(self, method):
        """Decorator to ensure UI methods are called from main thread"""
        def wrapper(self, *args, **kwargs):
            if not self._is_main_thread():
                violation = {
                    'method': method.__name__,
                    'class': self.__class__.__name__,
                    'thread': threading.current_thread().name,
                    'stack_trace': traceback.format_stack()
                }
                self.thread_violations.append(violation)
                logger.warning(f"⚠️ UI method {method.__name__} called from background thread!")
                logger.warning(f"   Class: {self.__class__.__name__}")
                logger.warning(f"   Thread: {threading.current_thread().name}")
            return method(self, *args, **kwargs)
        return wrapper
    
    def _is_main_thread(self) -> bool:
        """Check if current thread is the main (GUI) thread"""
        try:
            app = QApplication.instance()
            if app:
                return QThread.currentThread() == app.thread()
            return threading.current_thread() == threading.main_thread()
        except Exception:
            return threading.current_thread() == threading.main_thread()
    
    def _is_false_positive(self, line: str, method: str) -> bool:
        """Check if a detected UI method call is actually a false positive"""
        # Common false positive patterns
        false_positive_patterns = [
            'markdown.append',  # Documentation generation
            'report.append',     # Report generation
            'results.append',    # Data collection
            'list.append',       # Generic list operations
            'data.append',       # Data processing
            'log.append',        # Logging
            'output.append',     # Output generation
            'f.write',          # File operations
            'print',            # Print statements
            'logger',           # Logging
            'debug',            # Debug statements
            'info',             # Info statements
            'warning',          # Warning statements
            'error',            # Error statements
        ]
        
        for pattern in false_positive_patterns:
            if pattern in line:
                return True
        
        # Check if it's a comment or string
        if line.strip().startswith('#') or '"""' in line or "'''" in line:
            return True
            
        return False
    
    def _is_safe_context(self, context: str) -> bool:
        """Check if the context is actually safe (main thread operations)"""
        # Safe patterns that indicate main thread operations
        safe_patterns = [
            'def __init__',  # Constructor
            'def setup_',     # Setup methods
            'def initialize', # Initialization
            'def create_',    # Creation methods
            'def handle_',    # Event handlers (usually main thread)
            'def show_',      # Show methods
            'def hide_',      # Hide methods
            'def close',      # Close methods
            'def cleanup',    # Cleanup methods
            'QTimer.singleShot',  # Safe threading
            'QMetaObject.invokeMethod',  # Safe threading
            'safe_ui_update',  # Safe threading utility
            'QueuedConnection',  # Safe connection
            'Qt.ConnectionType.QueuedConnection',  # Safe connection
            'self.main_window',  # Main window operations
            'self.ui_manager',   # UI manager operations
            'self.chat_tab',     # Chat tab operations
            'logger.',           # Logging operations
            'print(',            # Print statements
            'return',            # Return statements
            'pass',              # Pass statements
            'continue',          # Continue statements
            'break',             # Break statements
            'if ',               # If statements
            'elif ',             # Elif statements
            'else:',             # Else statements
            'try:',              # Try blocks
            'except',            # Except blocks
            'finally:',          # Finally blocks
            'with ',             # With statements
            'class ',            # Class definitions
            'import ',           # Import statements
            'from ',             # From statements
            '#',                 # Comments
            '"""',               # Docstrings
            "'''",               # Docstrings
        ]
        
        for pattern in safe_patterns:
            if pattern in context:
                return True
                
        return False
    
    def _is_qthread_start_call(self, line: str, lines: List[str], line_index: int) -> bool:
        """Check if this is actually a QThread start call, not threading.Thread"""
        # Skip if it's a comment
        if line.strip().startswith('#'):
            return False
        
        # Look for threading.Thread in previous lines
        prev_lines = lines[max(0, line_index-10):line_index]
        for prev_line in prev_lines:
            if 'threading.Thread' in prev_line:
                return False
        
        # Check if it's actually a QThread object
        return ('QThread' in line or 'thread' in line) and not 'threading.Thread' in line
    
    def _is_qthread_instantiation(self, line: str, lines: List[str], line_index: int) -> bool:
        """Check if this is actually a QThread instantiation, not a method call"""
        # Skip if it's a comment
        if line.strip().startswith('#'):
            return False
        
        # Skip if it's a method call (has parentheses but not instantiation)
        if '(' in line and not any(pattern in line for pattern in ['QThread(', 'QRunnable(', 'worker(']):
            return False
        
        # Look for actual instantiation patterns
        return any(pattern in line for pattern in ['QThread(', 'QRunnable(', 'worker('])
    
    def _is_qthread_run_call(self, line: str, lines: List[str], line_index: int) -> bool:
        """Check if this is actually a QThread run call, not a method definition"""
        # Skip if it's a comment or method definition
        if line.strip().startswith('#') or 'def run' in line:
            return False
        
        # Check if it's actually calling .run() on a QThread object
        return '.run()' in line and ('QThread' in line or 'worker' in line)
    
    def analyze_codebase(self, root_dir: str = None) -> Dict[str, Any]:
        """Analyze the pyside_chat app directory for thread safety issues"""
        if not root_dir:
            root_dir = project_root
        
        # Focus only on the pyside_chat app directory
        app_dir = os.path.join(root_dir, 'pyside_chat')
        if not os.path.exists(app_dir):
            logger.error(f"pyside_chat directory not found at: {app_dir}")
            return {
                'files_analyzed': 0,
                'potential_issues': [],
                'safe_patterns_found': [],
                'unsafe_patterns_found': [],
                'ui_method_calls': [],
                'threading_usage': [],
                'qthread_misuse': []
            }
        
        logger.info("Starting thread safety analysis of pyside_chat app...")
        
        # Find all Python files in pyside_chat directory only
        python_files = []
        ignore_dirs = {'.git', '__pycache__', 'venv', 'env', '.env', 'chat_env', '.venv', '.tox', '.mypy_cache', '.pytest_cache', '.idea', '.vscode', 'build', 'dist', 'node_modules'}
        for root, dirs, files in os.walk(app_dir):
            # Skip certain directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        logger.info(f"Found {len(python_files)} Python files to analyze")
        
        # Analyze each file
        results = {
            'files_analyzed': 0,
            'potential_issues': [],
            'safe_patterns_found': [],
            'unsafe_patterns_found': [],
            'ui_method_calls': [],
            'threading_usage': [],
            'qthread_misuse': []  # AGGREGATE HERE
        }
        
        file_iter = tqdm(python_files, desc="Analyzing files") if tqdm else python_files
        for file_path in file_iter:
            try:
                file_results = self._analyze_file(file_path)
                results['files_analyzed'] += 1
                
                # Merge results
                results['potential_issues'].extend(file_results.get('potential_issues', []))
                results['safe_patterns_found'].extend(file_results.get('safe_patterns_found', []))
                results['unsafe_patterns_found'].extend(file_results.get('unsafe_patterns_found', []))
                results['ui_method_calls'].extend(file_results.get('ui_method_calls', []))
                results['threading_usage'].extend(file_results.get('threading_usage', []))
                results['qthread_misuse'].extend(file_results.get('qthread_misuse', []))  # AGGREGATE
                
            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")
        
        return results
    
    def _analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single Python file for thread safety issues"""
        results = {
            'file': file_path,
            'potential_issues': [],
            'safe_patterns_found': [],
            'unsafe_patterns_found': [],
            'ui_method_calls': [],
            'threading_usage': [],
            'qthread_misuse': []  # NEW
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Analyze each line
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Check for UI method calls - be more specific to avoid false positives
                for method in self.ui_methods:
                    # Look for actual UI method calls, not just any method with the same name
                    if (f'.{method}(' in line or f' {method}(' in line) and not self._is_false_positive(line, method):
                        results['ui_method_calls'].append({
                            'file': file_path,
                            'line': line_num,
                            'method': method,
                            'code': line
                        })
                
                # Check for safe patterns
                for pattern in self.safe_patterns:
                    if pattern in line:
                        results['safe_patterns_found'].append({
                            'file': file_path,
                            'line': line_num,
                            'pattern': pattern,
                            'code': line
                        })
                
                # Check for unsafe patterns
                for pattern in self.unsafe_patterns:
                    if pattern in line:
                        results['unsafe_patterns_found'].append({
                            'file': file_path,
                            'line': line_num,
                            'pattern': pattern,
                            'code': line
                        })
                
                # Check for threading usage
                threading_keywords = ['QThread', 'QRunnable', 'threading.Thread', 'moveToThread']
                for keyword in threading_keywords:
                    if keyword in line:
                        results['threading_usage'].append({
                            'file': file_path,
                            'line': line_num,
                            'keyword': keyword,
                            'code': line
                        })
                
                # Check for potential issues
                if any(keyword in line for keyword in ['processEvents', 'QApplication.processEvents']):
                    results['potential_issues'].append({
                        'file': file_path,
                        'line': line_num,
                        'issue': 'processEvents call detected',
                        'severity': 'high',
                        'code': line
                    })
                
                # Check for direct UI updates in worker threads - be more specific
                if any(method in line for method in self.ui_methods):
                    # Look for context that suggests background thread usage
                    context_lines = lines[max(0, line_num-5):line_num+5]
                    context = '\n'.join(context_lines)
                    
                    # Only flag if it's actually in a worker thread context
                    if any(indicator in context for indicator in ['QThread', 'QRunnable', 'worker', 'background']):
                        # Additional checks to avoid false positives
                        if not self._is_false_positive(line, method) and not self._is_safe_context(context):
                            results['potential_issues'].append({
                                'file': file_path,
                                'line': line_num,
                                'issue': 'UI method call in potential background thread context',
                                'severity': 'medium',
                                'code': line,
                                'context': context
                            })
            # --- QThread/QRunnable/worker misuse patterns ---
            # 1. .start() on QThread without .isRunning() guard
            for i, line in enumerate(lines):
                if ".start()" in line and self._is_qthread_start_call(line, lines, i):
                    # Look for .isRunning() in previous 5 lines
                    prev = '\n'.join(lines[max(0, i-5):i])
                    if ".isRunning()" not in prev and "is_alive()" not in prev:
                        results['qthread_misuse'].append({
                            'file': file_path,
                            'line': i+1,
                            'issue': 'QThread .start() without .isRunning() guard',
                            'code': line,
                            'context': prev
                        })
            # 2. Instantiation without .moveToThread()
            for i, line in enumerate(lines):
                if self._is_qthread_instantiation(line, lines, i):
                    # Look for .moveToThread in next 10 lines
                    next_lines = '\n'.join(lines[i+1:i+11])
                    if ".moveToThread" not in next_lines:
                        results['qthread_misuse'].append({
                            'file': file_path,
                            'line': i+1,
                            'issue': 'QThread/QRunnable/worker instantiated without .moveToThread()',
                            'code': line,
                            'context': next_lines
                        })
            # 3. .start() without .quit()/.wait() after
            for i, line in enumerate(lines):
                if ".start()" in line and self._is_qthread_start_call(line, lines, i):
                    # Look for .quit() and .wait() in next 10 lines
                    next_lines = '\n'.join(lines[i+1:i+11])
                    if ".quit()" not in next_lines or ".wait()" not in next_lines:
                        results['qthread_misuse'].append({
                            'file': file_path,
                            'line': i+1,
                            'issue': 'QThread .start() without .quit()/.wait() after',
                            'code': line,
                            'context': next_lines
                        })
            # 4. Direct .run() calls
            for i, line in enumerate(lines):
                if ".run()" in line and self._is_qthread_run_call(line, lines, i):
                    results['qthread_misuse'].append({
                        'file': file_path,
                        'line': i+1,
                        'issue': 'Direct .run() call on QThread/worker',
                        'code': line
                    })
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
        
        return results
    
    def generate_report(self, results: Dict[str, Any], output_file: str = None) -> str:
        """Generate a comprehensive thread safety report"""
        if not output_file:
            output_file = "Development_Tools/Reports/thread_safety_report.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("THREAD SAFETY ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Summary
            f.write("SUMMARY:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Files analyzed: {results['files_analyzed']}\n")
            f.write(f"Potential issues found: {len(results['potential_issues'])}\n")
            f.write(f"Safe patterns found: {len(results['safe_patterns_found'])}\n")
            f.write(f"Unsafe patterns found: {len(results['unsafe_patterns_found'])}\n")
            f.write(f"UI method calls found: {len(results['ui_method_calls'])}\n")
            f.write(f"Threading usage found: {len(results['threading_usage'])}\n")
            f.write(f"QThread misuse found: {len(results['qthread_misuse'])}\n\n")
            
            # Potential Issues
            if results['potential_issues']:
                f.write("POTENTIAL THREAD SAFETY ISSUES:\n")
                f.write("-" * 40 + "\n")
                for issue in results['potential_issues']:
                    f.write(f"File: {issue['file']}:{issue['line']}\n")
                    f.write(f"Issue: {issue['issue']}\n")
                    f.write(f"Severity: {issue['severity']}\n")
                    f.write(f"Code: {issue['code']}\n")
                    if 'context' in issue:
                        f.write(f"Context:\n{issue['context']}\n")
                    f.write("\n")
            
            # Safe Patterns
            if results['safe_patterns_found']:
                f.write("SAFE THREADING PATTERNS FOUND:\n")
                f.write("-" * 40 + "\n")
                for pattern in results['safe_patterns_found'][:10]:  # Show first 10
                    f.write(f"File: {pattern['file']}:{pattern['line']}\n")
                    f.write(f"Pattern: {pattern['pattern']}\n")
                    f.write(f"Code: {pattern['code']}\n\n")
            
            # Unsafe Patterns
            if results['unsafe_patterns_found']:
                f.write("UNSAFE THREADING PATTERNS FOUND:\n")
                f.write("-" * 40 + "\n")
                for pattern in results['unsafe_patterns_found']:
                    f.write(f"File: {pattern['file']}:{pattern['line']}\n")
                    f.write(f"Pattern: {pattern['pattern']}\n")
                    f.write(f"Code: {pattern['code']}\n\n")
            
            # UI Method Calls
            if results['ui_method_calls']:
                f.write("UI METHOD CALLS FOUND:\n")
                f.write("-" * 40 + "\n")
                for call in results['ui_method_calls'][:20]:  # Show first 20
                    f.write(f"File: {call['file']}:{call['line']}\n")
                    f.write(f"Method: {call['method']}\n")
                    f.write(f"Code: {call['code']}\n\n")
            
            # Threading Usage
            if results['threading_usage']:
                f.write("THREADING USAGE FOUND:\n")
                f.write("-" * 40 + "\n")
                for usage in results['threading_usage'][:15]:  # Show first 15
                    f.write(f"File: {usage['file']}:{usage['line']}\n")
                    f.write(f"Keyword: {usage['keyword']}\n")
                    f.write(f"Code: {usage['code']}\n\n")
            
            # QThread/QRunnable Misuse Patterns
            if 'qthread_misuse' in results and results['qthread_misuse']:
                f.write("QTHREAD/QRUNNABLE MISUSE PATTERNS:\n")
                f.write("-" * 40 + "\n")
                for misuse in results['qthread_misuse']:
                    f.write(f"File: {misuse['file']}:{misuse['line']}\n")
                    f.write(f"Issue: {misuse['issue']}\n")
                    f.write(f"Code: {misuse['code']}\n")
                    if 'context' in misuse:
                        f.write(f"Context:\n{misuse['context']}\n")
                    f.write("\n")
            
            # Recommendations
            f.write("RECOMMENDATIONS:\n")
            f.write("-" * 40 + "\n")
            f.write("1. Use QTimer.singleShot(0, callback) for UI updates from background threads\n")
            f.write("2. Use QMetaObject.invokeMethod with QueuedConnection for thread-safe calls\n")
            f.write("3. Avoid processEvents() calls in background threads\n")
            f.write("4. Use the existing safe_ui_update utility function\n")
            f.write("5. Ensure all UI updates go through the main thread\n")
            f.write("6. Use the existing StreamingUpdateTask for streaming UI updates\n")
            f.write("7. Follow the QThread vs QRunnable patterns established in the codebase\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("Report generated by Thread Safety Analyzer\n")
            f.write("=" * 80 + "\n")
        
        logger.info(f"Thread safety report generated: {output_file}")
        return output_file
    
    def create_safe_widget_wrapper(self, widget_class):
        """Create a thread-safe wrapper for a widget class"""
        class SafeWidget(widget_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._analyzer = ThreadSafetyAnalyzer()
            
            def __getattribute__(self, name):
                attr = super().__getattribute__(name)
                if name in self._analyzer.ui_methods and callable(attr):
                    return self._analyzer.ensure_main_thread(attr)
                return attr
        
        return SafeWidget


def main():
    """Main entry point for thread safety analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Thread Safety Analyzer")
    parser.add_argument("--output", default="Development_Tools/Reports/thread_safety_report.txt", help="Output report file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--analyze-file", help="Analyze specific file only")
    
    args = parser.parse_args()
    
    # Set the correct project root (go up from Development Tools/ThreadingAnalyser)
    global project_root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Go up two levels
    
    analyzer = ThreadSafetyAnalyzer()
    
    if args.analyze_file:
        # Analyze specific file
        if os.path.exists(args.analyze_file):
            results = analyzer._analyze_file(args.analyze_file)
            print(f"Analysis of {args.analyze_file}:")
            print(f"  Potential issues: {len(results['potential_issues'])}")
            print(f"  Safe patterns: {len(results['safe_patterns_found'])}")
            print(f"  UI method calls: {len(results['ui_method_calls'])}")
            print(f"  QThread misuse: {len(results['qthread_misuse'])}")
        else:
            print(f"File not found: {args.analyze_file}")
    else:
        # Analyze pyside_chat app only
        print("Starting thread safety analysis of pyside_chat app...")
        results = analyzer.analyze_codebase()
        
        # Generate report
        report_file = analyzer.generate_report(results, args.output)
        
        # Print summary
        print(f"\nAnalysis complete!")
        print(f"Files analyzed: {results['files_analyzed']}")
        print(f"Potential issues: {len(results['potential_issues'])}")
        print(f"Safe patterns: {len(results['safe_patterns_found'])}")
        print(f"Unsafe patterns: {len(results['unsafe_patterns_found'])}")
        print(f"UI method calls: {len(results['ui_method_calls'])}")
        print(f"Threading usage: {len(results['threading_usage'])}")
        print(f"QThread misuse: {len(results['qthread_misuse'])}")
        print(f"Report saved to: {report_file}")


if __name__ == "__main__":
    main() 