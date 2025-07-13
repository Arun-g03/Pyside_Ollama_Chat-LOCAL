"""
Profiler Helpers for Unified Profiler

Modular classes for system, thread, and function profiling, and report generation.
"""

import threading
import psutil
import time
import cProfile
import pstats
import io
import json
import datetime
import os
import signal
from pathlib import Path
from typing import Dict, List, Any, Optional


class SystemProfiler:
    """Profiles system resources (CPU, memory, disk, network) during app execution."""
    
    def __init__(self, interval=1.0):
        self.interval = interval
        self.running = False
        self.data = []
        self.monitor_thread = None
        self._start_time = None
        self._end_time = None

    def start(self):
        """Start continuous system monitoring in background thread."""
        self.running = True
        self.data = []
        self._start_time = time.time()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"System monitoring started (interval: {self.interval}s)")

    def stop(self):
        """Stop monitoring and collect final data."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self._end_time = time.time()
        # Collect one final data point
        self._collect()
        print("System monitoring stopped")

    def _monitor_loop(self):
        """Background monitoring loop."""
        while self.running:
            try:
                self._collect()
                time.sleep(self.interval)
            except Exception as e:
                print(f"Error in system monitoring: {e}")
                break

    def _collect(self):
        """Collect system resource data."""
        try:
            timestamp = time.time()
            
            # CPU info
            cpu_percent = psutil.cpu_percent(interval=None)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            cpu_freq_dict = cpu_freq._asdict() if cpu_freq else None
            
            # Memory info
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk info
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network info
            net_io = psutil.net_io_counters()
            net_if_addrs = psutil.net_if_addrs()
            
            # System info
            boot_time = psutil.boot_time()
            
            data_point = {
                'timestamp': timestamp,
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count,
                    'frequency': cpu_freq_dict,
                    'percent_per_core': psutil.cpu_percent(interval=None, percpu=True)
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'free': memory.free,
                    'percent': memory.percent,
                    'swap': swap._asdict()
                },
                'disk': {
                    'usage': disk_usage._asdict(),
                    'io': disk_io._asdict() if disk_io else None
                },
                'network': {
                    'io': net_io._asdict() if net_io else None,
                    'interfaces': {k: [addr._asdict() for addr in v] for k, v in net_if_addrs.items()}
                },
                'system': {
                    'boot_time': boot_time,
                    'platform': os.uname()._asdict() if hasattr(os, 'uname') else None
                }
            }
            
            self.data.append(data_point)
            
        except Exception as e:
            print(f"Error collecting system data: {e}")

    def get_data(self):
        """Get collected system data with statistics."""
        if not self.data:
            return {}
        
        # Calculate statistics
        cpu_percents = [d['cpu']['percent'] for d in self.data]
        memory_percents = [d['memory']['percent'] for d in self.data]
        
        stats = {
            'cpu': {
                'mean': sum(cpu_percents) / len(cpu_percents) if cpu_percents else 0,
                'max': max(cpu_percents) if cpu_percents else 0,
                'min': min(cpu_percents) if cpu_percents else 0
            },
            'memory': {
                'mean': sum(memory_percents) / len(memory_percents) if memory_percents else 0,
                'max': max(memory_percents) if memory_percents else 0,
                'min': min(memory_percents) if memory_percents else 0
            }
        }
        
        return {
            'interval': self.interval,
            'start_time': self._start_time,
            'end_time': self._end_time,
            'duration': (self._end_time - self._start_time) if self._end_time and self._start_time else 0,
            'data_points': self.data,
            'statistics': stats,
            'data_points_count': len(self.data)
        }


class ProcessProfiler:
    """Profiles the launched application process and its children."""
    
    def __init__(self, target_pid=None):
        self.target_pid = target_pid
        self.running = False
        self.data = []
        self.monitor_thread = None
        self._start_time = None
        self._end_time = None
        self.target_process = None

    def start(self, target_pid=None):
        """Start process monitoring."""
        if target_pid:
            self.target_pid = target_pid
        self.running = True
        self.data = []
        self._start_time = time.time()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"Process monitoring started for PID: {self.target_pid}")

    def stop(self):
        """Stop process monitoring."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self._end_time = time.time()
        # Collect final data
        self._collect()
        print("Process monitoring stopped")

    def _monitor_loop(self):
        """Background process monitoring loop."""
        while self.running:
            try:
                self._collect()
                time.sleep(1.0)  # Monitor every second
            except Exception as e:
                print(f"Error in process monitoring: {e}")
                break

    def _collect(self):
        """Collect process data."""
        try:
            if not self.target_pid:
                return
                
            timestamp = time.time()
            
            # Get target process
            try:
                target_proc = psutil.Process(self.target_pid)
            except psutil.NoSuchProcess:
                # Process may have exited
                return
            
            # Process info
            proc_info = {
                'pid': target_proc.pid,
                'name': target_proc.name(),
                'status': target_proc.status(),
                'create_time': target_proc.create_time(),
                'cpu_percent': target_proc.cpu_percent(),
                'memory_info': target_proc.memory_info()._asdict(),
                'memory_percent': target_proc.memory_percent(),
                'num_threads': target_proc.num_threads(),
                'connections': len(target_proc.connections()),
                'open_files': len(target_proc.open_files()),
                'environ': dict(target_proc.environ())
            }
            
            # Child processes
            children = []
            try:
                for child in target_proc.children(recursive=True):
                    child_info = {
                        'pid': child.pid,
                        'name': child.name(),
                        'status': child.status(),
                        'cpu_percent': child.cpu_percent(),
                        'memory_info': child.memory_info()._asdict(),
                        'num_threads': child.num_threads()
                    }
                    children.append(child_info)
            except Exception as e:
                print(f"Error getting child processes: {e}")
            
            data_point = {
                'timestamp': timestamp,
                'main_process': proc_info,
                'child_processes': children,
                'total_children': len(children)
            }
            
            self.data.append(data_point)
            
        except Exception as e:
            print(f"Error collecting process data: {e}")

    def get_data(self):
        """Get collected process data with statistics."""
        if not self.data:
            return {}
        
        # Calculate statistics
        cpu_percents = [d['main_process']['cpu_percent'] for d in self.data if d['main_process']]
        memory_percents = [d['main_process']['memory_percent'] for d in self.data if d['main_process']]
        memory_mb = [d['main_process']['memory_info']['rss'] / (1024*1024) for d in self.data if d['main_process']]
        
        stats = {
            'cpu': {
                'mean': sum(cpu_percents) / len(cpu_percents) if cpu_percents else 0,
                'max': max(cpu_percents) if cpu_percents else 0,
                'min': min(cpu_percents) if cpu_percents else 0
            },
            'memory': {
                'mean_mb': sum(memory_mb) / len(memory_mb) if memory_mb else 0,
                'max_mb': max(memory_mb) if memory_mb else 0,
                'min_mb': min(memory_mb) if memory_mb else 0,
                'percent_mean': sum(memory_percents) / len(memory_percents) if memory_percents else 0,
                'percent_max': max(memory_percents) if memory_percents else 0,
                'percent_min': min(memory_percents) if memory_percents else 0
            }
        }
        
        return {
            'start_time': self._start_time,
            'end_time': self._end_time,
            'duration': (self._end_time - self._start_time) if self._end_time and self._start_time else 0,
            'target_pid': self.target_pid,
            'data_points': self.data,
            'statistics': stats,
            'data_points_count': len(self.data)
        }


class ThreadProfiler:
    """Profiles thread usage and thread growth during app execution."""
    
    def __init__(self, interval=2.0):
        self.interval = interval
        self.snapshots = []
        self.running = False
        self.monitor_thread = None
        self._start_time = None
        self._end_time = None

    def start(self):
        """Start thread monitoring."""
        self.running = True
        self.snapshots = []
        self._start_time = time.time()
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"Thread monitoring started (interval: {self.interval}s)")

    def stop(self):
        """Stop thread monitoring."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self._end_time = time.time()
        # Capture final snapshot
        self._capture_snapshot()
        print("Thread monitoring stopped")

    def _monitor_loop(self):
        """Background thread monitoring loop."""
        while self.running:
            try:
                self._capture_snapshot()
                time.sleep(self.interval)
            except Exception as e:
                print(f"Error in thread monitoring: {e}")
                break

    def _capture_snapshot(self):
        """Capture thread snapshot."""
        try:
            timestamp = time.time()
            
            # Python threads
            py_threads = []
            for t in threading.enumerate():
                thread_info = {
                    'name': t.name,
                    'ident': t.ident,
                    'daemon': t.daemon,
                    'alive': t.is_alive(),
                    'type': 'python_thread'
                }
                py_threads.append(thread_info)
            
            # System threads (current process)
            sys_threads = []
            try:
                current_proc = psutil.Process()
                for t in current_proc.threads():
                    thread_info = {
                        'id': t.id,
                        'user_time': t.user_time,
                        'system_time': t.system_time,
                        'type': 'system_thread'
                    }
                    sys_threads.append(thread_info)
            except Exception as e:
                print(f"Error getting system threads: {e}")
            
            snapshot = {
                'timestamp': timestamp,
                'python_threads': py_threads,
                'system_threads': sys_threads,
                'total_python_threads': len(py_threads),
                'total_system_threads': len(sys_threads),
                'total_threads': len(py_threads) + len(sys_threads)
            }
            
            self.snapshots.append(snapshot)
            
        except Exception as e:
            print(f"Error capturing thread snapshot: {e}")

    def get_data(self):
        """Get thread data with analysis."""
        if not self.snapshots:
            return {}
        
        # Thread growth analysis
        initial_count = self.snapshots[0]['total_threads'] if self.snapshots else 0
        final_count = self.snapshots[-1]['total_threads'] if self.snapshots else 0
        growth = final_count - initial_count
        
        # Thread statistics
        total_threads = [s['total_threads'] for s in self.snapshots]
        python_threads = [s['total_python_threads'] for s in self.snapshots]
        system_threads = [s['total_system_threads'] for s in self.snapshots]
        
        stats = {
            'total_threads': {
                'mean': sum(total_threads) / len(total_threads) if total_threads else 0,
                'max': max(total_threads) if total_threads else 0,
                'min': min(total_threads) if total_threads else 0
            },
            'python_threads': {
                'mean': sum(python_threads) / len(python_threads) if python_threads else 0,
                'max': max(python_threads) if python_threads else 0,
                'min': min(python_threads) if python_threads else 0
            },
            'system_threads': {
                'mean': sum(system_threads) / len(system_threads) if system_threads else 0,
                'max': max(system_threads) if system_threads else 0,
                'min': min(system_threads) if system_threads else 0
            }
        }
        
        return {
            'start_time': self._start_time,
            'end_time': self._end_time,
            'duration': (self._end_time - self._start_time) if self._end_time and self._start_time else 0,
            'interval': self.interval,
            'snapshots': self.snapshots,
            'growth_analysis': {
                'initial_thread_count': initial_count,
                'final_thread_count': final_count,
                'thread_growth': growth,
                'snapshots_count': len(self.snapshots)
            },
            'statistics': stats
        }


class FunctionProfiler:
    """Profiles function-level performance using cProfile."""
    
    def __init__(self):
        self.profiler = None
        self.stats = None
        self.enabled = False
        self._start_time = None
        self._end_time = None

    def start(self):
        """Start function profiling."""
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        self.enabled = True
        self._start_time = time.time()
        print("Function profiling started")

    def stop(self):
        """Stop function profiling."""
        if self.profiler and self.enabled:
            self.profiler.disable()
            self.stats = pstats.Stats(self.profiler)
            self.enabled = False
            self._end_time = time.time()
            print("Function profiling stopped")

    def get_data(self):
        """Get function profiling data."""
        if not self.stats:
            return None
        
        # Get detailed stats by temporarily redirecting stdout
        import sys
        from io import StringIO
        
        # Save original stdout
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            self.stats.sort_stats('cumulative')
            self.stats.print_stats(50)  # Top 50 functions
            detailed_stats = sys.stdout.getvalue()
        finally:
            # Restore original stdout
            sys.stdout = old_stdout
        
        # Get summary stats
        stats_summary = {
            'total_calls': self.stats.total_calls,
            'total_time': self.stats.total_tt,
            'start_time': self._start_time,
            'end_time': self._end_time,
            'duration': (self._end_time - self._start_time) if self._end_time and self._start_time else 0
        }
        
        return {
            'summary': stats_summary,
            'detailed_stats': detailed_stats
        }


def generate_reports(system_profiler, process_profiler, thread_profiler, function_profiler, output_dir):
    """Generate comprehensive JSON and summary reports from all profilers."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_name = f"unified_profile_{timestamp}"

    # Gather data
    system_data = system_profiler.get_data() if system_profiler else {}
    process_data = process_profiler.get_data() if process_profiler else {}
    thread_data = thread_profiler.get_data() if thread_profiler else {}
    function_data = function_profiler.get_data() if function_profiler else {}

    # JSON report
    json_report = {
        'report_info': {
            'name': report_name,
            'generated': datetime.datetime.now().isoformat(),
            'duration': system_data.get('duration', 0)
        },
        'system': system_data,
        'process': process_data,
        'threads': thread_data,
        'function_profile': function_data,
    }
    json_path = output_dir / f"{report_name}.json"
    with open(json_path, 'w') as f:
        json.dump(json_report, f, indent=2, default=str)

    # Summary report
    summary_path = output_dir / f"{report_name}_summary.txt"
    with open(summary_path, 'w') as f:
        f.write("="*80 + "\n")
        f.write("UNIFIED PROFILER SUMMARY REPORT\n")
        f.write("="*80 + "\n\n")
        
        # Report info
        f.write(f"Report: {report_name}\n")
        f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration: {system_data.get('duration', 0):.2f} seconds\n\n")
        
        # System summary
        f.write("SYSTEM RESOURCES:\n")
        f.write("-" * 40 + "\n")
        if system_data and system_data.get('data_points'):
            last = system_data['data_points'][-1]
            stats = system_data.get('statistics', {})
            f.write(f"CPU Usage: {last['cpu']['percent']:.1f}% (avg: {stats.get('cpu', {}).get('mean', 0):.1f}%)\n")
            f.write(f"Memory Usage: {last['memory']['percent']:.1f}% (avg: {stats.get('memory', {}).get('mean', 0):.1f}%)\n")
            f.write(f"Disk Usage: {last['disk']['usage']['percent']:.1f}%\n")
            if last['network']['io']:
                f.write(f"Network Sent: {last['network']['io']['bytes_sent']:,} bytes\n")
                f.write(f"Network Recv: {last['network']['io']['bytes_recv']:,} bytes\n")
        f.write("\n")
        
        # Process summary
        f.write("PROCESS INFORMATION:\n")
        f.write("-" * 40 + "\n")
        if process_data and process_data.get('data_points'):
            last = process_data['data_points'][-1]
            stats = process_data.get('statistics', {})
            main_proc = last['main_process']
            f.write(f"Main Process: {main_proc['name']} (PID: {main_proc['pid']})\n")
            f.write(f"Status: {main_proc['status']}\n")
            f.write(f"CPU Usage: {main_proc['cpu_percent']:.1f}% (avg: {stats.get('cpu', {}).get('mean', 0):.1f}%)\n")
            f.write(f"Memory Usage: {main_proc['memory_percent']:.1f}% ({main_proc['memory_info']['rss'] / (1024*1024):.1f} MB)\n")
            f.write(f"Threads: {main_proc['num_threads']}\n")
            f.write(f"Child Processes: {last['total_children']}\n")
        f.write("\n")
        
        # Thread summary
        f.write("THREAD ANALYSIS:\n")
        f.write("-" * 40 + "\n")
        if thread_data and thread_data.get('snapshots'):
            last = thread_data['snapshots'][-1]
            growth = thread_data.get('growth_analysis', {})
            f.write(f"Total Threads: {last['total_threads']}\n")
            f.write(f"Python Threads: {last['total_python_threads']}\n")
            f.write(f"System Threads: {last['total_system_threads']}\n")
            f.write(f"Thread Growth: {growth.get('thread_growth', 0)} (+{growth.get('initial_thread_count', 0)} -> {growth.get('final_thread_count', 0)})\n")
        f.write("\n")
        
        # Function summary
        f.write("FUNCTION PROFILING:\n")
        f.write("-" * 40 + "\n")
        if function_data and function_data.get('summary'):
            summary = function_data['summary']
            f.write(f"Total Function Calls: {summary.get('total_calls', 0):,}\n")
            f.write(f"Total Time: {summary.get('total_time', 0):.4f} seconds\n")
            f.write(f"Profiling Duration: {summary.get('duration', 0):.2f} seconds\n\n")
            
            # Show top functions
            if function_data.get('detailed_stats'):
                f.write("TOP FUNCTIONS BY CUMULATIVE TIME:\n")
                f.write(function_data['detailed_stats'][:2000])  # First 2000 chars
        
        f.write("\n" + "="*80 + "\n")
        f.write(f"Full JSON report: {json_path}\n")
        f.write("="*80 + "\n")
    
    print(f"Reports saved:")
    print(f"  JSON: {json_path}")
    print(f"  Summary: {summary_path}")
    
    return str(json_path) 