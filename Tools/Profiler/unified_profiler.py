#!/usr/bin/env python3
"""
Unified Application Profiler

Launches the main application, profiles system/process/thread/function performance, and generates comprehensive reports.
"""

import sys
import os
import time
import subprocess
import threading
import signal
import argparse
from pathlib import Path

# Add the project root to the path so we can import from Tools
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import helpers
try:
    from Development_Tools.Profiler.profiler_helpers import SystemProfiler, ProcessProfiler, ThreadProfiler, FunctionProfiler, generate_reports
except ImportError as e:
    print(f"Error importing profiler helpers: {e}")
    print("Make sure profiler_helpers.py is in the Tools directory")
    sys.exit(1)


def launch_application(entry_point="main.py"):
    """Launch the main application as a subprocess."""
    print(f"Launching application: {entry_point}")
    try:
        process = subprocess.Popen(
            [sys.executable, entry_point],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        print(f"Application started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Error launching application: {e}")
        return None


def unified_profile(
    output_dir="profiling_reports",
    entry_point="main.py",
    detail_level="full"
):
    """Run unified profiling for the entire app lifecycle."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    print("=" * 80)
    print("UNIFIED APPLICATION PROFILER")
    print("=" * 80)
    print(f"Entry point: {entry_point}")
    print(f"Output directory: {output_dir}")
    print(f"Detail level: {detail_level}")
    print("Profiling will run for the entire app lifetime")
    print("-" * 80)

    # Initialize profilers
    system_profiler = SystemProfiler(interval=1.0)
    thread_profiler = ThreadProfiler(interval=2.0)
    function_profiler = FunctionProfiler()
    process_profiler = ProcessProfiler()

    # Launch the app
    app_process = launch_application(entry_point)
    if not app_process:
        print("Failed to launch application. Exiting.")
        return False

    # Start profiling
    print("Starting profilers...")
    system_profiler.start()
    thread_profiler.start()
    function_profiler.start()
    
    # Start process monitoring with the app's PID
    process_profiler.start(target_pid=app_process.pid)

    print("Profiling started. Waiting for application to exit...")
    try:
        # Wait until app exits naturally
        app_process.wait()
        print("Application exited.")
    except KeyboardInterrupt:
        print("\nProfiling interrupted by user. Stopping app...")
        app_process.terminate()
        try:
            app_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("Force killing application...")
            app_process.kill()
            app_process.wait(timeout=5)
    except Exception as e:
        print(f"Error during profiling: {e}")
        app_process.terminate()
    finally:
        print("Stopping profilers...")
        system_profiler.stop()
        thread_profiler.stop()
        function_profiler.stop()
        process_profiler.stop()
        
        # Generate reports
        print("Generating reports...")
        generate_reports(system_profiler, process_profiler, thread_profiler, function_profiler, output_dir)

    print("Profiling complete. Check the output directory for reports.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Unified Application Profiler")
    parser.add_argument("--output-dir", default="profiling_reports", help="Output directory for reports")
    parser.add_argument("--entry-point", default="main.py", help="Application entry point (default: main.py)")
    parser.add_argument("--detail-level", default="full", choices=["full", "basic"], help="Profiling detail level")
    args = parser.parse_args()

    success = unified_profile(
        output_dir=args.output_dir,
        entry_point=args.entry_point,
        detail_level=args.detail_level
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 