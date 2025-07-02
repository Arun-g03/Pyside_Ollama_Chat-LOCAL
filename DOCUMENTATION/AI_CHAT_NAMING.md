# AI-Powered Chat Naming

## Overview

The chat application now features AI-powered conversation naming that automatically generates descriptive names for your conversations based on their content. This replaces the generic timestamp-based filenames with meaningful, context-aware names.

## How It Works

### Automatic Naming
- Conversations start with "New Chat" as the default name
- After 3 or more messages are exchanged, the AI analyzes the conversation content
- A lightweight AI model (llama3.2:3b) generates a concise, descriptive name (3-6 words)
- The generated name captures the main topic or theme of the conversation

### Manual Naming
- Right-click on any conversation in the navigation panel
- Select "Generate AI Name" to manually trigger name generation
- This option only appears for conversations that don't already have AI-generated names

## Features

### Smart Name Generation
- **Context-Aware**: Analyzes user messages to understand conversation topics
- **Concise**: Generates short, descriptive names (3-6 words)
- **Specific**: Avoids generic terms like "conversation" or "chat"
- **Consistent**: Uses lower temperature (0.3) for more reliable results

### Fallback System
- If AI generation fails, conversations retain their original filename
- No data loss - original filenames are preserved as fallbacks
- Graceful error handling with detailed logging

### Performance Optimized
- Uses auto mode to automatically select the smallest available model for fast generation
- Only processes conversations with 3+ messages
- Asynchronous processing to avoid blocking the UI
- Caches generated names to avoid regeneration

## Technical Details

### Requirements
- Ollama running with at least one model available
- Auto mode will automatically select the smallest available model for efficiency
- Minimum 3 messages in conversation for generation
- Active internet connection for AI model access

### Configuration
The summarization service can be configured through the following settings:

```python
# Model used for name generation (Auto mode selects smallest available model)
summarization_model = "Auto"

# Minimum messages required for generation
min_messages_for_summarization = 3

# Temperature for generation (lower = more consistent)
temperature = 0.3
```

### File Format
AI-generated names are stored in the conversation metadata:

```json
{
  "metadata": {
    "ai_generated_name": "Python Code Debugging Help",
    "created": "2024-01-15T10:30:00",
    "model": "llama3.2:3b",
    "message_count": 5
  },
  "conversation": [...]
}
```

## Usage Examples

### Example Generated Names
- "Python Code Debugging Help"
- "Recipe for Chocolate Cake"
- "Travel Planning to Japan"
- "Math Homework Assistance"
- "Book Recommendations"

### User Interface
- **Navigation Panel**: Shows AI-generated names instead of filenames
- **Tooltips**: Display both AI name and original filename
- **Context Menu**: Right-click for manual generation option
- **Status Updates**: Real-time feedback on generation progress

## Troubleshooting

### Common Issues

1. **No names generated**
   - Check if Ollama is running
   - Verify at least one model is available
   - Ensure conversation has 3+ messages

2. **Generic names**
   - Model may need better prompting
   - Check conversation content quality
   - Verify model is responding correctly

3. **Generation failures**
   - Check application logs for errors
   - Verify network connectivity
   - Ensure sufficient system resources

### Logging
The feature includes comprehensive logging:

```
INFO: Starting name generation for conversation: /path/to/chat.json
INFO: Found 5 user messages for summarization
INFO: Sending summarization request to model: llama3.2:3b
INFO: Received response: Python Code Debugging Help
INFO: Generated chat name: Python Code Debugging Help
```

## Future Enhancements

- **Custom Models**: Allow users to select different models for generation
- **Name Editing**: Manual editing of generated names
- **Batch Processing**: Generate names for multiple conversations
- **Language Support**: Multi-language name generation
- **Advanced Filtering**: More sophisticated content analysis

## Contributing

To contribute to the AI naming feature:

1. Review the `SummarizationService` class
2. Test with different conversation types
3. Improve the prompt engineering
4. Add support for additional models
5. Enhance error handling and user feedback 