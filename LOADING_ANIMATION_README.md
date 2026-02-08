# Loading Wave Animation

This feature adds a beautiful wave-like loading animation with 3/4 dots that appears when users are waiting for AI responses.

## Overview

The loading animation consists of animated dots that move in a wave pattern to indicate that the system is processing or waiting for a response. The animation is automatically shown when streaming starts and hidden when streaming stops.

## Features

- **Wave Effect**: Dots move up and down in a wave pattern
- **Opacity Animation**: Dots fade in and out based on their wave position
- **Smooth Animation**: 60 FPS animation with smooth interpolation
- **Customizable**: Configurable number of dots, size, spacing, and animation parameters
- **Automatic Integration**: Automatically shows/hides with streaming state

## Implementation

### LoadingWaveWidget

The main widget is located at `pyside_chat/ui/Widgets/loading_wave_widget.py`.

**Key Features:**
- Configurable number of dots (default: 4)
- Adjustable dot size and spacing
- Customizable animation speed, wave amplitude, and frequency
- Color customization
- Automatic start/stop with visibility

**Usage:**
```python
from pyside_chat.ui.Widgets.loading_wave_widget import LoadingWaveWidget

# Create widget
loading_widget = LoadingWaveWidget(
    num_dots=4,           # Number of dots
    dot_size=8,           # Size of each dot in pixels
    spacing=12,           # Spacing between dots
    animation_speed=0.8,  # Animation speed
    wave_amplitude=0.3,   # Wave amplitude
    wave_frequency=2.0    # Wave frequency
)

# Start animation
loading_widget.start_animation()

# Stop animation
loading_widget.stop_animation()

# Check if animating
if loading_widget.is_animating():
    print("Animation is running")

# Customize appearance
loading_widget.set_dot_color(QColor(0, 120, 212))  # Blue color
loading_widget.set_animation_speed(1.0)  # Faster animation
loading_widget.set_wave_amplitude(0.5)   # Larger wave
```

### Integration with Chat Display

The loading animation is integrated into the chat display at `pyside_chat/ui/tabs/chat_tab/chat_display.py`.

**Methods Added:**
- `show_loading_animation()`: Shows and starts the loading animation
- `hide_loading_animation()`: Hides and stops the loading animation

### Integration with Chat Tab

The chat tab automatically manages the loading animation based on streaming state:

- **Streaming Start**: Shows loading animation
- **Streaming Stop**: Hides loading animation
- **Emergency Reset**: Hides loading animation

## Testing

A test script is provided at `test_loading_animation.py` to demonstrate the loading animation:

```bash
python test_loading_animation.py
```

This will open a test window where you can:
- Start/stop the animation
- See the wave effect in action
- Test different configurations

## Configuration

The loading animation can be customized through various parameters:

### Visual Parameters
- `num_dots`: Number of dots (default: 4)
- `dot_size`: Size of each dot in pixels (default: 8)
- `spacing`: Spacing between dots in pixels (default: 12)
- `dot_color`: Color of the dots (default: Blue)

### Animation Parameters
- `animation_speed`: Speed of the animation (default: 0.8)
- `wave_amplitude`: Amplitude of the wave effect (default: 0.3)
- `wave_frequency`: Frequency of the wave effect (default: 2.0)

## Technical Details

### Animation System
- Uses QTimer for smooth 60 FPS animation
- Sine wave calculations for wave effect
- Opacity interpolation for fade effects
- Automatic cleanup when widget is hidden

### Performance
- Lightweight implementation
- Minimal CPU usage
- Automatic timer management
- Efficient painting with QPainter

### Thread Safety
- All UI updates are thread-safe
- Uses QTimer.singleShot for cross-thread updates
- Proper signal/slot connections

## Usage in the Application

The loading animation is automatically integrated into the chat interface:

1. **User sends message** → Loading animation appears
2. **AI starts responding** → Loading animation continues
3. **AI finishes responding** → Loading animation disappears

The animation provides visual feedback that the system is processing the user's request and waiting for the AI response.

## Customization Examples

### Different Colors
```python
# Green loading animation
loading_widget.set_dot_color(QColor(0, 255, 0))

# Red loading animation  
loading_widget.set_dot_color(QColor(255, 0, 0))

# Purple loading animation
loading_widget.set_dot_color(QColor(128, 0, 128))
```

### Different Animation Styles
```python
# Fast, large wave
loading_widget.set_animation_speed(1.5)
loading_widget.set_wave_amplitude(0.8)

# Slow, subtle wave
loading_widget.set_animation_speed(0.3)
loading_widget.set_wave_amplitude(0.1)
```

### Different Dot Configurations
```python
# 3 dots, small
loading_widget = LoadingWaveWidget(num_dots=3, dot_size=6, spacing=8)

# 5 dots, large
loading_widget = LoadingWaveWidget(num_dots=5, dot_size=12, spacing=16)
```

## Future Enhancements

Potential improvements for the loading animation:

1. **Multiple Animation Styles**: Different wave patterns
2. **Color Themes**: Match application theme
3. **Sound Integration**: Optional audio feedback
4. **Progress Indication**: Show progress percentage
5. **Custom Wave Shapes**: Different mathematical functions
6. **Responsive Design**: Adapt to different screen sizes

## Troubleshooting

### Animation Not Showing
- Check if the widget is visible
- Verify that `start_animation()` was called
- Ensure the parent widget is properly sized

### Animation Not Smooth
- Check system performance
- Verify timer interval (should be ~16ms for 60 FPS)
- Ensure no blocking operations in main thread

### Memory Issues
- Animation automatically stops when widget is hidden
- Timer is properly managed and cleaned up
- No memory leaks in the implementation 