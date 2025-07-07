# EQ Visualizer Integration with Voice Mode

This document describes the integration of EQ visualizers with the chat application's voice mode functionality.

## Overview

When the application is in voice mode and an EQ visualizer is selected, the chat display is automatically replaced with the selected EQ visualizer. The EQ visualizer responds to real-time audio levels from the microphone input, providing a visual representation of the audio being captured.

## Features

### Automatic Display Switching
- When voice mode is activated and an EQ visualizer is selected, the chat display is automatically replaced with the EQ visualizer
- When voice mode is deactivated or EQ visualizer is set to "None", the chat display is restored
- The switching is seamless and maintains the application's UI state

### Real-time Audio Visualization
- EQ visualizers receive audio level data from the recording service
- Audio levels are converted to frequency data for visualization
- Multiple EQ visualizer types are available:
  - **Circle EQ**: Circular frequency visualization with color-coded sections
  - **Bar EQ**: Traditional bar-style equalizer display
  - **Circular Net EQ**: Network-style circular visualization
  - **Circular Gradient EQ**: Gradient-based circular visualization

### Voice Settings Integration
- EQ visualizer selection is integrated into the voice settings dialog
- Settings are persisted and restored between sessions
- EQ visualizer mode can be changed while in voice mode

## Implementation Details

### Key Components

1. **ChatTab Class** (`pyside_chat/ui/chat_tab.py`)
   - Manages EQ visualizer widgets
   - Handles display switching between chat and EQ
   - Processes audio level signals for EQ updates

2. **EQ Widgets** (`pyside_chat/ui/Audio_visualisers/eq_widgets/`)
   - `circle_eq_widget.py`: Circular frequency visualization
   - `bar_eq_widget.py`: Bar-style equalizer
   - `circular_net_eq_widget.py`: Network-style visualization
   - `circular_gradient_eq_widget.py`: Gradient-based visualization

3. **Voice Service** (`pyside_chat/services/Voice_STT_TTS_SERVICES/voice_service.py`)
   - Provides audio level signals from recording service
   - Stores EQ visualizer settings

4. **Voice Settings Dialog** (`pyside_chat/ui/Widgets/voice_settings_dialog.py`)
   - Allows selection of EQ visualizer mode
   - Persists EQ visualizer settings

### Signal Flow

1. **Audio Capture**: Recording service captures microphone audio
2. **Level Calculation**: Audio levels are calculated in real-time
3. **Signal Emission**: `audio_level_changed` signal is emitted
4. **EQ Update**: Chat tab receives signal and updates EQ visualizer
5. **Visualization**: EQ widget displays frequency data

### Methods

#### ChatTab Class
- `setup_eq_visualizers()`: Initialize EQ widget instances
- `switch_to_eq_visualizer()`: Replace chat display with EQ
- `switch_to_chat_display()`: Restore chat display
- `update_eq_visualizer()`: Update EQ with audio level data
- `update_eq_visualizer_mode()`: Change EQ visualizer mode
- `on_audio_level_changed()`: Handle audio level signals

#### Voice Service
- `get_eq_visualizer()`: Get current EQ visualizer setting
- `update_settings()`: Update voice settings including EQ

## Usage

### Enabling EQ Visualizer

1. Open the voice settings dialog
2. In the "General" tab, find the "EQ Visualizer" section
3. Select an EQ visualizer from the dropdown:
   - **None**: No EQ visualizer (default)
   - **Circle EQ**: Circular frequency display
   - **Bar EQ**: Traditional bar equalizer
   - **Circular Net EQ**: Network-style display
   - **Circular Gradient EQ**: Gradient-based display
4. Click "Save" to apply settings

### Using with Voice Mode

1. Select an EQ visualizer in voice settings
2. Click the voice button to start voice mode
3. The chat display will automatically switch to the EQ visualizer
4. Speak into the microphone to see real-time audio visualization
5. Click the voice button again to stop voice mode and return to chat

### Testing

A test script is provided to verify the integration:
```bash
python pyside_chat/ui/Audio_visualisers/test_eq_integration.py
```

The test script allows you to:
- Select different EQ visualizers
- Toggle voice mode
- See simulated audio levels
- Verify display switching behavior

## Configuration

### Voice Settings
The EQ visualizer setting is stored in the voice settings:
```json
{
  "eq_visualizer": "Circle EQ",
  "stt_api": "whisper",
  "tts_api": "coqui",
  "auto_speak": true
}
```

### Default Values
- **EQ Visualizer**: "None" (no visualization)
- **Audio Level Threshold**: 0.005 (for speech detection)
- **Animation Interval**: 16ms (60 FPS)

## Troubleshooting

### Common Issues

1. **EQ not displaying**: Check that voice mode is active and EQ visualizer is not set to "None"
2. **No audio response**: Verify microphone permissions and audio input settings
3. **Performance issues**: Reduce animation frequency or use simpler EQ visualizer
4. **Display not switching**: Ensure voice service is properly initialized

### Debug Information

Enable debug logging to see detailed information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Key debug messages:
- `"Switched to EQ visualizer: {mode}"`
- `"Switched back to chat display"`
- `"EQ visualizer mode updated to: {mode}"`
- `"Error updating EQ visualizer: {error}"`

## Future Enhancements

### Planned Features
- **FFT-based visualization**: Real frequency analysis instead of simulated data
- **Custom EQ presets**: User-defined frequency response curves
- **Audio file playback**: Visualize audio from files
- **Multiple EQ displays**: Show multiple EQ types simultaneously
- **Color customization**: User-defined color schemes for EQ displays

### Performance Optimizations
- **GPU acceleration**: Use OpenGL for smoother animations
- **Audio buffering**: Optimize audio processing pipeline
- **Memory management**: Better cleanup of EQ widget resources

## Dependencies

### Required Packages
- `PySide6`: Qt framework for UI
- `numpy`: Numerical computations for audio processing
- `sounddevice`: Audio input/output (optional, for real audio)

### Optional Dependencies
- `scipy`: Advanced signal processing (for FFT)
- `matplotlib`: Additional visualization options

## Contributing

When adding new EQ visualizers:

1. Create a new widget class in `eq_widgets/`
2. Implement required methods:
   - `set_eq_sections(values)` or `set_bar_values(values)`
   - `start_animation()` and `stop_animation()`
3. Add the widget to `setup_eq_visualizers()` in ChatTab
4. Update the voice settings dialog to include the new option
5. Test with the integration test script

## License

This integration is part of the Pyside Ollama Chat application and follows the same license terms. 