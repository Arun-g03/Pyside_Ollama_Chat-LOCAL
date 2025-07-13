#!/usr/bin/env python3
"""
Profiler Launcher - Runs the profiler alongside the main application

This script launches the main application and runs the profiler in parallel
to collect detailed thread analysis and performance data.
"""

import sys
import os
import time
import threading
import subprocess
import signal
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Tools.profiler import ApplicationProfiler


class ProfilerLauncher:
    """Launcher that runs the profiler alongside the main application"""
    
    def __init__(self, output_dir: str = "profiling_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.profiler = ApplicationProfiler(str(self.output_dir))
        self.app_process = None
        self.profiler_thread = None
        self.running = False
        
    def start_profiling(self):
        """Start the profiler in a separate thread"""
        self.profiler.start_profiling()
        self.running = True
        
        # Start profiler monitoring in a separate thread
        self.profiler_thread = threading.Thread(target=self._profiler_monitor_loop, daemon=True)
        self.profiler_thread.start()
        
        print("Profiler started in background")
        
    def _profiler_monitor_loop(self):
        """Monitor loop for the profiler"""
        while self.running:
            try:
                time.sleep(1)
            except Exception as e:
                print(f"Error in profiler monitor loop: {e}")
                break
    
    def launch_application(self):
        """Launch the main application"""
        try:
            print("Launching main application...")
            
            # Launch the main application
            self.app_process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            print(f"Application started with PID: {self.app_process.pid}")
            return True
            
        except Exception as e:
            print(f"Error launching application: {e}")
            return False
    
    def wait_for_application(self, timeout: int = 300):
        """Wait for the application to complete or timeout"""
        try:
            print(f"Waiting for application (timeout: {timeout}s)...")
            
            # Wait for the process to complete
            self.app_process.wait(timeout=timeout)
            print("Application completed")
            return True
            
        except subprocess.TimeoutExpired:
            print(f"Application timeout after {timeout} seconds")
            return False
        except Exception as e:
            print(f"Error waiting for application: {e}")
            return False
    
    def stop_profiling(self):
        """Stop profiling and generate reports"""
        self.running = False
        
        if self.profiler_thread:
            self.profiler_thread.join(timeout=5)
        
        self.profiler.stop_profiling()
        report_path = self.profiler.generate_report()
        
        print(f"Profiling completed. Report saved to: {report_path}")
        return report_path
    
    def cleanup(self):
        """Clean up resources"""
        if self.app_process and self.app_process.poll() is None:
            print("Terminating application process...")
            self.app_process.terminate()
            try:
                self.app_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("Force killing application process...")
                self.app_process.kill()
                self.app_process.wait(timeout=5)
    
    def run(self, duration: int = 60):
        """Run the profiler with the application"""
        try:
            print("=" * 60)
            print("PROFILER LAUNCHER")
            print("=" * 60)
            print(f"Duration: {duration} seconds")
            print(f"Output directory: {self.output_dir}")
            print("-" * 60)
            
            # Start the profiler
            self.start_profiling()
            
            # Launch the application
            if not self.launch_application():
                print("Failed to launch application")
                return False
            
            # Wait for the specified duration or until app exits
            start_time = time.time()
            while time.time() - start_time < duration:
                if self.app_process.poll() is not None:
                    print("Application exited early")
                    break
                time.sleep(1)
            
            # Stop profiling and generate reports
            report_path = self.stop_profiling()
            
            print(f"Profiling session completed")
            print(f"Report: {report_path}")
            
            return True
            
        except KeyboardInterrupt:
            print("\nProfiling interrupted by user")
            self.cleanup()
            self.stop_profiling()
            return False
        except Exception as e:
            print(f"Error during profiling: {e}")
            import traceback
            traceback.print_exc()
            self.cleanup()
            return False
        finally:
            self.cleanup()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Profiler Launcher")
    parser.add_argument("--duration", type=int, default=60, help="Profiling duration in seconds")
    parser.add_argument("--output-dir", default="profiling_reports", help="Output directory for reports")
    parser.add_argument("--continuous", action="store_true", help="Run until interrupted")
    
    args = parser.parse_args()
    
    launcher = ProfilerLauncher(args.output_dir)
    
    if args.continuous:
        print("Starting continuous profiling (press Ctrl+C to stop)...")
        launcher.start_profiling()
        launcher.launch_application()
        
        try:
            while True:
                time.sleep(1)
                if launcher.app_process and launcher.app_process.poll() is not None:
                    print("Application exited, stopping profiler...")
                    break
        except KeyboardInterrupt:
            print("\nStopping continuous profiling...")
        finally:
            launcher.stop_profiling()
            launcher.cleanup()
    else:
        launcher.run(args.duration)


if __name__ == "__main__":
    main() 