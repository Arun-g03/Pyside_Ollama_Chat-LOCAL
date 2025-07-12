@echo off
REM Application Profiler Launcher for Windows
REM Usage: run_profiler.bat [duration] [output_dir]

echo Application Profiler Launcher
echo ================================

if "%1"=="" (
    echo Running profiler with default settings (60 seconds)...
    python run_profiler.py
) else if "%1"=="--quick" (
    echo Running quick profiler (30 seconds)...
    python run_profiler.py --quick
) else if "%1"=="--help" (
    echo Usage:
    echo   run_profiler.bat                    - Run with default settings (60s)
    echo   run_profiler.bat --quick           - Run quick profiling (30s)
    echo   run_profiler.bat --help            - Show this help
    echo.
    echo Examples:
    echo   run_profiler.bat --quick
    echo   python run_profiler.py --duration 300 --output-dir my_reports
) else (
    echo Running profiler with custom duration: %1 seconds
    python run_profiler.py --duration %1
)

echo.
echo Profiling completed. Check the profiling_reports directory for results.
pause 