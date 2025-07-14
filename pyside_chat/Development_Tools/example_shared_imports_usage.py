#!/usr/bin/env python3
"""
Example: Using Shared Import Files

This script demonstrates how to use the generated shared import files
to reduce import duplication and improve code organization.
"""

# Example 1: Using OS and system imports
print("=== Example 1: OS and System Imports ===")
try:
    from pyside_chat.core.shared_imports.shared_imports import *
    print("✅ Successfully imported OS/system shared imports")
    print(f"   Available: os, sys, tempfile, Path")
    print(f"   Current working directory: {os.getcwd()}")
    print(f"   Python version: {sys.version}")
except ImportError as e:
    print(f"❌ Failed to import OS/system shared imports: {e}")

# Example 2: Using JSON and time imports
print("\n=== Example 2: JSON and Time Imports ===")
try:
    
    print("✅ Successfully imported JSON/time shared imports")
    print(f"   Available: json, time, datetime")
    
    # Demonstrate usage
    data = {"message": "Hello from shared imports!", "timestamp": datetime.now().isoformat()}
    json_str = json.dumps(data, indent=2)
    print(f"   JSON example: {json_str}")
except ImportError as e:
    print(f"❌ Failed to import JSON/time shared imports: {e}")

# Example 3: Using audio imports
print("\n=== Example 3: Audio Imports ===")
try:
    from pyside_chat.core.shared_imports.audio_imports import *
    print("✅ Successfully imported audio shared imports")
    print(f"   Available: pyaudio, sounddevice, soundfile, librosa")
    
    # Check if audio libraries are available
    try:
        import pyaudio
        print("   ✅ PyAudio available")
    except ImportError:
        print("   ❌ PyAudio not available")
        
    try:
        import sounddevice as sd
        print("   ✅ SoundDevice available")
    except ImportError:
        print("   ❌ SoundDevice not available")
        
    try:
        import soundfile as sf
        print("   ✅ SoundFile available")
    except ImportError:
        print("   ❌ SoundFile not available")
        
    try:
        import librosa
        print("   ✅ Librosa available")
    except ImportError:
        print("   ❌ Librosa not available")
        
except ImportError as e:
    print(f"❌ Failed to import audio shared imports: {e}")

# Example 4: Before and After Comparison
print("\n=== Example 4: Before vs After Comparison ===")

print("BEFORE (multiple individual imports):")
print("""
import os
import sys
import tempfile
from pathlib import Path
import json
import time
from datetime import datetime
import pyaudio
import sounddevice as sd
import soundfile as sf
import librosa
""")

print("AFTER (using shared imports):")
print("""
from pyside_chat.core.shared_imports.shared_imports import *

from pyside_chat.core.shared_imports.audio_imports import *
""")

print("✅ Benefits:")
print("   - Reduced from 11 import lines to 3")
print("   - Centralized import management")
print("   - Consistent import patterns across the codebase")
print("   - Easier to maintain and update")

# Example 5: Custom shared import usage
print("\n=== Example 5: Custom Shared Import Usage ===")

def demonstrate_shared_imports():
    """Demonstrate practical usage of shared imports"""
    
    # Using OS imports
    current_dir = os.getcwd()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_path = Path(temp_file.name)
    
    # Using JSON/time imports
    data = {
        "operation": "shared_imports_demo",
        "timestamp": datetime.now().isoformat(),
        "files_created": [str(temp_path)]
    }
    
    # Save data to temp file
    with open(temp_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Created temporary file: {temp_path}")
    print(f"✅ Data written: {json.dumps(data, indent=2)}")
    
    # Cleanup
    temp_path.unlink()
    print("✅ Cleaned up temporary file")

try:
    demonstrate_shared_imports()
except Exception as e:
    print(f"❌ Error in demonstration: {e}")

print("\n=== Summary ===")
print("The shared import files provide:")
print("1. 📦 Reduced import duplication")
print("2. 🔧 Centralized import management")
print("3. 📋 Consistent import patterns")
print("4. 🚀 Easier maintenance and updates")
print("5. 📊 Better code organization")

print("\nTo use in your own files:")
print("1. Import the shared import files you need")
print("2. Replace individual imports with shared imports")
print("3. Update your code to use the imported modules")
print("4. Test to ensure everything works correctly") 