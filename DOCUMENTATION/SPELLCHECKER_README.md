# Spellchecker Feature for Ollama Chat

## Overview
The chat application now includes a built-in spellchecker that helps users catch and correct spelling mistakes in their messages before sending them.

## Features
- **Real-time spell checking**: Misspelled words are highlighted with red underlines
- **Context menu suggestions**: Right-click on misspelled words to see correction suggestions
- **Personal dictionary**: Add words to your personal dictionary to ignore them
- **Toggle on/off**: Enable or disable spell checking using the checkbox in the chat interface

## Installation

### Option 1: Automatic Installation
Run the installation script:
```bash
python install_spellchecker.py
```

### Option 2: Manual Installation

1. **Install Python package**:
   ```bash
   pip install pyenchant
   ```

2. **Install system libraries** (required for enchant):

   **Windows**:
   - Download enchant from: https://www.abisource.com/projects/enchant/
   - Or use: `pip install pyenchant`

   **macOS**:
   ```bash
   brew install enchant
   ```

   **Linux (Ubuntu/Debian)**:
   ```bash
   sudo apt-get install libenchant1c2a
   ```

   **Linux (Fedora)**:
   ```bash
   sudo dnf install enchant
   ```

## Usage

### Basic Usage
1. Type your message in the chat input box
2. Misspelled words will be automatically highlighted with red underlines
3. Right-click on any misspelled word to see correction suggestions

### Context Menu Options
When you right-click on a misspelled word, you'll see:
- **Correction suggestions**: Click any suggestion to replace the word
- **Add to dictionary**: Add the word to your personal dictionary (it won't be flagged as misspelled again)
- **Ignore**: Same as "Add to dictionary"

### Toggle Spell Checking
- Use the "Spell Check" checkbox in the chat interface to enable/disable spell checking
- When disabled, no spell checking will occur and the placeholder text will change

## Troubleshooting

### Spellchecker Not Working
1. Make sure you've installed both the Python package and system libraries
2. Check the console output for any error messages
3. Try running the installation script: `python install_spellchecker.py`

### No Suggestions Appearing
1. Make sure the word is actually misspelled (common words won't show suggestions)
2. Check if the spellchecker is enabled (checkbox should be checked)
3. Try restarting the application

### Performance Issues
- Spell checking is performed automatically as you type
- If you experience lag, you can disable spell checking temporarily
- The spell check is delayed slightly to avoid interfering with typing

## Technical Details

### Dependencies
- `pyenchant`: Python wrapper for the enchant spellchecker
- `enchant`: System spellchecker library

### Supported Languages
The spellchecker will try to use your system's default language dictionary. If not available, it will fall back to English (US or GB).

### Personal Dictionary
Words added to your personal dictionary are stored locally and will be remembered between sessions.

## Notes
- Spell checking only works on alphabetic words (not numbers, symbols, or code)
- The feature gracefully degrades if the spellchecker is not available
- Spell checking is performed client-side and doesn't send any data to external services 