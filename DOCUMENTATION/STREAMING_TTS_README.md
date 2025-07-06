# Streaming TTS Synthesis

This document explains how to use the new streaming text-to-speech synthesis feature for Coqui TTS.

## Overview

The streaming synthesis feature allows Coqui TTS to start playing audio immediately as the text is being processed, rather than waiting for the entire audio file to be generated first. This provides a more responsive user experience, especially for longer texts.

## Features

- **Real-time playback**: Audio starts playing as soon as the first chunk is generated
- **Chunked processing**: Text is split into sentences and processed in chunks
- **Progress tracking**: Built-in progress signals for UI feedback
- **Speed control**: Audio speed can be adjusted in real-time
- **Fallback support**: Falls back to non-streaming mode if streaming fails

## Usage

### Basic Streaming Synthesis

```python
from pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service import CoquiTTSService

# Create TTS service
tts_service = CoquiTTSService()

# Use streaming synthesis (default)
tts_service.speak_text("Hello world!", use_streaming=True)

# Or explicitly use streaming
tts_service.speak_text("Hello world!", use_streaming=True)
```

### Non-Streaming Synthesis

```python
# Use traditional file-based synthesis
tts_service.speak_text("Hello world!", use_streaming=False)
```

### Through Voice Service

```python
from pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service import VoiceService

voice_service = VoiceService()

# Streaming synthesis
voice_service.speak_text_streaming("Hello world!")

# Non-streaming synthesis
voice_service.speak_text_non_streaming("Hello world!")

# Default (uses streaming for Coqui TTS)
voice_service.speak_text("Hello world!")
```

### Through Voice Service Wrapper

```python
from pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service_wrapper import VoiceServiceWrapper

voice_wrapper = VoiceServiceWrapper()

# Streaming synthesis
voice_wrapper.speak_text_streaming("Hello world!")

# Non-streaming synthesis
voice_wrapper.speak_text_non_streaming("Hello world!")
```

## Technical Details

### How It Works

1. **Text Splitting**: The input text is split into sentences using regex patterns
2. **Chunked Generation**: Each sentence is processed separately by the TTS model
3. **Real-time Playback**: Audio chunks are sent to a PyAudio stream for immediate playback
4. **Progress Tracking**: Progress signals are emitted as each chunk is processed

### Audio Processing

- **Sample Rate**: 22050 Hz (configurable)
- **Channels**: Mono (1 channel)
- **Format**: Float32
- **Chunk Size**: 1024 samples (configurable)

### Threading

- **Audio Generation**: Runs in a separate daemon thread
- **Audio Playback**: Uses QThread for PyAudio streaming
- **UI Thread**: Remains responsive during synthesis

## Configuration

### Audio Settings

```python
# Configure streaming player
streaming_player = StreamingAudioPlayer(
    sample_rate=22050,  # Audio sample rate
    channels=1,         # Mono audio
    chunk_size=1024     # Audio chunk size
)
```

### Text Processing

```python
# Configure text splitting
max_chars = 200  # Maximum characters per chunk
sentences = re.split(r'[.!?]+', text)  # Sentence splitting pattern
```

## Error Handling

The streaming synthesis includes comprehensive error handling:

- **Import Errors**: Falls back to non-streaming if PyAudio/scipy unavailable
- **Audio Errors**: Emits error signals for UI feedback
- **Thread Safety**: Proper cleanup of threads and audio streams
- **Resource Management**: Automatic cleanup of temporary files

## Performance Considerations

### Advantages

- **Lower Latency**: Audio starts playing immediately
- **Better UX**: No waiting for full generation
- **Memory Efficient**: Processes audio in chunks
- **Responsive UI**: Non-blocking operation

### Limitations

- **Model Dependent**: Only works with Coqui TTS models
- **Chunk Overhead**: Small overhead for chunk processing
- **Audio Quality**: May have slight artifacts at chunk boundaries

## Testing

Run the test script to verify streaming synthesis:

```bash
python test_streaming_tts.py
```

This will test both streaming and non-streaming modes with sample text.

## Troubleshooting

### Common Issues

1. **No Audio**: Check if PyAudio is installed and working
2. **Choppy Audio**: Try adjusting chunk size or sample rate
3. **High CPU**: Reduce chunk size or use non-streaming mode
4. **Memory Issues**: Ensure proper cleanup of audio streams

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.getLogger('pyside_chat.services.Voice_STT_TTS_SERVICES.coqui_tts_service').setLevel(logging.DEBUG)
```

## Future Enhancements

- **Adaptive Chunking**: Dynamic chunk size based on text length
- **Audio Buffering**: Configurable audio buffer size
- **Multiple Voices**: Support for voice switching during streaming
- **Audio Effects**: Real-time audio effects and filters
- **Network Streaming**: Support for remote TTS services 