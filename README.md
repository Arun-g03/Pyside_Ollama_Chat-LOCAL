# Pyside_Chat - Advanced AI Chat Application

A sophisticated desktop chat application built with PySide6 that provides an intuitive interface for interacting with AI models through Ollama. Features advanced personality systems, text-to-speech capabilities, spell checking, and comprehensive response enhancement.

## 🌟 Key Features

### 🤖 **AI Chat Interface**
- Seamless integration with Ollama AI models
- Real-time chat with customizable AI personalities
- Support for multiple AI models and configurations
- Conversation history management

### 🎭 **Advanced Personality System**
- **Comprehensive Personality Framework**: Create detailed AI personalities with traits, examples, and constraints
- **Agnostic Personalities**: Reusable personalities that work with any user without hardcoded names/pronouns
- **Pre-built Categories**: Family members, professions, relationships, historic figures, and specialists
- **Dynamic System Prompts**: Automatically generates comprehensive prompts using all personality components

### 🔊 **Multi-Platform Text-to-Speech**
- **Edge TTS** (Microsoft) - Fast and natural, recommended
- **Coqui TTS** - Advanced emotion control and multi-speaker support
- **Google TTS** - High quality but slower
- **pyttsx3** - Fast local TTS (more robotic)
- **Audio Playback Controls** - Skip, pause, and volume control

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

### ⚙️ **Advanced Configuration**
- Customizable chat settings (temperature, max tokens, etc.)
- Window size and layout preferences
- Feature toggles for various enhancements
- Persistent configuration management

### 📊 **Complexity Analysis**
- Analyze conversation complexity and readability
- Visual complexity indicators
- Detailed analysis widgets

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Ollama installed and running locally
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone
   cd Pyside_Chat
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv chat_env
   # Windows
   chat_env\Scripts\activate
   # macOS/Linux
   source chat_env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install spellchecker** (optional):
   ```bash
   python utils/install_spellchecker.py
   ```

5. **Run the application**:
   ```bash
   python main.py
   ```

### Minimal Installation
For basic functionality with just Edge TTS:
```bash
pip install PySide6 requests pygments edge-tts pygame keyboard
```

### Full Installation
For all features including Coqui TTS and spellchecker:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Chat
1. Launch the application
2. Select an AI model from the dropdown
3. Choose a personality or create a custom one
4. Start chatting!

### Personality Management
- **Browse Pre-built Personalities**: Navigate through categories like Family members, Professions, etc.
- **Create Custom Personalities**: Use the personality creation form with comprehensive options
- **Edit Existing Personalities**: Modify traits, examples, and constraints
- **Agnostic Personalities**: Use placeholders like `{user_name}` for reusable personalities

### Text-to-Speech
- **Enable TTS**: Check the TTS checkbox in the interface
- **Select TTS Engine**: Choose from Edge TTS, Coqui TTS, Google TTS, or pyttsx3
- **Control Playback**: Use skip, pause, and volume controls
- **Keyboard Shortcuts**: Use keyboard input for skip functionality

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
  "default_personality": "Family members.aunt",
  "auto_save_enabled": true,
  "spellcheck_enabled": true,
  "window_size": {
    "width": 1200,
    "height": 800
  },
  "chat_settings": {
    "max_tokens": 2048,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
  }
}
```

### Available Models
https://ollama.com/search

## 🏗️ Project Structure

```
Pyside_Chat/
├── main.py                 # Application entry point
├── config.json            # Default configuration
├── requirements.txt       # Python dependencies
├── SRC/                   # Source code
│   ├── ollama_chat.py     # Main chat interface
│   ├── personality_widget.py # Personality management
│   ├── personality_model.py  # Personality data model
│   ├── settings_dialog.py    # Settings interface
│   ├── config_manager.py     # Configuration management
│   ├── complexity_widget.py  # Complexity analysis UI
│   ├── complexity_analyzer.py # Complexity analysis logic
│   ├── worker.py          # Background worker
│   ├── styles.py          # UI styling
│   └── utils.py           # Utility functions
├── personalities/         # Personality definitions
│   ├── Family members/    # Family-related personalities
│   ├── Professions/       # Professional personalities
│   ├── relationships/     # Relationship-based personalities
│   ├── Historic people/   # Historical figure personalities
│   └── Specialists/       # Specialist personalities
├── DOCUMENTATION/         # Project documentation
├── chat_history/          # Conversation history storage
├── tests/                 # Test files
└── utils/                 # Utility scripts
```

## 🔧 Development

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
2. Implement functionality
3. Add tests
4. Update documentation
5. Submit pull request

## 🐛 Troubleshooting

### Common Issues

**Spellchecker Not Working**:
- Install system libraries: `python utils/install_spellchecker.py`
- Check console for error messages
- Ensure pyenchant is properly installed

**TTS Issues**:
- Verify audio drivers are working
- Check TTS engine installation
- Try different TTS engines

**Ollama Connection**:
- Ensure Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Verify API endpoint in settings

**Performance Issues**:
- Disable spell checking temporarily
- Use lighter TTS engines
- Reduce window size

## 📝 License

This project is licensed under the MIT License with the following conditions:

- You are free to use, modify, and distribute this software
- You must include the original copyright notice and license
- You cannot redistribute this as a standalone product
- You cannot claim this work as your own




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

## 🙏 Acknowledgments

- Ollama team for the AI model framework
- PySide6 developers for the GUI framework
- Microsoft Edge TTS for high-quality speech synthesis
- Coqui AI for advanced TTS capabilities
- All contributors and users of this project 