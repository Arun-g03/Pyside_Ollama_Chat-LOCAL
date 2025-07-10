#!/usr/bin/env python3
"""
Fix sentence_transformers dependency issues
This script resolves conflicts between PyTorch, transformers, and sentence_transformers
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a pip command and handle errors"""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✅ {description} - Success")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🔧 Fixing sentence_transformers dependency issues")
    print("=" * 50)
    
    # Step 1: Uninstall conflicting packages
    print("\n📦 Step 1: Uninstalling conflicting packages")
    packages_to_remove = [
        "torch",
        "torchvision", 
        "torchaudio",
        "transformers",
        "sentence-transformers",
        "huggingface-hub",
        "accelerate"
    ]
    
    for package in packages_to_remove:
        run_command([sys.executable, "-m", "pip", "uninstall", "-y", package], 
                   f"Uninstalling {package}")
    
    # Step 2: Install PyTorch CPU version (compatible)
    print("\n📦 Step 2: Installing PyTorch CPU version")
    run_command([
        sys.executable, "-m", "pip", "install", 
        "torch", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"
    ], "Installing PyTorch CPU version")
    
    # Step 3: Install scikit-learn
    print("\n📦 Step 3: Installing scikit-learn")
    run_command([
        sys.executable, "-m", "pip", "install", "scikit-learn", "--only-binary=all"
    ], "Installing scikit-learn")
    
    # Step 4: Install compatible versions in correct order
    print("\n📦 Step 4: Installing compatible ML packages")
    
    # Install huggingface-hub first
    run_command([
        sys.executable, "-m", "pip", "install", "huggingface-hub==0.20.3"
    ], "Installing huggingface-hub==0.20.3")
    
    # Install transformers
    run_command([
        sys.executable, "-m", "pip", "install", "transformers==4.35.2"
    ], "Installing transformers==4.35.2")
    
    # Install accelerate
    run_command([
        sys.executable, "-m", "pip", "install", "accelerate==0.25.0"
    ], "Installing accelerate==0.25.0")
    
    # Install sentence-transformers
    run_command([
        sys.executable, "-m", "pip", "install", "sentence-transformers==2.2.2"
    ], "Installing sentence-transformers==2.2.2")
    
    # Step 5: Test the installation
    print("\n🧪 Step 5: Testing the installation")
    test_script = """
import torch
import transformers
import sentence_transformers
from sentence_transformers import SentenceTransformer

print("✅ All packages imported successfully!")
print(f"PyTorch version: {torch.__version__}")
print(f"Transformers version: {transformers.__version__}")
print(f"Sentence-transformers version: {sentence_transformers.__version__}")

# Test sentence transformer
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ SentenceTransformer model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading SentenceTransformer: {e}")
"""
    
    try:
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print("✅ Installation test passed!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Installation test failed!")
        print(f"Error: {e.stderr}")
        return False
    
    print("\n🎉 Dependency fix completed successfully!")
    print("You can now run your application without sentence_transformers issues.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 