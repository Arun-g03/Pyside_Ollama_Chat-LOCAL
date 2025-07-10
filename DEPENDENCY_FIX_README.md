# Dependency Fix Guide

## Problem
The application was failing to start due to dependency conflicts with `sentence_transformers` and its dependencies (PyTorch, transformers, etc.).

## Solution

### 1. Updated Dependencies
The `install_dependencies.py` file has been updated to include missing dependencies:

**New Dependencies Added:**
- `PyAudio` - Audio I/O library for recording and playback
- `sounddevice` - Audio library for real-time audio processing  
- `vosk` - Offline speech recognition library
- `playsound` - Simple audio playback library

### 2. Fixed sentence_transformers Issue
Created `fix_sentence_transformers.py` to resolve the dependency conflict:

```bash
python fix_sentence_transformers.py
```

This script:
1. Uninstalls conflicting packages (torch, transformers, sentence-transformers, etc.)
2. Installs compatible versions in the correct order
3. Tests the installation

### 3. Fallback Semantic Search
Created `semantic_search_fallback.py` that provides keyword-based memory search when `sentence_transformers` is not available.

The main `semantic_search.py` now gracefully falls back to keyword matching if the ML dependencies fail.

## How to Fix

### Option 1: Run the Fix Script (Recommended)
```bash
python fix_sentence_transformers.py
```

### Option 2: Manual Installation
```bash
# Uninstall conflicting packages
pip uninstall -y torch torchvision torchaudio transformers sentence-transformers huggingface-hub accelerate

# Install compatible versions
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install scikit-learn --only-binary=all
pip install huggingface-hub==0.20.3
pip install transformers==4.35.2
pip install accelerate==0.25.0
pip install sentence-transformers==2.2.2
```

### Option 3: Use Updated Install Script
```bash
python pyside_chat/startup/install_dependencies.py
```

## What Was Updated

### 1. `pyside_chat/startup/install_dependencies.py`
- Added missing audio dependencies (PyAudio, sounddevice, vosk, playsound)
- Updated verification to include new dependencies
- Added helpful error messages for failed installations

### 2. `pyside_chat/features/memory/semantic_search.py`
- Added graceful fallback when sentence_transformers is not available
- Improved error handling for missing dependencies

### 3. `pyside_chat/features/memory/semantic_search_fallback.py`
- New fallback service using keyword matching
- Compatible API with the main semantic search service
- No ML dependencies required

### 4. `fix_sentence_transformers.py`
- Automated script to fix dependency conflicts
- Tests installation after fixing
- Provides clear feedback on success/failure

## Testing

After running the fix, test the installation:

```python
import torch
import transformers
import sentence_transformers
from sentence_transformers import SentenceTransformer

print("✅ All packages imported successfully!")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ SentenceTransformer model loaded successfully!")
```

## Notes

- The application will now work even if `sentence_transformers` fails to install
- Memory search will use keyword matching as a fallback
- Audio features require PyAudio and sounddevice
- Offline speech recognition requires vosk and model files
- All new dependencies are marked as optional (`skip_if_failed: True`)

## Troubleshooting

### PyAudio Issues on Windows
If PyAudio fails to install on Windows:
1. Install Visual C++ Build Tools
2. Or use: `pip install pipwin` then `pipwin install pyaudio`

### Vosk Model Issues
If offline speech recognition doesn't work:
1. Download Vosk models from: https://alphacephei.com/vosk/models
2. Place in `models/` directory

### sentence_transformers Still Failing
The application will work with keyword-based memory search as a fallback. 