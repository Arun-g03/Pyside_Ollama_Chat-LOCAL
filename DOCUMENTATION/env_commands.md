# Environment Setup Commands

# Create a new virtual environment
python -m venv chat_env

# Activate the virtual environment
chat_env\Scripts\Activate

# OPTION 1: Automated Installation (Recommended)
# Run the automated installation script - handles all dependencies correctly
python install_dependencies.py

# OPTION 2: Manual Installation (if needed)
# Upgrade pip to latest version
python -m pip install --upgrade pip

# Install Visual C++ Build Tools (if not already installed)
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Or install via: winget install Microsoft.VisualStudio.2022.BuildTools

# STEP 1: Install basic requirements (should work without issues)
pip install -r requirements.txt

# STEP 2: Install PyTorch with pre-built wheels (CPU version)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# STEP 3: Install scikit-learn with pre-built wheels
pip install scikit-learn --only-binary=all

# STEP 4: Install compatible ML packages (in correct order)
pip install huggingface-hub==0.16.4
pip install transformers==4.21.0
pip install sentence-transformers==2.2.2

# STEP 5: Install Coqui TTS (large download, may take time)
pip install TTS==0.22

# STEP 6: Verify installation
python -c "import torch; import sklearn; import sentence_transformers; print('All packages installed successfully!')"

# TROUBLESHOOTING:
# If you encounter dependency conflicts, run:
# python fix_sentence_transformers.py

# If blis still fails, try installing specific versions:
# pip install blis==0.7.9 --only-binary=all
# pip install thinc==8.1.10 --only-binary=all