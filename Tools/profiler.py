#!/usr/bin/env python3
"""
Application Profiler Tool

A comprehensive profiling tool for the PySide Ollama Chat application.
Profiles CPU usage, memory consumption, system resources, and application performance.
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


class SystemMonitor(QObject):
    """Monitor system resources during application execution"""
    
    # Signals for real-time monitoring
    cpu_usage_updated = Signal(float)
    memory_usage_updated = Signal(float)
    disk_io_updated = Signal(dict)
    network_io_updated = Signal(dict)
    
    def __init__(self, interval: float = 1.0):
        super().__init__()
        self.interval = interval
        self.monitoring = False
        self.monitor_thread = None
        self.data_points = []
        
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
                    'process_memory_vms': process_memory_info.vms
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
        print("Starting application profiling...")
        
        # Start system monitoring
        self.system_monitor.start_monitoring()
        
        # Start cProfile if available
        if PROFILE_AVAILABLE:
            self.profiler = cProfile.Profile()
            self.profiler.enable()
            
        self.start_time = time.time()
        
    def stop_profiling(self):
        """Stop profiling and collect results"""
        print("Stopping application profiling...")
        
        self.end_time = time.time()
        
        # Stop system monitoring
        self.system_monitor.stop_monitoring()
        
        # Stop cProfile if available
        if PROFILE_AVAILABLE and self.profiler:
            self.profiler.disable()
            
            # Create stats object
            s = io.StringIO()
            self.stats = pstats.Stats(self.profiler, stream=s)
            self.stats.sort_stats('cumulative')
            
    def collect_process_info(self):
        """Collect information about the application process and its children"""
        try:
            current_process = psutil.Process()
            self.app_process = {
                'pid': current_process.pid,
                'name': current_process.name(),
                'cmdline': current_process.cmdline(),
                'cpu_percent': current_process.cpu_percent(),
                'memory_info': current_process.memory_info()._asdict(),
                'num_threads': current_process.num_threads(),
                'status': current_process.status()
            }
            
            # Get child processes
            children = current_process.children(recursive=True)
            for child in children:
                try:
                    child_info = {
                        'pid': child.pid,
                        'name': child.name(),
                        'cmdline': child.cmdline(),
                        'cpu_percent': child.cpu_percent(),
                        'memory_info': child.memory_info()._asdict(),
                        'num_threads': child.num_threads(),
                        'status': child.status()
                    }
                    self.child_processes.append(child_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Error collecting process info: {e}")
            
    def collect_system_info(self) -> Dict[str, Any]:
        """Collect comprehensive system information"""
        try:
            # CPU info
            cpu_info = {
                'count': psutil.cpu_count(),
                'count_logical': psutil.cpu_count(logical=True),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                'usage_per_cpu': psutil.cpu_percent(percpu=True)
            }
            
            # Memory info
            memory = psutil.virtual_memory()
            memory_info = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percent': memory.percent
            }
            
            # Disk info
            disk = psutil.disk_usage('/')
            disk_info = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
            
            # Network info
            network_info = {
                'interfaces': psutil.net_if_addrs(),
                'io_counters': psutil.net_io_counters()._asdict()
            }
            
            # Platform info
            platform_info = {
                'system': psutil.sys.platform,
                'python_version': sys.version,
                'architecture': psutil.sys.maxsize > 2**32 and "64bit" or "32bit"
            }
            
            return {
                'cpu': cpu_info,
                'memory': memory_info,
                'disk': disk_info,
                'network': network_info,
                'platform': platform_info,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error collecting system info: {e}")
            return {}
            
    def generate_report(self, report_name: str = None) -> str:
        """Generate a comprehensive profiling report"""
        if not report_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"profiling_report_{timestamp}"
            
        report_path = self.output_dir / f"{report_name}.json"
        
        # Collect final data
        self.collect_process_info()
        system_info = self.collect_system_info()
        monitoring_summary = self.system_monitor.get_summary()
        
        # Prepare report data
        report_data = {
            'profiling_info': {
                'start_time': self.start_time,
                'end_time': self.end_time,
                'duration': self.end_time - self.start_time if self.end_time else None,
                'report_generated': datetime.datetime.now().isoformat()
            },
            'system_info': system_info,
            'monitoring_summary': monitoring_summary,
            'process_info': {
                'main_process': self.app_process,
                'child_processes': self.child_processes
            },
            'raw_monitoring_data': self.system_monitor.data_points
        }
        
        # Add cProfile stats if available
        if self.stats:
            # Get top functions by cumulative time
            s = io.StringIO()
            self.stats.print_stats(20)  # Top 20 functions
            report_data['profile_stats'] = s.getvalue()
            
            # Get function call counts
            call_counts = {}
            for func, (cc, nc, tt, ct, callers) in self.stats.stats.items():
                call_counts[f"{func[0]}:{func[1]}:{func[2]}"] = {
                    'call_count': cc,
                    'primitive_call_count': nc,
                    'total_time': tt,
                    'cumulative_time': ct
                }
            report_data['function_stats'] = call_counts
        
        # Save report
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"Profiling report saved to: {report_path}")
        return str(report_path)
        
    def generate_summary_report(self, report_path: str) -> str:
        """Generate a human-readable summary report"""
        try:
            with open(report_path, 'r') as f:
                data = json.load(f)
                
            summary_path = report_path.replace('.json', '_summary.txt')
            
            with open(summary_path, 'w') as f:
                f.write("=" * 80 + "\n")
                f.write("APPLICATION PROFILING REPORT SUMMARY\n")
                f.write("=" * 80 + "\n\n")
                
                # Profiling duration
                if data['profiling_info']['duration']:
                    f.write(f"Profiling Duration: {data['profiling_info']['duration']:.2f} seconds\n\n")
                
                # System summary
                f.write("SYSTEM INFORMATION:\n")
                f.write("-" * 40 + "\n")
                f.write(f"CPU Cores: {data['system_info']['cpu']['count']}\n")
                f.write(f"Memory Total: {data['system_info']['memory']['total'] / (1024**3):.2f} GB\n")
                f.write(f"Disk Total: {data['system_info']['disk']['total'] / (1024**3):.2f} GB\n\n")
                
                # Performance summary
                if data['monitoring_summary']:
                    f.write("PERFORMANCE SUMMARY:\n")
                    f.write("-" * 40 + "\n")
                    summary = data['monitoring_summary']
                    
                    f.write(f"CPU Usage:\n")
                    f.write(f"  Average: {summary['cpu']['mean']:.2f}%\n")
                    f.write(f"  Maximum: {summary['cpu']['max']:.2f}%\n")
                    f.write(f"  Minimum: {summary['cpu']['min']:.2f}%\n\n")
                    
                    f.write(f"Memory Usage:\n")
                    f.write(f"  Average: {summary['memory']['mean']:.2f}%\n")
                    f.write(f"  Maximum: {summary['memory']['max']:.2f}%\n")
                    f.write(f"  Minimum: {summary['memory']['min']:.2f}%\n\n")
                    
                    f.write(f"Process CPU Usage:\n")
                    f.write(f"  Average: {summary['process_cpu']['mean']:.2f}%\n")
                    f.write(f"  Maximum: {summary['process_cpu']['max']:.2f}%\n")
                    f.write(f"  Minimum: {summary['process_cpu']['min']:.2f}%\n\n")
                    
                    f.write(f"Process Memory Usage:\n")
                    f.write(f"  Average: {summary['process_memory']['mean'] / (1024**2):.2f} MB\n")
                    f.write(f"  Maximum: {summary['process_memory']['max'] / (1024**2):.2f} MB\n")
                    f.write(f"  Minimum: {summary['process_memory']['min'] / (1024**2):.2f} MB\n\n")
                
                # Process information
                if data['process_info']['main_process']:
                    f.write("PROCESS INFORMATION:\n")
                    f.write("-" * 40 + "\n")
                    proc = data['process_info']['main_process']
                    f.write(f"Main Process: {proc['name']} (PID: {proc['pid']})\n")
                    f.write(f"Threads: {proc['num_threads']}\n")
                    f.write(f"Status: {proc['status']}\n\n")
                    
                    if data['process_info']['child_processes']:
                        f.write(f"Child Processes: {len(data['process_info']['child_processes'])}\n")
                        for i, child in enumerate(data['process_info']['child_processes'][:5]):  # Show first 5
                            f.write(f"  {i+1}. {child['name']} (PID: {child['pid']})\n")
                        if len(data['process_info']['child_processes']) > 5:
                            f.write(f"  ... and {len(data['process_info']['child_processes']) - 5} more\n\n")
                
                # Top functions (if available)
                if 'function_stats' in data:
                    f.write("TOP FUNCTIONS BY EXECUTION TIME:\n")
                    f.write("-" * 40 + "\n")
                    
                    # Sort by cumulative time
                    sorted_funcs = sorted(
                        data['function_stats'].items(),
                        key=lambda x: x[1]['cumulative_time'],
                        reverse=True
                    )
                    
                    for i, (func_name, stats) in enumerate(sorted_funcs[:10]):  # Top 10
                        f.write(f"{i+1}. {func_name}\n")
                        f.write(f"   Calls: {stats['call_count']}\n")
                        f.write(f"   Total Time: {stats['total_time']:.4f}s\n")
                        f.write(f"   Cumulative Time: {stats['cumulative_time']:.4f}s\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("Report generated by Application Profiler Tool\n")
                f.write("=" * 80 + "\n")
                
            print(f"Summary report saved to: {summary_path}")
            return summary_path
            
        except Exception as e:
            print(f"Error generating summary report: {e}")
            return ""


def profile_application(duration: int = 60, output_dir: str = "profiling_reports"):
    """Profile the main application for a specified duration"""
    profiler = ApplicationProfiler(output_dir)
    
    try:
        print(f"Starting application profiling for {duration} seconds...")
        profiler.start_profiling()
        
        # Import and run the main application
        from pyside_chat.features.ollama.ollama_chat import OllamaChat
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        window = OllamaChat()
        window.show()
        
        # Set up a timer to stop profiling after the specified duration
        timer = QTimer()
        timer.timeout.connect(lambda: stop_profiling_and_save(profiler))
        timer.start(duration * 1000)
        
        # Run the application
        result = app.exec()
        
        # If the app exits before the timer, stop profiling
        if profiler.system_monitor.monitoring:
            profiler.stop_profiling()
            report_path = profiler.generate_report()
            profiler.generate_summary_report(report_path)
            
        return result
        
    except Exception as e:
        print(f"Error during profiling: {e}")
        traceback.print_exc()
        return 1


def stop_profiling_and_save(profiler):
    """Stop profiling and save reports"""
    profiler.stop_profiling()
    report_path = profiler.generate_report()
    profiler.generate_summary_report(report_path)
    print("Profiling completed and reports saved.")


def main():
    """Main entry point for the profiler tool"""
    parser = argparse.ArgumentParser(description="Application Profiler Tool")
    parser.add_argument(
        "--duration", 
        type=int, 
        default=60,
        help="Profiling duration in seconds (default: 60)"
    )
    parser.add_argument(
        "--output-dir", 
        type=str, 
        default="profiling_reports",
        help="Output directory for reports (default: profiling_reports)"
    )
    parser.add_argument(
        "--quick", 
        action="store_true",
        help="Quick profiling mode (30 seconds)"
    )
    
    args = parser.parse_args()
    
    if args.quick:
        duration = 30
    else:
        duration = args.duration
        
    print(f"Application Profiler Tool")
    print(f"Duration: {duration} seconds")
    print(f"Output directory: {args.output_dir}")
    print(f"Quick mode: {args.quick}")
    print("-" * 50)
    
    # Check dependencies
    if not QT_AVAILABLE:
        print("Error: PySide6 is required for application profiling")
        return 1
        
    if not PROFILE_AVAILABLE:
        print("Warning: cProfile not available, detailed function profiling disabled")
        
    # Run profiling
    return profile_application(duration, args.output_dir)


if __name__ == "__main__":
    sys.exit(main()) 