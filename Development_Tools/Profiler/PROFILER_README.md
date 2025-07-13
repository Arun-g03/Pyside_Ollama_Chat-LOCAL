# Unified Application Profiler

A comprehensive profiling tool for the PySide Ollama Chat application. Launches the app, monitors system resources, thread usage, and function performance, and generates detailed reports.

## Features
- **System Resource Monitoring**: CPU, memory, disk, and network usage
- **Thread Profiling**: Python and OS thread usage and growth
- **Function Profiling**: Function-level profiling using cProfile
- **Automatic App Launch**: Starts the app and profiles until it exits (or for a set duration)
- **Comprehensive Reports**: JSON and human-readable summary
- **Modular Design**: Easy to extend via `profiler_helpers.py`

## Requirements
- Python 3.7+
- psutil
- cProfile (built-in)

## Installation
Install dependencies:
```bash
pip install psutil
```

## Usage
Run the profiler (default: launches `main.py` and profiles until it exits):
```bash
python Tools/profiler.py
```

### Advanced Usage
```bash
# Profile for 120 seconds
python Tools/profiler.py --duration 120

# Custom output directory
python Tools/profiler.py --output-dir my_reports

# Profile a different entry point
python Tools/profiler.py --entry-point my_app.py

# Basic (faster, less detailed) profiling
python Tools/profiler.py --detail-level basic
```

## Command Line Options
- `--duration`: Profiling duration in seconds (default: until app exits)
- `--output-dir`: Output directory for reports (default: profiling_reports)
- `--entry-point`: Application entry point (default: main.py)
- `--detail-level`: Profiling detail level (`full` or `basic`)

## Output
The profiler generates:
- **JSON Report**: All collected data (system, threads, functions)
- **Summary Report**: Human-readable summary of key stats

### Example Output (Summary)
```
======================================================================
UNIFIED PROFILER SUMMARY
======================================================================

SYSTEM RESOURCE SNAPSHOT:
CPU: 25.5%
Memory: 65.3%
Disk: 40.2%
Net bytes sent: 123456

THREAD SNAPSHOT:
Python threads: 8
System threads: 12

TOP FUNCTIONS BY CUMULATIVE TIME:
<function stats here>

======================================================================
Full JSON report: profiling_reports/unified_profile_YYYYMMDD_HHMMSS.json
```

## Tips
- Use longer durations for more comprehensive analysis
- Use a custom output directory to organize reports
- Compare reports before/after code changes

## Troubleshooting
- **Import Errors**: Ensure all dependencies are installed
- **App not launching**: Check the entry point path
- **No output**: Check permissions for the output directory

## Extending the Profiler
- Add new profilers or enhance existing ones in `profiler_helpers.py`
- Add new fields to the JSON report or summary as needed

---

This tool replaces all previous profiler scripts. For legacy profiling, see your version control history. 