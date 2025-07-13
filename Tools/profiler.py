#!/usr/bin/env python3
"""
Application Profiler Tool

A comprehensive profiling tool for the PySide Ollama Chat application.
Profiles CPU usage, memory consumption, system resources, and application performance.
Enhanced with detailed thread analysis and QThread monitoring.
"""

import sys
import os
import time
import psutil
import threading
import json
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import traceback

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer, QThread, Signal, QObject
    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False
    print("Warning: PySide6 not available, Qt profiling disabled")

try:
    import cProfile
    import pstats
    import io
    PROFILE_AVAILABLE = True
except ImportError:
    PROFILE_AVAILABLE = False
    print("Warning: cProfile not available, detailed profiling disabled")


class ThreadAnalyzer:
    """Analyze thread usage and identify thread sources"""
    
    def __init__(self):
        self.thread_snapshots = []
        self.qt_threads = []
        self.python_threads = []
        
    def capture_thread_snapshot(self):
        """Capture current thread state"""
        try:
            current_process = psutil.Process()
            threads = current_process.threads()
            
            # Get Python threads
            python_threads = []
            for thread in threading.enumerate():
                thread_info = {
                    'name': thread.name,
                    'ident': thread.ident,
                    'daemon': thread.daemon,
                    'alive': thread.is_alive(),
                    'type': 'python_thread'
                }
                python_threads.append(thread_info)
            
            # Get Qt threads if available
            qt_threads = []
            if QT_AVAILABLE:
                try:
                    app = QApplication.instance()
                    if app:
                        # Get all QThread objects
                        qt_threads = self._get_qt_threads()
                except Exception as e:
                    print(f"Error getting Qt threads: {e}")
            
            snapshot = {
                'timestamp': time.time(),
                'total_threads': len(threads),
                'python_threads': python_threads,
                'qt_threads': qt_threads,
                'system_threads': threads
            }
            
            self.thread_snapshots.append(snapshot)
            return snapshot
            
        except Exception as e:
            print(f"Error capturing thread snapshot: {e}")
            return None
    
    def _get_qt_threads(self):
        """Get information about Qt threads"""
        qt_threads = []
        try:
            # Get main thread
            main_thread = QThread.currentThread()
            qt_threads.append({
                'name': main_thread.objectName() or 'MainThread',
                'type': 'QThread',
                'is_main': True,
                'is_running': main_thread.isRunning(),
                'priority': main_thread.priority()
            })
            
            # Try to get other QThread instances
            # This is limited by Qt's design, but we can try to track them
            # through our application's thread management
            
        except Exception as e:
            print(f"Error getting Qt thread details: {e}")
        
        return qt_threads
    
    def analyze_thread_growth(self):
        """Analyze thread count changes over time"""
        if len(self.thread_snapshots) < 2:
            return {}
        
        analysis = {
            'initial_thread_count': self.thread_snapshots[0]['total_threads'],
            'final_thread_count': self.thread_snapshots[-1]['total_threads'],
            'thread_growth': self.thread_snapshots[-1]['total_threads'] - self.thread_snapshots[0]['total_threads'],
            'snapshots': len(self.thread_snapshots),
            'thread_history': []
        }
        
        for i, snapshot in enumerate(self.thread_snapshots):
            analysis['thread_history'].append({
                'snapshot': i,
                'timestamp': snapshot['timestamp'],
                'total_threads': snapshot['total_threads'],
                'python_threads': len(snapshot['python_threads']),
                'qt_threads': len(snapshot['qt_threads'])
            })
        
        return analysis
    
    def get_thread_details(self):
        """Get detailed information about current threads"""
        if not self.thread_snapshots:
            return {}
        
        latest = self.thread_snapshots[-1]
        
        # Categorize threads by type
        thread_categories = {
            'python_threads': [],
            'qt_threads': [],
            'system_threads': [],
            'unknown_threads': []
        }
        
        # Python threads
        for thread in latest['python_threads']:
            thread_categories['python_threads'].append({
                'name': thread['name'],
                'daemon': thread['daemon'],
                'alive': thread['alive'],
                'type': 'python'
            })
        
        # Qt threads
        for thread in latest['qt_threads']:
            thread_categories['qt_threads'].append({
                'name': thread['name'],
                'is_main': thread.get('is_main', False),
                'is_running': thread.get('is_running', False),
                'type': 'qt'
            })
        
        # System threads (from psutil)
        for thread in latest['system_threads']:
            thread_categories['system_threads'].append({
                'id': thread.id,
                'user_time': thread.user_time,
                'system_time': thread.system_time,
                'type': 'system'
            })
        
        return {
            'total_threads': latest['total_threads'],
            'categories': thread_categories,
            'summary': {
                'python_threads': len(thread_categories['python_threads']),
                'qt_threads': len(thread_categories['qt_threads']),
                'system_threads': len(thread_categories['system_threads'])
            }
        }


class SystemMonitor(QObject):
    """Monitor system resources during application execution"""
    
    # Signals for real-time monitoring
    cpu_usage_updated = Signal(float)
    memory_usage_updated = Signal(float)
    disk_io_updated = Signal(dict)
    network_io_updated = Signal(dict)
    thread_count_updated = Signal(int)
    
    def __init__(self, interval: float = 1.0):
        super().__init__()
        self.interval = interval
        self.monitoring = False
        self.monitor_thread = None
        self.data_points = []
        self.thread_analyzer = ThreadAnalyzer()
        
        # Get initial system info
        self.cpu_count = psutil.cpu_count()
        self.memory_total = psutil.virtual_memory().total
        
        # Network and disk counters
        self.network_initial = psutil.net_io_counters()
        self.disk_initial = psutil.disk_io_counters()
        
    def start_monitoring(self):
        """Start system resource monitoring"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"System monitoring started (interval: {self.interval}s)")
        
    def stop_monitoring(self):
        """Stop system resource monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("System monitoring stopped")
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                timestamp = time.time()
                
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=0.1)
                
                # Memory usage
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                memory_used = memory.used
                memory_available = memory.available
                
                # Disk I/O
                disk_io = psutil.disk_io_counters()
                disk_read_bytes = disk_io.read_bytes - self.disk_initial.read_bytes
                disk_write_bytes = disk_io.write_bytes - self.disk_initial.write_bytes
                
                # Network I/O
                network_io = psutil.net_io_counters()
                network_bytes_sent = network_io.bytes_sent - self.network_initial.bytes_sent
                network_bytes_recv = network_io.bytes_recv - self.network_initial.bytes_recv
                
                # Process-specific info
                current_process = psutil.Process()
                process_cpu_percent = current_process.cpu_percent()
                process_memory_info = current_process.memory_info()
                
                # Thread analysis
                thread_snapshot = self.thread_analyzer.capture_thread_snapshot()
                thread_count = thread_snapshot['total_threads'] if thread_snapshot else 0
                
                data_point = {
                    'timestamp': timestamp,
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'memory_used': memory_used,
                    'memory_available': memory_available,
                    'disk_read_bytes': disk_read_bytes,
                    'disk_write_bytes': disk_write_bytes,
                    'network_bytes_sent': network_bytes_sent,
                    'network_bytes_recv': network_bytes_recv,
                    'process_cpu_percent': process_cpu_percent,
                    'process_memory_rss': process_memory_info.rss,
                    'process_memory_vms': process_memory_info.vms,
                    'thread_count': thread_count
                }
                
                self.data_points.append(data_point)
                
                # Emit signals for real-time monitoring
                self.cpu_usage_updated.emit(cpu_percent)
                self.memory_usage_updated.emit(memory_percent)
                self.disk_io_updated.emit({
                    'read_bytes': disk_read_bytes,
                    'write_bytes': disk_write_bytes
                })
                self.network_io_updated.emit({
                    'bytes_sent': network_bytes_sent,
                    'bytes_recv': network_bytes_recv
                })
                self.thread_count_updated.emit(thread_count)
                
                time.sleep(self.interval)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(self.interval)
                
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics from collected data"""
        if not self.data_points:
            return {}
            
        cpu_values = [dp['cpu_percent'] for dp in self.data_points]
        memory_values = [dp['memory_percent'] for dp in self.data_points]
        process_cpu_values = [dp['process_cpu_percent'] for dp in self.data_points]
        process_memory_values = [dp['process_memory_rss'] for dp in self.data_points]
        thread_values = [dp['thread_count'] for dp in self.data_points]
        
        # Thread analysis
        thread_analysis = self.thread_analyzer.analyze_thread_growth()
        thread_details = self.thread_analyzer.get_thread_details()
        
        return {
            'monitoring_duration': self.data_points[-1]['timestamp'] - self.data_points[0]['timestamp'],
            'data_points_count': len(self.data_points),
            'cpu': {
                'mean': sum(cpu_values) / len(cpu_values),
                'max': max(cpu_values),
                'min': min(cpu_values)
            },
            'memory': {
                'mean': sum(memory_values) / len(memory_values),
                'max': max(memory_values),
                'min': min(memory_values)
            },
            'process_cpu': {
                'mean': sum(process_cpu_values) / len(process_cpu_values),
                'max': max(process_cpu_values),
                'min': min(process_cpu_values)
            },
            'process_memory': {
                'mean': sum(process_memory_values) / len(process_memory_values),
                'max': max(process_memory_values),
                'min': min(process_memory_values)
            },
            'threads': {
                'mean': sum(thread_values) / len(thread_values),
                'max': max(thread_values),
                'min': min(thread_values),
                'growth_analysis': thread_analysis,
                'current_details': thread_details
            }
        }


class ApplicationProfiler:
    """Main application profiler"""
    
    def __init__(self, output_dir: str = "profiling_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.system_monitor = SystemMonitor()
        self.profiler = None
        self.stats = None
        self.start_time = None
        self.end_time = None
        
        # Application process info
        self.app_process = None
        self.child_processes = []
        
    def start_profiling(self):
        """Start profiling the application"""
        self.start_time = time.time()
        
        # Start system monitoring
        self.system_monitor.start_monitoring()
        
        # Start cProfile if available
        if PROFILE_AVAILABLE:
            self.profiler = cProfile.Profile()
            self.profiler.enable()
            print("Detailed function profiling started")
        
        print("Application profiling started")
        
    def stop_profiling(self):
        """Stop profiling and collect results"""
        self.end_time = time.time()
        
        # Stop system monitoring
        self.system_monitor.stop_monitoring()
        
        # Stop cProfile if active
        if self.profiler:
            self.profiler.disable()
            self.stats = pstats.Stats(self.profiler)
            print("Detailed function profiling stopped")
        
        print("Application profiling stopped")
        
    def collect_process_info(self):
        """Collect detailed process information"""
        try:
            current_process = psutil.Process()
            
            # Get process info
            self.app_process = {
                'pid': current_process.pid,
                'name': current_process.name(),
                'status': current_process.status(),
                'create_time': current_process.create_time(),
                'cpu_percent': current_process.cpu_percent(),
                'memory_info': current_process.memory_info()._asdict(),
                'num_threads': current_process.num_threads(),
                'connections': len(current_process.connections()),
                'open_files': len(current_process.open_files()),
                'environ': dict(current_process.environ())
            }
            
            # Get child processes
            children = current_process.children(recursive=True)
            for child in children:
                child_info = {
                    'pid': child.pid,
                    'name': child.name(),
                    'status': child.status(),
                    'cpu_percent': child.cpu_percent(),
                    'memory_info': child.memory_info()._asdict(),
                    'num_threads': child.num_threads()
                }
                self.child_processes.append(child_info)
                
        except Exception as e:
            print(f"Error collecting process info: {e}")
            
    def collect_system_info(self) -> Dict[str, Any]:
        """Collect system information"""
        try:
            # CPU info
            cpu_info = {
                'count': psutil.cpu_count(),
                'count_logical': psutil.cpu_count(logical=True),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                'usage_per_core': psutil.cpu_percent(interval=1, percpu=True)
            }
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_info = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percent': memory.percent,
                'swap': psutil.swap_memory()._asdict()
            }
            
            # Disk info
            disk_info = {
                'partitions': [p._asdict() for p in psutil.disk_partitions()],
                'usage': psutil.disk_usage('/')._asdict(),
                'io_counters': psutil.disk_io_counters()._asdict()
            }
            
            # Network info
            network_info = {
                'interfaces': psutil.net_if_addrs(),
                'io_counters': psutil.net_io_counters()._asdict()
            }
            
            return {
                'cpu': cpu_info,
                'memory': memory_info,
                'disk': disk_info,
                'network': network_info,
                'boot_time': psutil.boot_time()
            }
            
        except Exception as e:
            print(f"Error collecting system info: {e}")
            return {}
            
    def generate_report(self, report_name: str = None) -> str:
        """Generate comprehensive profiling report"""
        if not report_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"profiling_report_{timestamp}"
        
        # Collect final data
        self.collect_process_info()
        system_info = self.collect_system_info()
        summary = self.system_monitor.get_summary()
        
        # Generate detailed report
        report_data = {
            'report_info': {
                'name': report_name,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'duration': self.end_time - self.start_time if self.end_time else 0
            },
            'system_info': system_info,
            'process_info': {
                'main_process': self.app_process,
                'child_processes': self.child_processes
            },
            'performance_summary': summary,
            'thread_analysis': summary.get('threads', {}).get('current_details', {}),
            'thread_growth': summary.get('threads', {}).get('growth_analysis', {})
        }
        
        # Add function profiling if available
        if self.stats:
            # Get top functions by cumulative time
            io = io.StringIO()
            self.stats.sort_stats('cumulative')
            self.stats.print_stats(20, file=io)  # Top 20 functions
            report_data['function_profiling'] = io.getvalue()
        
        # Save detailed report
        detailed_report_path = self.output_dir / f"{report_name}_detailed.json"
        with open(detailed_report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Generate summary report
        summary_report_path = self.output_dir / f"{report_name}_summary.txt"
        self.generate_summary_report(summary_report_path, report_data)
        
        print(f"Detailed report saved: {detailed_report_path}")
        print(f"Summary report saved: {summary_report_path}")
        
        return str(detailed_report_path)
        
    def generate_summary_report(self, report_path: str, report_data: Dict[str, Any]) -> str:
        """Generate human-readable summary report"""
        try:
            with open(report_path, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("APPLICATION PROFILING REPORT SUMMARY\n")
                f.write("=" * 80 + "\n\n")
                
                # Report info
                report_info = report_data['report_info']
                f.write(f"Profiling Duration: {report_info['duration']:.2f} seconds\n\n")
                
                # System information
                f.write("SYSTEM INFORMATION:\n")
                f.write("-" * 40 + "\n")
                system_info = report_data['system_info']
                if system_info:
                    f.write(f"CPU Cores: {system_info['cpu']['count']}\n")
                    f.write(f"Memory Total: {system_info['memory']['total'] / (1024**3):.2f} GB\n")
                    f.write(f"Disk Total: {system_info['disk']['usage']['total'] / (1024**3):.2f} GB\n")
                f.write("\n")
                
                # Performance summary
                f.write("PERFORMANCE SUMMARY:\n")
                f.write("-" * 40 + "\n")
                summary = report_data['performance_summary']
                if summary:
                    # CPU usage
                    cpu_stats = summary.get('cpu', {})
                    if cpu_stats:
                        f.write("CPU Usage:\n")
                        f.write(f"  Average: {cpu_stats.get('mean', 0):.2f}%\n")
                        f.write(f"  Maximum: {cpu_stats.get('max', 0):.2f}%\n")
                        f.write(f"  Minimum: {cpu_stats.get('min', 0):.2f}%\n\n")
                    
                    # Memory usage
                    memory_stats = summary.get('memory', {})
                    if memory_stats:
                        f.write("Memory Usage:\n")
                        f.write(f"  Average: {memory_stats.get('mean', 0):.2f}%\n")
                        f.write(f"  Maximum: {memory_stats.get('max', 0):.2f}%\n")
                        f.write(f"  Minimum: {memory_stats.get('min', 0):.2f}%\n\n")
                    
                    # Process CPU usage
                    process_cpu_stats = summary.get('process_cpu', {})
                    if process_cpu_stats:
                        f.write("Process CPU Usage:\n")
                        f.write(f"  Average: {process_cpu_stats.get('mean', 0):.2f}%\n")
                        f.write(f"  Maximum: {process_cpu_stats.get('max', 0):.2f}%\n")
                        f.write(f"  Minimum: {process_cpu_stats.get('min', 0):.2f}%\n\n")
                    
                    # Process memory usage
                    process_memory_stats = summary.get('process_memory', {})
                    if process_memory_stats:
                        f.write("Process Memory Usage:\n")
                        f.write(f"  Average: {process_memory_stats.get('mean', 0) / (1024**2):.2f} MB\n")
                        f.write(f"  Maximum: {process_memory_stats.get('max', 0) / (1024**2):.2f} MB\n")
                        f.write(f"  Minimum: {process_memory_stats.get('min', 0) / (1024**2):.2f} MB\n\n")
                
                # Process information
                f.write("PROCESS INFORMATION:\n")
                f.write("-" * 40 + "\n")
                process_info = report_data['process_info']
                if process_info and process_info['main_process']:
                    main_process = process_info['main_process']
                    f.write(f"Main Process: {main_process['name']} (PID: {main_process['pid']})\n")
                    
                    # Thread information
                    thread_stats = summary.get('threads', {})
                    if thread_stats:
                        f.write(f"Threads: {thread_stats.get('max', 0)}\n")
                        f.write(f"Status: {main_process['status']}\n\n")
                        
                        # Thread growth analysis
                        growth_analysis = thread_stats.get('growth_analysis', {})
                        if growth_analysis:
                            f.write("THREAD ANALYSIS:\n")
                            f.write("-" * 40 + "\n")
                            f.write(f"Initial Thread Count: {growth_analysis.get('initial_thread_count', 0)}\n")
                            f.write(f"Final Thread Count: {growth_analysis.get('final_thread_count', 0)}\n")
                            f.write(f"Thread Growth: {growth_analysis.get('thread_growth', 0)}\n")
                            f.write(f"Snapshots Taken: {growth_analysis.get('snapshots', 0)}\n\n")
                            
                            # Thread details
                            thread_details = thread_stats.get('current_details', {})
                            if thread_details:
                                f.write("CURRENT THREAD BREAKDOWN:\n")
                                f.write("-" * 40 + "\n")
                                summary_details = thread_details.get('summary', {})
                                f.write(f"Python Threads: {summary_details.get('python_threads', 0)}\n")
                                f.write(f"Qt Threads: {summary_details.get('qt_threads', 0)}\n")
                                f.write(f"System Threads: {summary_details.get('system_threads', 0)}\n\n")
                                
                                # Detailed thread information
                                categories = thread_details.get('categories', {})
                                if categories:
                                    f.write("DETAILED THREAD INFORMATION:\n")
                                    f.write("-" * 40 + "\n")
                                    
                                    # Python threads
                                    python_threads = categories.get('python_threads', [])
                                    if python_threads:
                                        f.write("Python Threads:\n")
                                        for thread in python_threads:
                                            f.write(f"  - {thread['name']} (daemon: {thread['daemon']}, alive: {thread['alive']})\n")
                                        f.write("\n")
                                    
                                    # Qt threads
                                    qt_threads = categories.get('qt_threads', [])
                                    if qt_threads:
                                        f.write("Qt Threads:\n")
                                        for thread in qt_threads:
                                            f.write(f"  - {thread['name']} (main: {thread.get('is_main', False)}, running: {thread.get('is_running', False)})\n")
                                        f.write("\n")
                
                # Function profiling
                if 'function_profiling' in report_data:
                    f.write("TOP FUNCTIONS BY EXECUTION TIME:\n")
                    f.write("-" * 40 + "\n")
                    f.write(report_data['function_profiling'])
                
                f.write("\n" + "=" * 80 + "\n")
                f.write("Report generated by Application Profiler Tool\n")
                f.write("=" * 80 + "\n")
            
            return str(report_path)
            
        except Exception as e:
            print(f"Error generating summary report: {e}")
            return ""


def profile_application(duration: int = 60, output_dir: str = "profiling_reports"):
    """Profile the application for a specified duration"""
    profiler = ApplicationProfiler(output_dir)
    
    print(f"Starting application profiling for {duration} seconds...")
    profiler.start_profiling()
    
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("\nProfiling interrupted by user")
    
    profiler.stop_profiling()
    report_path = profiler.generate_report()
    
    print(f"Profiling completed. Report saved to: {report_path}")
    return profiler


def stop_profiling_and_save(profiler):
    """Stop profiling and save results"""
    profiler.stop_profiling()
    return profiler.generate_report()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Application Profiler Tool")
    parser.add_argument("--duration", type=int, default=60, help="Profiling duration in seconds")
    parser.add_argument("--output-dir", default="profiling_reports", help="Output directory for reports")
    parser.add_argument("--continuous", action="store_true", help="Run continuous profiling until interrupted")
    
    args = parser.parse_args()
    
    if args.continuous:
        print("Starting continuous profiling (press Ctrl+C to stop)...")
        profiler = ApplicationProfiler(args.output_dir)
        profiler.start_profiling()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping continuous profiling...")
            stop_profiling_and_save(profiler)
    else:
        profile_application(args.duration, args.output_dir)


if __name__ == "__main__":
    main() 