#!/usr/bin/env python3
"""
Enhanced Profiler Runner

This script runs the enhanced profiler to get detailed thread analysis
and identify where additional threads are coming from.
"""

import sys
import os
import time
import subprocess
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Tools.profiler import ApplicationProfiler


def run_enhanced_profiling(duration: int = 120):
    """Run enhanced profiling with detailed thread analysis"""
    
    print("=" * 80)
    print("ENHANCED APPLICATION PROFILER")
    print("=" * 80)
    print(f"Duration: {duration} seconds")
    print("This will provide detailed thread analysis to identify thread sources")
    print("-" * 80)
    
    # Create profiler
    profiler = ApplicationProfiler("detailed_analysis")
    
    # Start profiling
    print("Starting enhanced profiling...")
    profiler.start_profiling()
    
    try:
        # Wait for the specified duration
        print(f"Profiling for {duration} seconds...")
        print("Press Ctrl+C to stop early")
        
        for i in range(duration):
            time.sleep(1)
            if (i + 1) % 10 == 0:
                print(f"Profiling progress: {i + 1}/{duration} seconds")
                
    except KeyboardInterrupt:
        print("\nProfiling interrupted by user")
    
    # Stop profiling and generate reports
    print("Stopping profiling and generating reports...")
    profiler.stop_profiling()
    report_path = profiler.generate_report()
    
    print(f"\nProfiling completed!")
    print(f"Detailed report: {report_path}")
    print(f"Summary report: {report_path.replace('_detailed.json', '_summary.txt')}")
    
    # Display key findings
    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    
    try:
        import json
        with open(report_path, 'r') as f:
            data = json.load(f)
        
        # Thread analysis
        thread_analysis = data.get('thread_growth', {})
        if thread_analysis:
            print(f"Initial Thread Count: {thread_analysis.get('initial_thread_count', 0)}")
            print(f"Final Thread Count: {thread_analysis.get('final_thread_count', 0)}")
            print(f"Thread Growth: {thread_analysis.get('thread_growth', 0)}")
            print(f"Snapshots Taken: {thread_analysis.get('snapshots', 0)}")
        
        # Current thread details
        thread_details = data.get('thread_analysis', {})
        if thread_details:
            summary = thread_details.get('summary', {})
            print(f"\nCurrent Thread Breakdown:")
            print(f"  Python Threads: {summary.get('python_threads', 0)}")
            print(f"  Qt Threads: {summary.get('qt_threads', 0)}")
            print(f"  System Threads: {summary.get('system_threads', 0)}")
            
            # Detailed thread information
            categories = thread_details.get('categories', {})
            if categories:
                python_threads = categories.get('python_threads', [])
                if python_threads:
                    print(f"\nPython Threads:")
                    for thread in python_threads:
                        print(f"  - {thread['name']} (daemon: {thread['daemon']}, alive: {thread['alive']})")
                
                qt_threads = categories.get('qt_threads', [])
                if qt_threads:
                    print(f"\nQt Threads:")
                    for thread in qt_threads:
                        print(f"  - {thread['name']} (main: {thread.get('is_main', False)}, running: {thread.get('is_running', False)})")
        
        # Performance summary
        performance = data.get('performance_summary', {})
        if performance:
            thread_stats = performance.get('threads', {})
            if thread_stats:
                print(f"\nThread Statistics:")
                print(f"  Average Thread Count: {thread_stats.get('mean', 0):.1f}")
                print(f"  Maximum Thread Count: {thread_stats.get('max', 0)}")
                print(f"  Minimum Thread Count: {thread_stats.get('min', 0)}")
        
    except Exception as e:
        print(f"Error reading report: {e}")
    
    print("\n" + "=" * 80)
    print("Check the generated reports for detailed analysis")
    print("=" * 80)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Application Profiler")
    parser.add_argument("--duration", type=int, default=120, help="Profiling duration in seconds")
    parser.add_argument("--quick", action="store_true", help="Quick profiling (30 seconds)")
    
    args = parser.parse_args()
    
    duration = 30 if args.quick else args.duration
    
    run_enhanced_profiling(duration)


if __name__ == "__main__":
    main() 