#!/usr/bin/env python3
"""
Profiler Launcher Script

A simple launcher for the application profiler tool.
Usage:
    python run_profiler.py [options]
"""

import sys
import os
from pathlib import Path

# Add the Tools directory to the path
tools_dir = Path(__file__).parent
sys.path.insert(0, str(tools_dir))

# Add the project root to the path
project_root = tools_dir.parent
sys.path.insert(0, str(project_root))

def main():
    """Main launcher function"""
    print("Application Profiler Launcher")
    print("=" * 40)
    
    # Import and run the profiler
    try:
        from profiler import main as profiler_main
        return profiler_main()
    except ImportError as e:
        print(f"Error importing profiler: {e}")
        print("Make sure profiler.py is in the Tools directory")
        return 1
    except Exception as e:
        print(f"Error running profiler: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 