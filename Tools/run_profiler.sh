#!/bin/bash
# Application Profiler Launcher for Unix/Linux
# Usage: ./run_profiler.sh [duration] [output_dir]

echo "Application Profiler Launcher"
echo "================================"

if [ "$1" = "" ]; then
    echo "Running profiler with default settings (60 seconds)..."
    python3 run_profiler.py
elif [ "$1" = "--quick" ]; then
    echo "Running quick profiler (30 seconds)..."
    python3 run_profiler.py --quick
elif [ "$1" = "--help" ]; then
    echo "Usage:"
    echo "  ./run_profiler.sh                    - Run with default settings (60s)"
    echo "  ./run_profiler.sh --quick           - Run quick profiling (30s)"
    echo "  ./run_profiler.sh --help            - Show this help"
    echo ""
    echo "Examples:"
    echo "  ./run_profiler.sh --quick"
    echo "  python3 run_profiler.py --duration 300 --output-dir my_reports"
else
    echo "Running profiler with custom duration: $1 seconds"
    python3 run_profiler.py --duration "$1"
fi

echo ""
echo "Profiling completed. Check the profiling_reports directory for results." 