# PySide Chat - Refactored Structure

This directory contains the refactored version of the PySide Chat application with an improved project structure.

## �� Structure Overview

### `app/`
Application-level components including lifecycle management and service coordination.

### `config/`
Configuration management and settings.

### `core/`
Core abstractions, models, and utilities shared across the application.

### `features/`
Domain-oriented feature modules:
- **chat/**: Chat functionality and controllers
- **memory/**: Memory management and semantic search
- **voice/**: Voice processing (TTS, STT, audio)
- **personality/**: AI personality system
- **ollama/**: Ollama AI integration
- **user/**: User profile management

### `ui/`
User interface components:
- **main_window.py**: Main application window
- **themes/**: Styling and theming
- **widgets/**: Reusable UI components
- **dialogs/**: Modal dialogs and settings
- **tabs/**: Tab-based interface components
- **visualizers/**: Audio visualization components

### `workers/`
Background processing and worker threads.

### `startup/`
Application startup, dependency management, and installation utilities.

## �� Migration Status

This is a **work in progress**. Some files may need adaptation to work with the new structure.

### Next Steps:
1. Update import statements to match new structure
2. Adapt main window to new architecture
3. Update service dependencies
4. Test all functionality
5. Remove old structure

## 🚀 Usage

To use the refactored version:

```bash
# Update main.py to import from new structure
python main.py
```

## �� Notes

- All files have been copied from the original structure
- Some files may need manual adaptation
- Import statements will need updating
- The new structure follows domain-driven design principles
