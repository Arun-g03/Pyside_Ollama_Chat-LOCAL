"""
Thread Safety Auditor for PySide6 Chat Application

This module provides comprehensive thread safety analysis and reporting.
"""

import os
import sys
import threading
import traceback
from typing import Dict, List, Any, Optional
from pathlib import Path

from PySide6.QtCore import QThread, QApplication, QTimer
from PySide6.QtWidgets import QWidget

from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ThreadSafetyAuditor:
    """
    Comprehensive thread safety auditor for PySide6 applications.
    
    This auditor analyzes the current state of threads, detects potential
    cross-thread UI operations, and provides recommendations for fixes.
    """
    
    def __init__(self):
        self.thread_info = {}
        self.cross_thread_operations = []
        self.thread_safety_issues = []
        self.recommendations = []
        self.analysis_complete = False
        
    def analyze_current_threads(self):
        """Analyze all currently active threads"""
        try:
            active_threads = threading.enumerate()
            logger.info(f"Analyzing {len(active_threads)} active threads")
            
            # Categorize threads
            main_thread = None
            qt_threads = []
            worker_threads = []
            voice_threads = []
            audio_threads = []
            other_threads = []
            
            for thread in active_threads:
                thread_name = thread.name.lower()
                thread_info = {
                    'name': thread.name,
                    'ident': thread.ident,
                    'daemon': thread.daemon,
                    'alive': thread.is_alive(),
                    'type': 'unknown'
                }
                
                if 'voice' in thread_name or 'audio' in thread_name:
                    voice_threads.append(thread_info)
                    thread_info['type'] = 'voice'
                elif 'audio' in thread_name or 'pyaudio' in thread_name:
                    audio_threads.append(thread_info)
                    thread_info['type'] = 'audio'
                elif 'worker' in thread_name or 'dummy' in thread_name:
                    worker_threads.append(thread_info)
                    thread_info['type'] = 'worker'
                else:
                    other_threads.append(thread_info)
                    thread_info['type'] = 'other'
                
                self.thread_info[thread.ident] = thread_info
            
            # Log thread analysis
            logger.info(f"Thread analysis complete:")
            logger.info(f"  Main thread: {len([t for t in active_threads if t.name == 'MainThread'])}")
            logger.info(f"  Qt threads: {len(qt_threads)}")
            logger.info(f"  Worker threads: {len(worker_threads)}")
            logger.info(f"  Voice threads: {len(voice_threads)}")
            logger.info(f"  Audio threads: {len(audio_threads)}")
            logger.info(f"  Other threads: {len(other_threads)}")
            
        except Exception as e:
            logger.error(f"Error analyzing threads: {e}")
    
    def detect_cross_thread_ui_operations(self):
        """Detect potential cross-thread UI operations"""
        try:
            # Check for potential cross-thread UI updates
            main_thread = QApplication.instance().thread() if QApplication.instance() else None
            
            if main_thread:
                # Check if any non-main threads are trying to update UI
                for thread_id, thread_info in self.thread_info.items():
                    if thread_info['type'] in ['voice', 'audio', 'worker']:
                        # This is a potential cross-thread operation
                        self.cross_thread_operations.append({
                            'thread_id': thread_id,
                            'thread_name': thread_info['name'],
                            'thread_type': thread_info['type'],
                            'description': f"Worker thread {thread_info['name']} may perform UI operations"
                        })
            
            logger.info(f"Detected {len(self.cross_thread_operations)} potential cross-thread operations")
            
        except Exception as e:
            logger.error(f"Error detecting cross-thread operations: {e}")
    
    def check_thread_safety_patterns(self):
        """Check for common thread safety patterns and issues"""
        try:
            # Check for excessive threads
            thread_breakdown = self._get_thread_breakdown()
            if thread_breakdown.get('audio', 0) > 3:
                self.thread_safety_issues.append({
                    'type': 'excessive_audio_threads',
                    'description': f"Too many audio threads: {thread_breakdown.get('audio', 0)}",
                    'severity': 'warning'
                })
            
            if thread_breakdown.get('worker', 0) > 10:
                self.thread_safety_issues.append({
                    'type': 'excessive_worker_threads',
                    'description': f"Too many worker threads: {thread_breakdown.get('worker', 0)}",
                    'severity': 'warning'
                })
            
            # Check for main thread issues
            main_thread_count = len([t for t in self.thread_info.values() if t['name'] == 'MainThread'])
            if main_thread_count != 1:
                self.thread_safety_issues.append({
                    'type': 'main_thread_issue',
                    'description': f"Expected 1 main thread, found {main_thread_count}",
                    'severity': 'error'
                })
            
            logger.info(f"Found {len(self.thread_safety_issues)} thread safety issues")
            
        except Exception as e:
            logger.error(f"Error checking thread safety patterns: {e}")
    
    def _get_thread_breakdown(self) -> Dict[str, int]:
        """Get breakdown of threads by type"""
        breakdown = {}
        for thread_info in self.thread_info.values():
            thread_type = thread_info['type']
            breakdown[thread_type] = breakdown.get(thread_type, 0) + 1
        return breakdown
    
    def generate_recommendations(self):
        """Generate recommendations for thread safety improvements"""
        try:
            recommendations = []
            
            # Check for excessive threads
            thread_breakdown = self._get_thread_breakdown()
            if thread_breakdown.get('audio', 0) > 3:
                recommendations.append("Consider reducing the number of audio threads")
            
            if thread_breakdown.get('worker', 0) > 10:
                recommendations.append("Consider using a thread pool for worker threads")
            
            # Check for signal connection issues
            for issue in self.thread_safety_issues:
                if issue['type'] == 'excessive_signal_receivers':
                    recommendations.append("Review signal connections to avoid duplicates")
            
            # General recommendations
            recommendations.extend([
                "Use QTimer.singleShot(0, callback) for UI updates from background threads",
                "Use QMetaObject.invokeMethod with QueuedConnection for thread-safe calls",
                "Avoid processEvents() calls in background threads",
                "Use the existing safe_ui_update utility function",
                "Ensure all UI updates go through the main thread",
                "Use the existing StreamingUpdateTask for streaming UI updates",
                "Follow the QThread vs QRunnable patterns established in the codebase"
            ])
            
            self.recommendations = recommendations
            logger.info(f"Generated {len(recommendations)} recommendations")
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
    
    def run_full_analysis(self):
        """Run a complete thread safety analysis"""
        try:
            logger.info("Starting comprehensive thread safety analysis")
            
            self.analyze_current_threads()
            self.detect_cross_thread_ui_operations()
            self.check_thread_safety_patterns()
            self.generate_recommendations()
            
            self.analysis_complete = True
            logger.info("Thread safety analysis complete")
            
        except Exception as e:
            logger.error(f"Error in full analysis: {e}")
    
    def generate_report(self) -> str:
        """Generate a comprehensive thread safety report"""
        if not self.analysis_complete:
            self.run_full_analysis()
        
        report = []
        report.append("=" * 80)
        report.append("THREAD SAFETY ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Thread Summary
        report.append("THREAD SUMMARY:")
        report.append("-" * 40)
        thread_breakdown = self._get_thread_breakdown()
        for thread_type, count in thread_breakdown.items():
            report.append(f"  {thread_type.capitalize()}: {count}")
        report.append("")
        
        # Cross-thread Operations
        if self.cross_thread_operations:
            report.append("POTENTIAL CROSS-THREAD OPERATIONS:")
            report.append("-" * 40)
            for op in self.cross_thread_operations:
                report.append(f"  Thread: {op['thread_name']} ({op['thread_type']})")
                report.append(f"  Description: {op['description']}")
                report.append("")
        else:
            report.append("No potential cross-thread operations detected")
            report.append("")
        
        # Thread Safety Issues
        if self.thread_safety_issues:
            report.append("THREAD SAFETY ISSUES:")
            report.append("-" * 40)
            for issue in self.thread_safety_issues:
                report.append(f"  [{issue['severity'].upper()}] {issue['description']}")
            report.append("")
        else:
            report.append("No thread safety issues detected")
            report.append("")
        
        # Recommendations
        if self.recommendations:
            report.append("RECOMMENDATIONS:")
            report.append("-" * 40)
            for i, rec in enumerate(self.recommendations, 1):
                report.append(f"  {i}. {rec}")
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, filepath: str):
        """Save the thread safety report to a file"""
        try:
            report = self.generate_report()
            with open(filepath, 'w') as f:
                f.write(report)
            logger.info(f"Thread safety report saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")


def run_thread_safety_audit() -> ThreadSafetyAuditor:
    """
    Run a complete thread safety audit and return the auditor instance.
    
    Returns:
        ThreadSafetyAuditor: The auditor instance with analysis results
    """
    auditor = ThreadSafetyAuditor()
    auditor.run_full_analysis()
    return auditor


def quick_thread_check() -> Dict[str, Any]:
    """
    Perform a quick thread safety check.
    
    Returns:
        Dict containing basic thread safety information
    """
    try:
        active_threads = threading.enumerate()
        main_thread_count = len([t for t in active_threads if t.name == 'MainThread'])
        worker_thread_count = len([t for t in active_threads if 'worker' in t.name.lower()])
        voice_thread_count = len([t for t in active_threads if 'voice' in t.name.lower()])
        
        return {
            'total_threads': len(active_threads),
            'main_threads': main_thread_count,
            'worker_threads': worker_thread_count,
            'voice_threads': voice_thread_count,
            'has_qt_app': QApplication.instance() is not None,
            'main_thread_ok': main_thread_count == 1,
            'excessive_workers': worker_thread_count > 10,
            'excessive_voice': voice_thread_count > 3
        }
    except Exception as e:
        logger.error(f"Error in quick thread check: {e}")
        return {'error': str(e)}


if __name__ == "__main__":
    # Run the audit when executed directly
    auditor = run_thread_safety_audit()
    print(auditor.generate_report()) 