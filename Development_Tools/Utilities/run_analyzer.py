#!/usr/bin/env python3
"""
Codebase Analyzer Runner
Simple script to run either the basic or advanced codebase analyzer.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_and_install_dependencies():
    """Check and install required dependencies."""
    required_packages = {
        'networkx': 'networkx',
        'ast': 'built-in',
        'pathlib': 'built-in',
        'typing': 'built-in',
        'collections': 'built-in',
        'json': 'built-in',
        'datetime': 'built-in',
        're': 'built-in',
        'os': 'built-in'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        if pip_name == 'built-in':
            continue
            
        try:
            importlib.import_module(package)
            print(f"✅ {package} is available")
        except ImportError:
            missing_packages.append(pip_name)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    return True


def run_basic_analyzer():
    """Run the basic codebase analyzer."""
    print("🔧 Running basic codebase analyzer...")
    try:
        from codebase_analyzer import CodebaseAnalyzer
        
        analyzer = CodebaseAnalyzer()
        analyzer.analyze_codebase()
        analyzer.generate_markdown_report("Reports/basic_codebase_analysis.md")
        
        print("✅ Basic analysis complete!")
        print("📄 Check 'basic_codebase_analysis.md' for the report")
        
    except Exception as e:
        print(f"❌ Error running basic analyzer: {e}")


def run_advanced_analyzer():
    """Run the advanced codebase analyzer."""
    print("🚀 Running advanced codebase analyzer...")
    try:
        from advanced_codebase_analyzer import AdvancedCodebaseAnalyzer
        
        analyzer = AdvancedCodebaseAnalyzer()
        analyzer.analyze_codebase()
        analyzer.generate_markdown_report("advanced_codebase_analysis.md")
        analyzer.export_dependency_graph("dependency_graph.json")
        
        print("✅ Advanced analysis complete!")
        print("📄 Check 'advanced_codebase_analysis.md' for the detailed report")
        print("📊 Check 'dependency_graph.json' for the dependency graph data")
        
    except Exception as e:
        print(f"❌ Error running advanced analyzer: {e}")


def main():
    """Main function to run the analyzer."""
    print("🔍 Codebase Relationship Analyzer")
    print("=" * 40)
    
    # Check dependencies
    if not check_and_install_dependencies():
        print("❌ Cannot proceed without required dependencies")
        return
    
    # Check if analyzer files exist
    basic_exists = Path("codebase_analyzer.py").exists()
    advanced_exists = Path("advanced_codebase_analyzer.py").exists()
    
    if not basic_exists and not advanced_exists:
        print("❌ No analyzer files found!")
        print("Please ensure codebase_analyzer.py or advanced_codebase_analyzer.py exists")
        return
    
    # Choose analyzer
    if advanced_exists:
        print("\n📋 Available analyzers:")
        if basic_exists:
            print("1. Basic Analyzer (codebase_analyzer.py)")
        print("2. Advanced Analyzer (advanced_codebase_analyzer.py)")
        
        choice = input("\nSelect analyzer (1 or 2): ").strip()
        
        if choice == "1" and basic_exists:
            run_basic_analyzer()
        elif choice == "2":
            run_advanced_analyzer()
        else:
            print("❌ Invalid choice or analyzer not available")
    elif basic_exists:
        print("\n📋 Running basic analyzer (only option available)")
        run_basic_analyzer()
    
    print("\n🎉 Analysis complete!")


if __name__ == "__main__":
    main() 