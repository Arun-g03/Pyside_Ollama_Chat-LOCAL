# PySide Ollama Chat - Advanced AI Chat Application

A sophisticated desktop chat application built with PySide6 that provides an intuitive interface for interacting with AI models through Ollama. Features advanced personality systems, text-to-speech capabilities, spell checking, and comprehensive response enhancement.

## 🌟 Key Features

### 🤖 **AI Chat Interface**
- Seamless integration with Ollama AI models
- Real-time chat with customizable AI personalities
- Support for multiple AI models and configurations
- Conversation history management
- Advanced conversation enhancement system

### 🎭 **Advanced Personality System**
- **Comprehensive Personality Framework**: Create detailed AI personalities with traits, examples, and constraints
- **Agnostic Personalities**: Reusable personalities that work with any user without hardcoded names/pronouns
- **Pre-built Categories**: Family members, professions, historic figures, and specialists
- **Dynamic System Prompts**: Automatically generates comprehensive prompts using all personality components

### 🔊 **Multi-Platform Voice Features**
- **Text-to-Speech (TTS)**: Multiple TTS engines including Coqui TTS, Edge TTS, and pyttsx3
- **Speech-to-Text (STT)**: Vosk-based offline speech recognition
- **Audio Visualization**: Real-time EQ visualizers for audio feedback
- **Voice Controls**: Recording, playback, and voice settings management
- **Streaming Audio**: Real-time audio streaming with interruption support

### ✨ **Response Enhancement System**
- **Automatic Enhancement**: Analyzes and improves AI responses automatically
- **Smart Detection**: Identifies responses that need more detail or better structure
- **Seamless Integration**: Replaces original responses with enhanced versions
- **No User Input Required**: Works completely automatically

### 🔍 **Built-in Spellchecker**
- Real-time spell checking with red underlines
- Context menu suggestions for corrections
- Personal dictionary support
- Toggle on/off functionality

### 🧠 **Memory & Semantic Search**
- **Conversation Memory**: Short-term and long-term memory systems
- **Semantic Search**: Find relevant conversations using AI embeddings
- **Memory Management**: Browse and manage conversation history
- **Context Preservation**: Maintain conversation context across sessions

### 🔄 **Advanced Threading System**
- **Persistent Thread Pools**: Reusable threads for better performance and resource management
- **Dual Architecture**: QThread for streaming operations, QRunnable for processing tasks
- **Smart Thread Management**: Automatic thread lifecycle management with configurable timeouts
- **Thread Monitoring**: Real-time monitoring of thread utilization and performance
- **Resource Optimization**: Intelligent thread allocation based on system capabilities
- **Error Recovery**: Automatic thread replacement and error handling
- **Thread Safety**: Proper signal/slot connections and thread-safe communication

### 📊 **Complexity Analysis**
- Analyze conversation complexity and readability
- Visual complexity indicators
- Detailed analysis widgets

### ⚙️ **Advanced Configuration**
- Customizable chat settings (temperature, max tokens, etc.)
- Window size and layout preferences
- Feature toggles for various enhancements
- Persistent configuration management

## 📸 Application Screenshots

Here are some screenshots showcasing the key features of PySide Ollama Chat:

### Main Chat Interface
![Main Chat Interface](DOCUMENTATION/App_Images/Main%20chat_blank.png)
*Clean and intuitive main chat interface with conversation history*

### Model Management
![Model Management](DOCUMENTATION/App_Images/Model_Management.png)
*Easy model selection and configuration with Ollama integration*

### Personality Selection
![Personality Selection](DOCUMENTATION/App_Images/Personality_Selection.png)
*Browse and select from a wide variety of pre-built personalities*

### Personality Creation
![Personality Creation](DOCUMENTATION/App_Images/Personality_Creation.png)
*Create custom personalities with comprehensive trait configuration*

### Chat Interaction
![Chat Interaction](DOCUMENTATION/App_Images/Chat_Hello.png)
*Engage in natural conversations with AI personalities*

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Ollama installed and running locally
- Virtual environment (recommended)
- NVIDIA GPU with CUDA 12.4 support (for advanced TTS features)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Pyside_Ollama_Chat-LOCAL
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Windows
   python -m venv chat_env
   chat_env\Scripts\activate
   
   # Linux/Mac
   python3 -m venv chat_env
   source chat_env/bin/activate
   ```

3. **Install dependencies**:
   The application includes automatic dependency checking and installation:
   ```bash
   python main.py
   ```
   
   The application will automatically check for missing dependencies and install them if needed.

### Manual Dependency Installation
If you prefer to install dependencies manually:

```bash
# Core dependencies
pip install PySide6 requests pygments edge-tts pygame keyboard

# For full functionality including Coqui TTS and spellchecker
python pyside_chat/startup/install_dependencies.py
```

### Dependency Management

The application includes comprehensive dependency management:

**Automatic Dependency Check**:
- `main.py` automatically checks for missing dependencies before starting
- Automatically runs `install_dependencies.py` if issues are found
- Provides detailed reports of missing packages and version conflicts

**Command Line Options**:
```bash
# Normal startup with dependency checking
python main.py

# Skip dependency checking
python main.py --skip-deps

# Check dependencies but don't auto-install
python main.py --no-auto-install
```

**Manual Dependency Management**:
```bash
# Check dependencies manually
python pyside_chat/startup/dependency_checker.py

# Install dependencies manually
python pyside_chat/startup/install_dependencies.py
```

## 📖 Usage

### Basic Chat
1. Launch the application
2. Select an AI model from the dropdown
3. Choose a personality or create a custom one
4. Start chatting!

### Voice Features
- **Text-to-Speech**: Enable TTS in voice settings to hear AI responses
- **Speech-to-Text**: Use voice input for hands-free chatting
- **Audio Visualization**: Watch real-time EQ visualizers during audio playback
- **Voice Controls**: Adjust speed, volume, and voice selection

### Threading & Performance
- **Persistent Thread Pools**: Optimized thread management for streaming and processing
- **QThread for Streaming**: Long-running operations like chat streaming and audio processing
- **QRunnable for Processing**: Quick tasks like spell checking and data processing
- **Thread Monitoring**: Real-time monitoring of thread utilization and performance metrics
- **Automatic Resource Management**: Intelligent thread allocation and cleanup

### Personality Management
- **Browse Pre-built Personalities**: Navigate through categories like Family members, Professions, etc.
- **Create Custom Personalities**: Use the personality creation form with comprehensive options
- **Edit Existing Personalities**: Modify traits, examples, and constraints
- **Agnostic Personalities**: Use placeholders like `{user_name}` for reusable personalities

### Memory & Search
- **Memory Tab**: Browse and manage conversation history
- **Semantic Search**: Find relevant conversations using natural language queries
- **Memory Settings**: Configure short-term and long-term memory retention

### Spellchecker
- **Automatic Detection**: Misspelled words are highlighted with red underlines
- **Context Menu**: Right-click on misspelled words for correction suggestions
- **Personal Dictionary**: Add words to ignore them in future checks
- **Toggle**: Enable/disable spell checking as needed

## 🎨 Personality System

### Creating Personalities
The personality system supports comprehensive character creation:

```json
{
  "traits": {
    "name": "Character Name",
    "description": "Character description",
    "tone": "friendly and supportive",
    "style": "casual and caring",
    "expertise": ["topic1", "topic2"],
    "conversation_style": "friendly",
    "response_length": "detailed",
    "formality_level": "casual",
    "humor_level": "moderate",
    "emoji_usage": true,
    "code_formatting": false
  },
  "prompt": {
    "system_prompt": "You are a character speaking to {user_name}...",
    "user_prompt_template": "{user_name}: {user_input}\nCharacter:",
    "context_prompt": "Our conversation so far:\n{context}\n\n{user_name} says: {user_input}",
    "examples": [
      "Example response 1",
      "Example response 2"
    ],
    "constraints": [
      "Always be supportive",
      "Maintain character consistency"
    ]
  }
}
```

### Agnostic Personalities
Use placeholders for reusable personalities:
- `{user_name}` - User's name
- `{user_pronouns}` - User's pronouns
- `{character_name}` - Character's name
- `{character_title}` - Character's title

## ⚙️ Configuration

### Default Settings
The application uses `config.json` for default settings:

```json
{
  "default_model": "deepseek-r1:32b",
  "default_temperature": 0.7,
  "default_personality": "Specialist.assistant",
  "auto_save_enabled": true,
  "spellcheck_enabled": true,
  "window_size": {
    "width": 1200,
    "height": 823
  },
  "chat_settings": {
    "max_tokens": 2048,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
  },
  "voice_settings": {
    "stt_api": "Vosk",
    "tts_api": "Coqui TTS",
    "auto_speak": true,
    "voice_speed": 1.0,
    "tts_streaming": true
  },
  "enhancement_enabled": false,
  "history_enabled": true,
  "memory_enabled": true,
  "theme": "Dark"
}
```

### Available Models
Download models from Ollama's official site: https://ollama.com/search

## 🏗️ Project Structure

```
Pyside_Ollama_Chat-LOCAL/
├── main.py                 # Application entry point
├── config.json            # Default configuration
├── pyside_chat/          # Source code
│   ├── app/              # Application lifecycle and management
│   │   ├── main.py       # Main application window
│   │   ├── service_manager.py  # Service coordination
│   │   ├── event_bus.py  # Event-driven architecture
│   │   ├── app_lifecycle.py  # Application lifecycle management
│   │   └── threading_integration.py  # Threading integration
│   ├── config/           # Configuration management
│   │   └── config_manager.py
│   ├── core/             # Core abstractions and utilities
│   │   ├── logging/      # Logging system
│   │   ├── models/       # Data models
│   │   ├── threading/    # Advanced threading system
│   │   │   ├── threading_service.py      # Main threading service
│   │   │   ├── persistent_thread_pool.py # Persistent thread pools
│   │   │   ├── qthread_workers.py        # QThread-based workers
│   │   │   ├── qrunnable_tasks.py        # QRunnable-based tasks
│   │   │   ├── thread_monitor.py         # Thread monitoring
│   │   │   └── thread_calculator.py      # Thread allocation logic
│   │   └── utils/        # Core utilities
│   ├── features/         # Domain-oriented feature modules
│   │   ├── chat/         # Chat functionality and controllers
│   │   │   ├── chat_controller.py
│   │   │   ├── conversation_service.py
│   │   │   ├── complexity_analyser/
│   │   │   ├── enhancers/
│   │   │   └── summarization/
│   │   ├── memory/       # Memory management and semantic search
│   │   │   ├── memory_service.py
│   │   │   └── semantic_search.py
│   │   ├── voice/        # Voice processing (TTS, STT, audio)
│   │   │   ├── voice_service.py
│   │   │   ├── voice_service_manager.py
│   │   │   ├── tts/      # Text-to-speech services
│   │   │   ├── stt/      # Speech-to-text services
│   │   │   ├── audio/    # Audio recording and playback
│   │   │   └── orchestrator/  # Voice process management
│   │   ├── personality/  # AI personality system
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   ├── profiles/ # Personality definitions
│   │   │   ├── loader.py
│   │   │   └── formatter.py
│   │   ├── ollama/       # Ollama AI integration
│   │   │   ├── ollama_service.py
│   │   │   └── ollama_chat.py
│   │   └── user/         # User profile management
│   │       └── user_profile_service.py
│   ├── ui/               # User interface components
│   │   ├── ui_manager.py # UI coordination
│   │   ├── tabs/         # Tab-based interface components
│   │   │   ├── chat_tab/
│   │   │   ├── model_tab.py
│   │   │   ├── personality_tab.py
│   │   │   └── memory_tab.py
│   │   ├── Widgets/      # Reusable UI widgets
│   │   │   ├── spellchecker_widget.py
│   │   │   ├── complexity_widget.py
│   │   │   ├── message_editor.py
│   │   │   └── chat_navigation.py
│   │   ├── dialogs/      # Modal dialogs and settings
│   │   ├── themes/       # Styling and theming
│   │   ├── visualizers/  # Audio visualization components
│   │   └── utils/        # UI utilities
│   └── startup/          # Application startup and dependency management
│       ├── dependency_checker.py
│       ├── install_dependencies.py
│       ├── requirements.txt
│       └── system_installer.py
├── DOCUMENTATION/         # Project documentation
├── User_history/          # Conversation history storage
├── Logs/                  # Application logs
├── models/                # Vosk speech recognition models
├── Development_Tools/     # Development and analysis tools
└── PACKAGING_the_app/     # Application packaging utilities
```

## 🔧 Development

### Architecture Overview

The application follows a modular, domain-driven design:

- **App Layer**: Application lifecycle and service coordination
- **Features Layer**: Domain-specific functionality (chat, voice, personality, etc.)
- **Core Layer**: Shared abstractions and utilities
- **UI Layer**: User interface components and management
- **Startup Layer**: Dependency management and initialization

### Key Components

**Service Manager**: Coordinates all application services
**Event Bus**: Handles communication between components
**Chat Controller**: Manages chat functionality and AI interactions
**Voice Service**: Handles TTS, STT, and audio processing
**Personality Service**: Manages AI personality system
**Memory Service**: Handles conversation memory and semantic search
**Threading Service**: Manages persistent thread pools and threading operations

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
The project follows Python best practices with:
- Type hints
- Docstrings
- PEP 8 compliance
- Modular architecture

### Adding New Features
1. Create feature branch
2. Implement functionality in appropriate feature module
3. Add tests
4. Update documentation
5. Submit pull request

## 🐛 Troubleshooting

### Common Issues

**Spellchecker Not Working**:
- Install system libraries: `python pyside_chat/startup/install_dependencies.py`
- Check console for error messages
- Ensure pyenchant is properly installed

**Ollama Connection**:
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Verify API endpoint in settings

**Voice Features**:
- Install audio dependencies: `python pyside_chat/startup/install_dependencies.py`
- Download Vosk models for speech recognition
- Check audio device settings

**Performance Issues**:
- Disable spell checking temporarily
- Reduce window size
- Close unnecessary tabs
- Check GPU memory usage for TTS features
- Monitor thread pool utilization
- Adjust thread pool sizes for your system

**Dependency Issues**:
- Run dependency checker: `python pyside_chat/startup/dependency_checker.py`
- Install missing dependencies: `python pyside_chat/startup/install_dependencies.py`
- Check Python version (3.8+ required)

## 📝 License

[License](LICENSE.txt)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

## 📚 Documentation

For detailed documentation, see the `DOCUMENTATION/` folder:
- [Personality System Enhancements](DOCUMENTATION/PERSONALITY_SYSTEM_ENHANCEMENTS.md)
- [Agnostic Personality Examples](DOCUMENTATION/agnostic_personality_examples.md)
- [Follow-up System](DOCUMENTATION/FOLLOW_UP_SYSTEM.md)
- [Spellchecker Guide](DOCUMENTATION/SPELLCHECKER_README.md)
- [Pronoun Usage Guide](DOCUMENTATION/pronoun_usage_guide.md)
- [Semantic Search](DOCUMENTATION/SEMANTIC_SEARCH_README.md)
- [Environment Setup](DOCUMENTATION/env_commands.md)
- [Logging Commands](DOCUMENTATION/Logging%20Commands.md)

## 🔮 Future Works

### 🔄 **Threading Enhancements**
- **Dynamic Thread Scaling** - Automatic thread pool size adjustment based on system load
- **Thread Performance Analytics** - Advanced metrics and optimization suggestions
- **Distributed Threading** - Multi-process threading for CPU-intensive operations
- **Thread Priority Management** - Intelligent thread prioritization based on task importance

### 🎯 **Additional Features**
- **Voice Cloning** - Create custom voices from audio samples
- **Emotion Detection** - Analyze text sentiment for appropriate voice modulation
- **Multi-language Support** - Automatic language detection and TTS switching
- **Audio Export** - Save conversations as audio files
- **Real-time Voice Chat** - Two-way voice communication with AI

### 🖼️ **Multi-Modal AI Support**
- **Image Context** - Upload images to provide visual context for AI responses
- **Document Analysis** - Support for PDF, DOCX, TXT, and other document formats
- **Code File Processing** - Upload and analyze code files for programming assistance
- **Screenshot Integration** - Capture and include screenshots in conversations
- **Visual Question Answering** - Ask questions about uploaded images
- **File Type Recognition** - Automatic detection and handling of various file formats
- **Batch File Processing** - Upload multiple files for comprehensive analysis
- **Image Annotation** - AI-powered image description and analysis

## 🙏 Acknowledgments

- Ollama team for the AI model framework
- PySide6 developers for the GUI framework
- Coqui AI for advanced TTS capabilities
- Vosk team for offline speech recognition
- All contributors and users of this project 