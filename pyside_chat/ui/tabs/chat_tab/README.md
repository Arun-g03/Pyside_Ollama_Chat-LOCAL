# Chat Tab Modular Structure

This folder contains the modularized components of the main chat interface. The original monolithic `chat_tab.py` has been broken down into smaller, more manageable components.

## Components

### 1. `chat_tab.py` - Main Orchestrator
The main `ChatTab` class that orchestrates all other components. This is the primary interface that should be imported and used by the main application.

**Key responsibilities:**
- Initializes and coordinates all other components
- Handles signal routing between components
- Manages the overall UI layout
- Provides the main interface for external code

### 2. `chat_display.py` - Message Display
Handles the chat message display, editing functionality, and streaming responses.

**Key responsibilities:**
- Message display and formatting
- Message editing with hover buttons
- Streaming response handling
- Mouse interaction for edit buttons

### 3. `voice_controls.py` - Voice Functionality
Manages all voice-related functionality including TTS, STT, and audio level monitoring.

**Key responsibilities:**
- Voice service initialization and management
- TTS (Text-to-Speech) functionality
- STT (Speech-to-Text) functionality
- Audio level monitoring and visualization
- Voice settings management

### 4. `eq_visualizer.py` - Audio Visualization
Handles EQ (Equalizer) visualization for audio levels during voice interactions.

**Key responsibilities:**
- EQ widget management (Circle, Bar, Waveform variants)
- Audio level to visual bar conversion
- Frequency band distribution
- EQ mode switching (None, Circle EQ, Bar EQ, etc.)

### 5. `input_controls.py` - User Input
Manages message input, send/cancel buttons, and settings controls.

**Key responsibilities:**
- Message input handling
- Send/cancel button management
- Model and personality selection
- Temperature control
- Input mode switching (Chat/Voice)

## Usage

### Basic Import
```python
from pyside_chat.ui.tabs import ChatTab

# Create the chat tab
chat_tab = ChatTab(
    parent=parent_widget,
    conversation_manager=conversation_manager,
    summarization_service=summarization_service,
    config_manager=config_manager
)
```

### Component Access
If you need to access specific components directly:

```python
# Access voice controls
voice_controls = chat_tab.voice_controls

# Access EQ visualizer
eq_visualizer = chat_tab.eq_visualizer

# Access input controls
input_controls = chat_tab.input_controls

# Access chat display
chat_display = chat_tab.chat_display
```

## Signal Connections

The main `ChatTab` class handles all signal routing between components. Key signals include:

- `message_sent` - Emitted when user sends a message
- `message_cancelled` - Emitted when user cancels a message
- `voice_input_received` - Emitted when voice input is received
- `audio_level_changed` - Emitted when audio level changes
- `message_edited` - Emitted when a message is edited

## Benefits of Modularization

1. **Maintainability**: Each component has a single responsibility
2. **Testability**: Components can be tested independently
3. **Reusability**: Components can be reused in other parts of the application
4. **Readability**: Code is easier to understand and navigate
5. **Flexibility**: Components can be modified without affecting others

## Migration Notes

The original `chat_tab.py` has been moved to `chat_tab_backup.py` for reference. The new modular structure maintains the same external interface, so existing code should continue to work without changes.

## Testing

Run the test file to verify imports work correctly:
```python
python -m pyside_chat.ui.tabs.chat_tab.test_modular_imports
``` 