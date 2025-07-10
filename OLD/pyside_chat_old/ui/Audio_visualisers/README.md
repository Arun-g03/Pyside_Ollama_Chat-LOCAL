# Audio Visualizer - Modular EQ System

This directory contains a modularized audio visualizer system with multiple EQ visualization modes.

## Structure

```
Audio_visualisers/
├── eq_orchestrator.py          # Main orchestrator that manages all EQ widgets
├── eq_widgets/                 # Individual EQ widget modules
│   ├── __init__.py            # Package initialization
│   ├── circle_eq_widget.py    # Circular EQ visualizer
│   ├── bar_eq_widget.py       # Bar EQ visualizer
│   ├── circular_net_eq_widget.py      # Circular net visualizer
│   └── circular_gradient_eq_widget.py # Circular gradient visualizer
├── test_modular_eq.py         # Test script for the modular system
├── voice_ring_animation.py    # Original monolithic file (legacy)
└── README.md                  # This file
```

## EQ Widgets

### 1. CircleEQWidget (`circle_eq_widget.py`)
- **Purpose**: Displays audio frequency data in circular sections
- **Features**: 
  - 24 circular sections with smooth animations
  - Frequency-based color coding (bass, mid, treble)
  - Radial gradients for visual appeal
- **Usage**: `CircleEQWidget(parent=None, num_sections=24)`

### 2. BarEQWidget (`bar_eq_widget.py`)
- **Purpose**: Traditional bar equalizer with animated vertical bars
- **Features**:
  - 48 frequency bars with reflection effects
  - Smooth interpolation between target values
  - Frequency-based color gradients
- **Usage**: `BarEQWidget(parent=None, num_bars=48)`

### 3. CircularNetEQWidget (`circular_net_eq_widget.py`)
- **Purpose**: Vanta.js-inspired circular net with connected points
- **Features**:
  - 64 points around a circle with organic motion
  - Glowing connecting lines
  - Customizable colors per net
- **Usage**: `CircularNetEQWidget(parent=None, num_points=64, color=(80,180,255))`

### 4. CircularGradientEQWidget (`circular_gradient_eq_widget.py`)
- **Purpose**: Fills circular area with soft gradient based on audio
- **Features**:
  - Smooth gradient fills
  - Glowing outlines
  - Configurable alpha, radius scale, and energy multiplier
- **Usage**: `CircularGradientEQWidget(parent=None, num_points=64, color=(80,180,255), alpha=120)`

## Main Orchestrator

### eq_orchestrator.py
The main orchestrator file that:
- Manages all EQ widgets
- Handles audio input (file or microphone)
- Provides mode switching between different visualizers
- Manages audio presets and device selection
- Coordinates audio processing and visualization updates

**Key Features**:
- 5 visualization modes (Circle EQ, Bar EQ, Waveform EQ, Waveform Gradient, Waveform Blue Gradient)
- Real-time audio processing with FFT analysis
- Microphone input support
- Audio file playback
- Preset management

## Usage

### Running the Visualizer
```python
from eq_orchestrator import MainWindow
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())
```

### Using Individual Widgets
```python
from eq_widgets.circle_eq_widget import CircleEQWidget
from eq_widgets.bar_eq_widget import BarEQWidget

# Create widgets
circle_eq = CircleEQWidget()
bar_eq = BarEQWidget()

# Update with frequency data
circle_eq.set_eq_sections([0.1, 0.5, 0.8, ...])
bar_eq.set_eq_bars([0.1, 0.3, 0.7, ...])
```

## Testing

Run the test script to verify the modularization:
```bash
cd pyside_chat/ui/Audio_visualisers
python test_modular_eq.py
```

## Audio Processing

The system uses FFT (Fast Fourier Transform) to analyze audio frequency content:
- **Sample Rate**: 44100 Hz
- **FFT Size**: 2048 samples
- **Frequency Bands**: Bass (20-250 Hz), Low Mid (250-500 Hz), Mid (500-2000 Hz), High Mid (2000-4000 Hz), Treble (4000-20000 Hz)

## Configuration

### Audio Presets
Edit `AUDIO_PRESETS` in `eq_orchestrator.py` to add your audio files:
```python
AUDIO_PRESETS = {
    "My Music": r"path/to/your/music.mp3",
    "Test Audio": r"path/to/test.wav",
    # Add more presets...
}
```

### Widget Configuration
Each widget has configurable parameters:
- Animation intervals (16ms for 60 FPS)
- Smoothing factors (0.18 for smooth transitions)
- Visual ratios and dimensions
- Color schemes and alpha values

## Migration from Legacy

The original `voice_ring_animation.py` file is preserved for reference. The new modular system provides:
- **Better organization**: Each EQ type is in its own file
- **Easier maintenance**: Changes to one EQ don't affect others
- **Reusability**: Individual widgets can be used independently
- **Testability**: Each component can be tested separately
- **Extensibility**: New EQ types can be added easily

## Adding New EQ Widgets

To add a new EQ widget:

1. Create a new file in `eq_widgets/` (e.g., `new_eq_widget.py`)
2. Inherit from `QWidget` and implement the standard interface:
   - `set_eq_sections(values)` or `set_eq_bars(values)` method
   - `start_animation()` and `stop_animation()` methods
   - `set_idle()` method
   - `paintEvent()` method
3. Add the widget to `eq_widgets/__init__.py`
4. Import and integrate it in `eq_orchestrator.py`

## Dependencies

- PySide6 (Qt6 bindings)
- numpy (for FFT calculations)
- sounddevice (for audio input/output)
- soundfile (for audio file reading)

## Performance Notes

- Animation runs at 60 FPS by default
- FFT processing is done in real-time
- Widget updates are thread-safe using Qt signals
- Memory usage scales with the number of frequency bins and animation complexity 