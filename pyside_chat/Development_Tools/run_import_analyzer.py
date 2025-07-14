#!/usr/bin/env python3
"""
Import Analyzer Runner

Simple script to run the import analyzer with different options.
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from Development_Tools.import_analyzer import ImportAnalyzer

def main():
    """Run the import analyzer with command line options"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PySide Chat Import Analyzer")
    parser.add_argument(
        "--codebase", 
        default="pyside_chat", 
        help="Path to the codebase to analyze (default: pyside_chat)"
    )
    parser.add_argument(
        "--output-dir", 
        default="pyside_chat/core/shared_imports", 
        help="Output directory for shared import files"
    )
    parser.add_argument(
        "--report", 
        default="import_analysis_report.json", 
        help="Output file for the analysis report"
    )
    parser.add_argument(
        "--min-frequency", 
        type=int, 
        default=3, 
        help="Minimum frequency for shared import groups (default: 3)"
    )
    parser.add_argument(
        "--no-shared-files", 
        action="store_true", 
        help="Skip generating shared import files"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    print("🔍 PySide Chat Import Analyzer")
    print("="*40)
    
    # Create analyzer
    analyzer = ImportAnalyzer(args.codebase)
    
    # Scan the codebase
    print("📁 Scanning codebase...")
    analyzer.scan_codebase()
    
    # Build dependency graph
    print("🔗 Building dependency graph...")
    analyzer.build_dependency_graph()
    
    # Detect circular dependencies
    print("🔄 Detecting circular dependencies...")
    analyzer.detect_circular_dependencies()
    
    # Analyze import frequency
    print("📊 Analyzing import frequency...")
    analyzer.analyze_import_frequency()
    
    # Identify shared imports
    print("📋 Identifying shared imports...")
    analyzer.identify_shared_imports(min_frequency=args.min_frequency)
    
    # Generate shared import files (unless disabled)
    if not args.no_shared_files:
        print("📝 Generating shared import files...")
        analyzer.generate_shared_import_files(args.output_dir)
    
    # Generate report
    print("📄 Generating analysis report...")
    analyzer.generate_report(args.report)
    
    # Print summary
    analyzer.print_summary()
    
    print(f"\n✅ Analysis complete!")
    print(f"📄 Report saved to: {args.report}")
    if not args.no_shared_files:
        print(f"📁 Shared import files saved to: {args.output_dir}")
    
    # Print recommendations
    print("\n💡 RECOMMENDATIONS:")
    recommendations = analyzer.generate_recommendations()
    
    if recommendations['shared_import_files']:
        print("\n📋 Suggested shared import files:")
        for rec in recommendations['shared_import_files']:
            print(f"   {rec['file']} - {rec['category']} ({rec['potential_savings']} import lines saved)")
    
    if recommendations['circular_dependency_fixes']:
        print("\n⚠️  Circular dependency fixes needed:")
        for rec in recommendations['circular_dependency_fixes']:
            print(f"   {' -> '.join(rec['cycle'])} -> {rec['cycle'][0]}")
            print(f"   Suggestion: {rec['suggestion']}")
    
    if recommendations['import_optimizations']:
        print("\n🔧 Import optimizations:")
        for rec in recommendations['import_optimizations']:
            if rec['type'] == 'unused_imports':
                print(f"   Found potentially unused imports in {len(rec['files'])} files")

if __name__ == "__main__":
    main() 