import sys
import math
import random
from PySide6.QtCore import Qt, QTimer, QMetaObject, Slot, Signal
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush, QRadialGradient, QPainterPath, QTransform, QPen
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QCheckBox
)
import threading
import sounddevice as sd
import soundfile as sf
import numpy as np
import os

# Optional: Hardcode an audio path here
HARDCODED_AUDIO_PATH = r"C:\Users\arun-\iCloudDrive\notaBIGFAN.mp3"

# Additional audio file paths for presets
AUDIO_PRESETS = {
    "Nota BIGFAN": r"C:\Users\arun-\iCloudDrive\notaBIGFAN.mp3",
    "TTS Output": r"C:\Users\arun-\AppData\Local\Temp\tts_user_models\tts_output.wav",
    "LOTR Passage": r"C:\Users\arun-\AppData\Local\Temp\tts_user_models\Lord_Of_rings_Passage_tts_output.wav",  # Add your music files here
    "Sample 2": r"C:\Users\arun-\Music\sample2.mp3",
    "Sample 3": r"C:\Users\arun-\Music\sample3.mp3",
    "Test Audio": r"C:\Users\arun-\Downloads\test_audio.wav"
}

BAR_EQ_MULTIPLIER = 1 # Increase for more sensitive/taller bars, decrease for less

# Frequency band mapping for proper EQ visualization
# Standard frequency ranges for audio equalization
FREQ_BANDS = {
    'bass': (20, 250),      # Bass: 20-250 Hz
    'low_mid': (250, 500),   # Low Mid: 250-500 Hz  
    'mid': (500, 2000),      # Mid: 500-2000 Hz
    'high_mid': (2000, 4000), # High Mid: 2000-4000 Hz
    'treble': (4000, 20000)  # Treble: 4000-20000 Hz
}

# Bar distribution across frequency bands
BAR_DISTRIBUTION = {
    'bass': 0.25,        # 25% of bars for bass (bars 0-11)
    'low_mid': 0.15,     # 15% of bars for low mid (bars 12-19)
    'mid': 0.25,         # 25% of bars for mid (bars 20-31)
    'high_mid': 0.15,    # 15% of bars for high mid (bars 32-39)
    'treble': 0.20       # 20% of bars for treble (bars 40-47)
}

def map_frequency_to_bars(fft_magnitude, sample_rate, num_bars=48):
    """
    Map FFT frequency bins to bar ranges based on frequency bands.
    
    Args:
        fft_magnitude: FFT magnitude array
        sample_rate: Audio sample rate
        num_bars: Number of bars to generate
        
    Returns:
        list: Bar values mapped to frequency bands
    """
    # Calculate frequency resolution
    freq_resolution = sample_rate / (2 * len(fft_magnitude))
    
    # Calculate bar distribution
    bars_per_band = {}
    current_bar = 0
    for band, ratio in BAR_DISTRIBUTION.items():
        bars_in_band = int(num_bars * ratio)
        bars_per_band[band] = (current_bar, current_bar + bars_in_band)
        current_bar += bars_in_band
    
    # Ensure we use all bars
    if current_bar < num_bars:
        bars_per_band['treble'] = (bars_per_band['treble'][0], num_bars)
    
    # Map frequency bins to bars
    bar_values = [0.1] * num_bars  # Start with minimum values
    
    for band, (low_freq, high_freq) in FREQ_BANDS.items():
        if band not in bars_per_band:
            continue
            
        start_bar, end_bar = bars_per_band[band]
        bars_in_band = end_bar - start_bar
        
        # Find frequency bin range for this band
        low_bin = int(low_freq / freq_resolution)
        high_bin = int(high_freq / freq_resolution)
        high_bin = min(high_bin, len(fft_magnitude) - 1)
        
        if low_bin >= high_bin:
            continue
            
        # Get magnitude values for this frequency band
        band_magnitude = fft_magnitude[low_bin:high_bin + 1]
        
        if len(band_magnitude) == 0:
            continue
            
        # Split band magnitude into bars
        if bars_in_band > 0:
            bins_per_bar = max(1, len(band_magnitude) // bars_in_band)
            
            for i in range(bars_in_band):
                start_idx = i * bins_per_bar
                end_idx = min(start_idx + bins_per_bar, len(band_magnitude))
                
                if start_idx < len(band_magnitude):
                    # Calculate RMS energy for this bar's frequency range
                    bar_bins = band_magnitude[start_idx:end_idx]
                    if len(bar_bins) > 0:
                        energy = float(np.sqrt(np.mean(bar_bins**2))) * BAR_EQ_MULTIPLIER
                        bar_values[start_bar + i] = energy
    
    return bar_values

class CircleEQWidget(QWidget):
    """
    A simplified circular equalizer widget that displays audio frequency data in circular sections.
    
    This widget renders frequency data in circular sections, similar to the bar EQ but in a circular format.
    Each section represents a frequency band (bass, mid, treble) with smooth animations.
    """
    
    # Configuration constants
    DEFAULT_NUM_SECTIONS = 24  # Number of circular sections (increased from 12 for more detail)
    DEFAULT_ANIMATION_INTERVAL = 16  # milliseconds (60 FPS) - Options: 33ms (30 FPS), 16ms (60 FPS), 8ms (120 FPS)
    DEFAULT_IDLE_VALUE = 0.1
    ANIMATION_SMOOTHING_FACTOR = 0.18
    
    # Visual configuration
    CIRCLE_RADIUS_RATIO = 0.35  # Percentage of widget size for circle radius
    INNER_RADIUS_RATIO = 0.15   # Percentage for inner circle (hole)
    
    def __init__(self, parent=None, num_sections=None):
        """
        Initialize the circular equalizer widget.
        
        Args:
            parent: Parent widget
            num_sections: Number of circular sections (default: DEFAULT_NUM_SECTIONS)
        """
        super().__init__(parent)
        
        # Initialize configuration
        self.num_sections = num_sections or self.DEFAULT_NUM_SECTIONS
        self.setMinimumSize(500, 500)
        
        # Initialize data arrays
        self._section_values = [self.DEFAULT_IDLE_VALUE] * self.num_sections
        self._target_values = [self.DEFAULT_IDLE_VALUE] * self.num_sections
        
        # Setup animation timer
        self._setup_animation_timer()
        
        # State tracking
        self._is_idle = True

    def _setup_animation_timer(self):
        """Initialize and configure the animation timer."""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)

    def _animate(self):
        """
        Animate the sections by smoothly interpolating current values toward target values.
        This method is called by the timer to update the visual state.
        """
        # Animation smoothing
        for i in range(self.num_sections):
            current = self._section_values[i]
            target = self._target_values[i]
            self._section_values[i] += (target - current) * self.ANIMATION_SMOOTHING_FACTOR
        
        self.update()

    @Slot(list)
    def set_eq_sections(self, values):
        """
        Set the target values for the circular sections.
        
        Args:
            values: List of float values representing target section heights (0.1 to 1.0)
        """
        if not values:
            # Handle empty input
            self._target_values = [self.DEFAULT_IDLE_VALUE] * self.num_sections
            self._is_idle = True
            return
            
        # Ensure values are in valid range [0.1, 1.0]
        validated_values = []
        for val in values:
            if isinstance(val, (int, float)):
                # Clamp to valid range
                clamped_val = max(0.1, min(1.0, float(val)))
                validated_values.append(clamped_val)
            else:
                # Invalid value, use default
                validated_values.append(self.DEFAULT_IDLE_VALUE)
        
        # Handle array length mismatch
        if len(validated_values) != self.num_sections:
            if len(validated_values) > self.num_sections:
                # Truncate to fit
                validated_values = validated_values[:self.num_sections]
            else:
                # Pad with default values
                validated_values.extend([self.DEFAULT_IDLE_VALUE] * (self.num_sections - len(validated_values)))
        
        self._target_values = validated_values
        self._is_idle = False

    def set_idle(self):
        """Reset all sections to their idle state."""
        self._target_values = [self.DEFAULT_IDLE_VALUE] * self.num_sections
        self._is_idle = True

    def start_animation(self):
        """Start the animation timer."""
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)

    def stop_animation(self):
        """Stop the animation timer."""
        self._timer.stop()

    def get_current_values(self):
        """
        Get current section values for debugging/monitoring.
        
        Returns:
            dict: Current state information
        """
        return {
            'section_values': self._section_values.copy(),
            'target_values': self._target_values.copy(),
            'is_idle': self._is_idle,
            'num_sections': self.num_sections
        }

    def _create_section_gradient(self, center_x, center_y, inner_radius, outer_radius, angle_start, angle_span, value, section_index):
        """
        Create a gradient for a circular section.
        
        Args:
            center_x, center_y: Center of the circle
            inner_radius, outer_radius: Inner and outer radii
            angle_start, angle_span: Start angle and span in radians
            value: Section value (0.1 to 1.0)
            section_index: Index of the section for frequency-based coloring
            
        Returns:
            QRadialGradient: Configured gradient for the section
        """
        # Determine color based on frequency band (24 sections)
        bass_end = int(self.num_sections * 0.33)  # First 33% - bass (sections 0-7)
        mid_end = int(self.num_sections * 0.67)   # Next 34% - mid (sections 8-15)
        # Remaining 33% - treble (sections 16-23)
        
        if section_index < bass_end:
            # Bass - deep blue to purple
            colors = [(80, 120, 255), (180, 80, 255)]
        elif section_index < mid_end:
            # Mid - red to orange
            colors = [(255, 80, 80), (255, 160, 80)]
        else:
            # Treble - yellow to bright green
            colors = [(255, 240, 80), (120, 255, 120)]
        
        # Calculate radius based on value
        radius = inner_radius + (outer_radius - inner_radius) * value
        
        # Create radial gradient
        gradient = QRadialGradient(center_x, center_y, radius)
        gradient.setColorAt(0.0, QColor(colors[0][0], colors[0][1], colors[0][2], 200))
        gradient.setColorAt(0.7, QColor(colors[1][0], colors[1][1], colors[1][2], 150))
        gradient.setColorAt(1.0, QColor(colors[1][0], colors[1][1], colors[1][2], 0))
        
        return gradient

    def paintEvent(self, event):
        """
        Paint the circular equalizer widget.
        
        Args:
            event: Paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill background
        painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0))
        
        # Calculate circle geometry
        w, h = self.width(), self.height()
        center_x, center_y = w / 2, h / 2
        max_radius = min(w, h) * self.CIRCLE_RADIUS_RATIO
        inner_radius = min(w, h) * self.INNER_RADIUS_RATIO
        
        # Draw sections
        angle_step = 2 * math.pi / self.num_sections
        
        for i, value in enumerate(self._section_values):
            angle_start = i * angle_step
            angle_span = angle_step
            
            # Create gradient for this section
            gradient = self._create_section_gradient(
                center_x, center_y, inner_radius, max_radius, 
                angle_start, angle_span, value, i
            )
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.NoPen)
            
            # Draw section as a pie slice
            painter.drawPie(
                center_x - max_radius, center_y - max_radius,
                max_radius * 2, max_radius * 2,
                int(angle_start * 180 / math.pi * 16),  # Convert to Qt angle units
                int(angle_span * 180 / math.pi * 16)
            )

class BarEQWidget(QWidget):
    """
    A bar equalizer widget that displays audio frequency data as animated bars.
    
    This widget renders a series of vertical bars that respond to audio frequency data,
    creating a visual equalizer effect. The bars animate smoothly between target values
    and include reflection effects for enhanced visual appeal.
    """
    
    # Configuration constants
    DEFAULT_NUM_BARS = 48
    DEFAULT_ANIMATION_INTERVAL = 20  # milliseconds (60 FPS) - Options: 33ms (30 FPS), 16ms (60 FPS), 8ms (120 FPS)
    DEFAULT_IDLE_VALUE = 0.1  # Changed back to 0.1 so bars are visible when idle
    ANIMATION_SMOOTHING_FACTOR = 0.18
    
    # Visual configuration
    BAR_HEIGHT_RATIO = 0.38  # Percentage of widget height for max bar height
    BASE_Y_RATIO = 0.48      # Y position for bar base
    BAR_WIDTH_RATIO = 2      # Number of bars per width unit
    
    def __init__(self, parent=None, num_bars=None):
        """
        Initialize the bar equalizer widget.
        
        Args:
            parent: Parent widget
            num_bars: Number of frequency bars to display (default: DEFAULT_NUM_BARS)
        """
        super().__init__(parent)
        
        # Initialize configuration
        self.num_bars = num_bars or self.DEFAULT_NUM_BARS
        self.setMinimumSize(800, 400)
        
        # Initialize data arrays
        self._bar_values = [self.DEFAULT_IDLE_VALUE] * self.num_bars
        self._target_values = [self.DEFAULT_IDLE_VALUE] * self.num_bars
        
        # Setup animation timer
        self._setup_animation_timer()
        
        # State tracking
        self._is_idle = True

    def _setup_animation_timer(self):
        """Initialize and configure the animation timer."""
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)

    def _animate(self):
        """
        Animate the bars by smoothly interpolating current values toward target values.
        This method is called by the timer to update the visual state.
        """
        for i in range(self.num_bars):
            current = self._bar_values[i]
            target = self._target_values[i]
            self._bar_values[i] += (target - current) * self.ANIMATION_SMOOTHING_FACTOR
        
        self.update()

    @Slot(list)
    def set_eq_bars(self, values):
        """
        Set the target values for the frequency bars.
        
        Args:
            values: List of float values representing target bar heights (0.0 to 1.0)
        """
        if not values:
            # Handle empty input
            self._target_values = [self.DEFAULT_IDLE_VALUE] * self.num_bars
            self._is_idle = True
            return
            
        # Ensure values are in valid range [0.1, 1.0]
        validated_values = []
        for val in values:
            if isinstance(val, (int, float)):
                # Clamp to valid range
                clamped_val = max(0.1, min(1.0, float(val)))
                validated_values.append(clamped_val)
            else:
                # Invalid value, use default
                validated_values.append(self.DEFAULT_IDLE_VALUE)
        
        # Handle array length mismatch
        if len(validated_values) != self.num_bars:
            if len(validated_values) > self.num_bars:
                # Truncate to fit
                validated_values = validated_values[:self.num_bars]
            else:
                # Pad with default values
                validated_values.extend([self.DEFAULT_IDLE_VALUE] * (self.num_bars - len(validated_values)))
        
        self._target_values = validated_values
        self._is_idle = False

    def set_idle(self):
        """Reset all bars to their idle state."""
        self._target_values = [self.DEFAULT_IDLE_VALUE] * self.num_bars
        self._is_idle = True

    def start_animation(self):
        """Start the animation timer."""
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)

    def stop_animation(self):
        """Stop the animation timer."""
        self._timer.stop()

    def get_current_values(self):
        """
        Get current bar values for debugging/monitoring.
        
        Returns:
            dict: Current state information
        """
        return {
            'bar_values': self._bar_values.copy(),
            'target_values': self._target_values.copy(),
            'is_idle': self._is_idle,
            'num_bars': self.num_bars
        }

    def _calculate_bar_geometry(self, widget_width, widget_height):
        """
        Calculate bar dimensions and positioning.
        
        Args:
            widget_width: Width of the widget
            widget_height: Height of the widget
            
        Returns:
            dict: Geometry information for rendering bars
        """
        bar_width = widget_width // (self.num_bars * self.BAR_WIDTH_RATIO)
        gap = bar_width // 2
        max_bar_height = int(widget_height * self.BAR_HEIGHT_RATIO)
        base_y = int(widget_height * self.BASE_Y_RATIO)
        
        return {
            'bar_width': bar_width,
            'gap': gap,
            'max_bar_height': max_bar_height,
            'base_y': base_y
        }

    def _create_bar_gradient(self, x, y, width, height, is_reflection=False, bar_index=0):
        """
        Create a gradient for a bar.
        
        Args:
            x: X position of the bar
            y: Y position of the bar
            width: Width of the bar
            height: Height of the bar
            is_reflection: Whether this is a reflection gradient
            bar_index: Index of the bar for frequency-based coloring
            
        Returns:
            QLinearGradient: Configured gradient for the bar
        """
        # Determine color based on frequency band
        num_bars = self.num_bars
        bass_end = int(num_bars * 0.25)  # First 25% - bass
        low_mid_end = int(num_bars * 0.40)  # Next 15% - low mid
        mid_end = int(num_bars * 0.65)  # Next 25% - mid
        high_mid_end = int(num_bars * 0.80)  # Next 15% - high mid
        # Remaining 20% - treble
        
        if bar_index < bass_end:
            # Bass - deep blue to purple
            colors = [(80, 120, 255), (120, 80, 255), (180, 80, 255)]
        elif bar_index < low_mid_end:
            # Low Mid - purple to red
            colors = [(180, 80, 255), (255, 80, 180), (255, 80, 120)]
        elif bar_index < mid_end:
            # Mid - red to orange
            colors = [(255, 80, 80), (255, 120, 80), (255, 160, 80)]
        elif bar_index < high_mid_end:
            # High Mid - orange to yellow
            colors = [(255, 160, 80), (255, 200, 80), (255, 240, 80)]
        else:
            # Treble - yellow to bright green
            colors = [(255, 240, 80), (200, 255, 80), (120, 255, 120)]
        
        if is_reflection:
            # Reflection gradient (mirrored and semi-transparent)
            gradient = QLinearGradient(x, y, x, y + height)
            gradient.setColorAt(0.0, QColor(colors[0][0], colors[0][1], colors[0][2], 120))
            gradient.setColorAt(0.5, QColor(colors[1][0], colors[1][1], colors[1][2], 60))
            gradient.setColorAt(1.0, QColor(colors[2][0], colors[2][1], colors[2][2], 0))
        else:
            # Main bar gradient
            gradient = QLinearGradient(x, y - height, x, y)
            gradient.setColorAt(0.0, QColor(colors[0][0], colors[0][1], colors[0][2]))
            gradient.setColorAt(0.5, QColor(colors[1][0], colors[1][1], colors[1][2]))
            gradient.setColorAt(1.0, QColor(colors[2][0], colors[2][1], colors[2][2]))
        
        return gradient

    def _draw_bar(self, painter, x, y, width, height, value, max_height, bar_index=0):
        """
        Draw a single bar with its reflection.
        
        Args:
            painter: QPainter instance
            x: X position of the bar
            y: Y position of the bar base
            width: Width of the bar
            height: Height of the bar
            value: Current bar value (0.0 to 1.0)
            max_height: Maximum possible bar height
            bar_index: Index of the bar for frequency-based coloring
        """
        # Calculate actual bar height based on value
        bar_height = int(value * max_height)
        
        # Draw main bar
        main_gradient = self._create_bar_gradient(x, y, width, bar_height, bar_index=bar_index)
        painter.setBrush(QBrush(main_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRect(x, y - bar_height, width, bar_height)
        
        # Draw reflection
        if bar_height > 0:
            reflection_gradient = self._create_bar_gradient(x, y, width, bar_height, is_reflection=True, bar_index=bar_index)
            painter.setBrush(QBrush(reflection_gradient))
            painter.drawRect(x, y, width, bar_height)

    def paintEvent(self, event):
        """
        Paint the bar equalizer widget.
        
        Args:
            event: Paint event
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill background
        painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0))
        
        # Calculate geometry
        geometry = self._calculate_bar_geometry(self.width(), self.height())
        
        # Draw all bars
        for i, value in enumerate(self._bar_values):
            x = geometry['gap'] + i * (geometry['bar_width'] + geometry['gap'])
            self._draw_bar(
                painter, 
                x, 
                geometry['base_y'], 
                geometry['bar_width'], 
                geometry['max_bar_height'], 
                value, 
                geometry['max_bar_height'],
                i
            )

class CircularNetEQWidget(QWidget):
    """
    A Vanta.js-inspired circular net visualizer: points around a circle, connected by glowing lines, with organic motion and optional audio reactivity.
    Now supports custom color for each net.
    """
    DEFAULT_NUM_POINTS = 64
    DEFAULT_ANIMATION_INTERVAL = 16  # ~60 FPS
    DEFAULT_IDLE_VALUE = 0.1
    ANIMATION_SMOOTHING_FACTOR = 0.18
    RADIUS_RATIO = 0.32
    GLOW_WIDTH = 12
    CONNECTIONS = 3  # How many neighbors to connect to (on each side)

    def __init__(self, parent=None, num_points=None, color=None):
        super().__init__(parent)
        self.setMinimumSize(500, 500)
        self.num_points = num_points or self.DEFAULT_NUM_POINTS
        self._base_radius = self.DEFAULT_IDLE_VALUE
        self._point_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
        self._target_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
        self._noise_offsets = [random.uniform(0, 1000) for _ in range(self.num_points)]
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)
        self._is_idle = True
        self._t = 0
        # Color for this net (QColor or tuple)
        if color is None:
            self.color = QColor(80, 120, 255)  # Default blue
        elif isinstance(color, tuple):
            self.color = QColor(*color)
        else:
            self.color = color

    def _animate(self):
        self._t += 0.015
        for i in range(self.num_points):
            # Organic motion: combine target radius (audio) and smooth noise
            noise = math.sin(self._t + self._noise_offsets[i]) * 0.18 + math.sin(self._t * 0.7 + self._noise_offsets[i] * 0.5) * 0.08
            target = self._target_radii[i] + noise
            self._point_radii[i] += (target - self._point_radii[i]) * self.ANIMATION_SMOOTHING_FACTOR
        self.update()

    @Slot(list)
    def set_net_radii(self, values):
        if not values:
            self._target_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
            self._is_idle = True
            return
        validated = []
        for v in values:
            if isinstance(v, (int, float)):
                validated.append(max(0.1, min(1.0, float(v))))
            else:
                validated.append(self.DEFAULT_IDLE_VALUE)
        if len(validated) != self.num_points:
            if len(validated) > self.num_points:
                validated = validated[:self.num_points]
            else:
                validated.extend([self.DEFAULT_IDLE_VALUE] * (self.num_points - len(validated)))
        self._target_radii = validated
        self._is_idle = False

    def set_idle(self):
        self._target_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
        self._is_idle = True

    def start_animation(self):
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)
    def stop_animation(self):
        self._timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        base_radius = min(w, h) * self.RADIUS_RATIO
        # Do not fill background, let parent show through
        # Transparent background for overlay
        # painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        # painter.fillRect(0, 0, w, h, Qt.transparent)
        # Calculate points
        points = []
        for i, val in enumerate(self._point_radii):
            angle = 2 * math.pi * i / self.num_points
            r = base_radius + (val - 0.1) * base_radius * 1.1
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        # Draw glowing lines (multiple strokes for glow)
        for glow in range(self.GLOW_WIDTH, 0, -3):
            alpha = int(30 + 60 * (glow / self.GLOW_WIDTH))
            color = QColor(self.color)
            color.setAlpha(alpha)
            pen = color
            painter.setPen(pen)
            for i in range(self.num_points):
                for j in range(1, self.CONNECTIONS + 1):
                    k = (i + j) % self.num_points
                    painter.drawLine(
                        int(points[i][0]), int(points[i][1]),
                        int(points[k][0]), int(points[k][1])
                    )
        # Draw main net (brighter lines)
        main_color = QColor(self.color)
        main_color.setAlpha(200)
        painter.setPen(main_color)
        for i in range(self.num_points):
            for j in range(1, self.CONNECTIONS + 1):
                k = (i + j) % self.num_points
                painter.drawLine(
                    int(points[i][0]), int(points[i][1]),
                    int(points[k][0]), int(points[k][1])
                )
        # Draw points as glowing dots
        dot_color = QColor(self.color)
        dot_color.setAlpha(180)
        for i, (x, y) in enumerate(points):
            painter.setBrush(dot_color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(x) - 3, int(y) - 3, 7, 7)

class CircularGradientEQWidget(QWidget):
    """
    Like CircularNetEQWidget, but fills the area defined by the animated points with a soft, faded gradient (no lines or dots).
    """
    DEFAULT_NUM_POINTS = 64
    DEFAULT_ANIMATION_INTERVAL = 16  # ~60 FPS
    DEFAULT_IDLE_VALUE = 0.1
    ANIMATION_SMOOTHING_FACTOR = 0.18
    RADIUS_RATIO = 0.32

    def __init__(self, parent=None, num_points=None, color=None, alpha=120, radius_scale=1.0, radius_ratio=None, energy_mult=None):
        super().__init__(parent)
        self.setMinimumSize(500, 500)
        self.num_points = num_points or self.DEFAULT_NUM_POINTS
        self._base_radius = self.DEFAULT_IDLE_VALUE
        self._point_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
        self._target_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
        self._noise_offsets = [random.uniform(0, 1000) for _ in range(self.num_points)]
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)
        self._is_idle = True
        self._t = 0
        if color is None:
            self.color = QColor(80, 120, 255)
        elif isinstance(color, tuple):
            self.color = QColor(*color)
        else:
            self.color = color
        self.alpha = alpha
        self.radius_scale = radius_scale
        self.radius_ratio = radius_ratio
        self.energy_mult = energy_mult

    def _smooth_radii(self, radii, window=5):
        n = len(radii)
        smoothed = []
        for i in range(n):
            vals = [radii[(i + j - window//2) % n] for j in range(window)]
            smoothed.append(sum(vals) / window)
        return smoothed

    def _animate(self):
        self._t += 0.015
        for i in range(self.num_points):
            noise = math.sin(self._t + self._noise_offsets[i]) * 0.18 + math.sin(self._t * 0.7 + self._noise_offsets[i] * 0.5) * 0.08
            target = self._target_radii[i] + noise
            self._point_radii[i] += (target - self._point_radii[i]) * self.ANIMATION_SMOOTHING_FACTOR
        self.update()

    @Slot(list)
    def set_net_radii(self, values):
        if not values:
            self._target_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
            self._is_idle = True
            return
        validated = []
        for v in values:
            if isinstance(v, (int, float)):
                validated.append(max(0.25, min(1.0, float(v))))
            else:
                validated.append(self.DEFAULT_IDLE_VALUE)
        if len(validated) != self.num_points:
            if len(validated) > self.num_points:
                validated = validated[:self.num_points]
            else:
                validated.extend([self.DEFAULT_IDLE_VALUE] * (self.num_points - len(validated)))
        self._target_radii = validated
        self._is_idle = False

    def set_idle(self):
        self._target_radii = [self.DEFAULT_IDLE_VALUE] * self.num_points
        # Do not reset self._point_radii, let animation interpolate
        self._is_idle = True
        self.start_animation()  # Ensure timer is running for smooth return

    def start_animation(self):
        self._timer.start(self.DEFAULT_ANIMATION_INTERVAL)
    def stop_animation(self):
        self._timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        ratio = self.radius_ratio if self.radius_ratio is not None else self.RADIUS_RATIO
        base_radius = min(w, h) * ratio
        base_radius *= self.radius_scale
        energy_mult = self.energy_mult if self.energy_mult is not None else 1.1
        # Smooth the radii
        smoothed_radii = self._smooth_radii(self._point_radii, window=5)
        # Calculate points
        points = []
        for i, val in enumerate(smoothed_radii):
            angle = 2 * math.pi * i / self.num_points
            r = base_radius + (val - 0.25) * base_radius * energy_mult
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        # Create a smooth path using quadTo
        path = QPainterPath()
        if points:
            path.moveTo(points[0][0], points[0][1])
            n = len(points)
            for i in range(n):
                p1 = points[i]
                p2 = points[(i + 1) % n]
                mid = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
                path.quadTo(p1[0], p1[1], mid[0], mid[1])
            path.closeSubpath()
        # Fill the polygon with a vibrant, semi-transparent color
        fill_color = QColor(self.color)
        fill_color.setAlpha(self.alpha)
        painter.setBrush(QBrush(fill_color))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)
        # Draw a glowing outline
        glow_color = QColor(self.color)
        glow_color.setAlpha(self.alpha)
        glow_pen = QPen(glow_color, 6)
        painter.setPen(glow_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)
        # Optionally overlay a faint radial gradient for depth
        grad = QRadialGradient(cx, cy, base_radius * 1.25)
        c = QColor(self.color)
        c.setAlpha(self.alpha)
        grad.setColorAt(0.0, c)
        c2 = QColor(self.color)
        c2.setAlpha(0)
        grad.setColorAt(1.0, c2)
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - base_radius, cy - base_radius, base_radius * 2, base_radius * 2)

class MainWindow(QMainWindow):
    # Signal to update bar values from audio thread
    bar_values_updated = Signal(list)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EQ Visualizer - Mode Switcher")
        main_widget = QWidget(self)
        vbox = QVBoxLayout(main_widget)
        # Mode switcher
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Circle EQ", "Bar EQ", "Waveform EQ", "Waveform Gradient", "Waveform Blue Gradient"])
        self.mode_combo.currentIndexChanged.connect(self.switch_mode)
        vbox.addWidget(self.mode_combo)
        # Audio controls
        hbox = QHBoxLayout()
        self.audio_path_label = QLabel("No audio file selected", self)
        self.audio_path_label.setWordWrap(True)
        self.select_btn = QPushButton("Select Audio File", self)
        self.select_btn.clicked.connect(self.select_audio_file)
        self.play_btn = QPushButton("Play", self)
        self.play_btn.clicked.connect(self.play_audio)
        self.mute_btn = QPushButton("Mute", self)
        self.mute_btn.setCheckable(True)
        self.mute_btn.clicked.connect(self.toggle_mute)
        self.system_audio_checkbox = QCheckBox("Use Microphone Input", self)
        self.system_audio_checkbox.stateChanged.connect(self.toggle_system_audio)
        # Device dropdown
        self.device_combo = QComboBox(self)
        self.device_combo.setMinimumWidth(220)
        self.device_combo.addItem("Select microphone device...")
        self.device_combo.currentIndexChanged.connect(self.on_device_selected)
        self.system_audio_device_index = None
        # Refresh button for devices
        self.refresh_devices_btn = QPushButton("Refresh Devices", self)
        self.refresh_devices_btn.clicked.connect(self.refresh_device_list)
        hbox.addWidget(self.select_btn)
        hbox.addWidget(self.audio_path_label)
        hbox.addWidget(self.play_btn)
        hbox.addWidget(self.mute_btn)
        hbox.addWidget(self.system_audio_checkbox)
        hbox.addWidget(self.device_combo)
        hbox.addWidget(self.refresh_devices_btn)
        vbox.addLayout(hbox)
        
        # Audio presets
        preset_label = QLabel("Audio Presets:", self)
        vbox.addWidget(preset_label)
        
        # Create preset buttons in a grid layout
        preset_layout = QHBoxLayout()
        self.preset_buttons = {}
        
        for preset_name, preset_path in AUDIO_PRESETS.items():
            btn = QPushButton(preset_name, self)
            btn.setMaximumWidth(120)
            btn.clicked.connect(lambda checked, path=preset_path, name=preset_name: self.load_audio_preset(path, name))
            preset_layout.addWidget(btn)
            self.preset_buttons[preset_name] = btn
        
        vbox.addLayout(preset_layout)
        
        # Visualizer area
        self.visualizer_stack = QWidget()
        self.visualizer_layout = QVBoxLayout(self.visualizer_stack)
        self.visualizer_layout.setContentsMargins(0, 0, 0, 0)
        self.circle_widget = CircleEQWidget(self)
        self.bar_widget = BarEQWidget(self)
        # Three overlapping nets for bass, mid, treble
        self.waveform_net_container = QWidget(self)
        self.waveform_net_container.setAttribute(Qt.WA_TranslucentBackground)
        self.waveform_net_container.setLayout(None)
        self.waveform_bg = QWidget(self.waveform_net_container)
        self.waveform_bg.setStyleSheet('background: black;')
        self.waveform_bg.lower()
        self.waveform_bass = CircularNetEQWidget(self.waveform_net_container, num_points=64, color=(80,180,255))
        self.waveform_mid = CircularNetEQWidget(self.waveform_net_container, num_points=64, color=(255,80,180))
        self.waveform_treble = CircularNetEQWidget(self.waveform_net_container, num_points=64, color=(220,255,120))
        # Geometry will be set in resizeEvent
        self.visualizer_layout.addWidget(self.circle_widget)
        self.visualizer_layout.addWidget(self.bar_widget)
        self.visualizer_layout.addWidget(self.waveform_net_container)
        self.bar_widget.hide()
        self.waveform_net_container.hide()
        # Hide all nets initially
        self.waveform_bass.hide()
        self.waveform_mid.hide()
        self.waveform_treble.hide()
        
        # Three overlapping gradient widgets for bass, mid, treble
        self.waveform_grad_container = QWidget(self)
        self.waveform_grad_container.setAttribute(Qt.WA_TranslucentBackground)
        self.waveform_grad_container.setLayout(None)
        self.waveform_grad_bg = QWidget(self.waveform_grad_container)
        self.waveform_grad_bg.setStyleSheet('background: black;')
        self.waveform_grad_bg.lower()
        self.waveform_grad_bass = CircularGradientEQWidget(self.waveform_grad_container, num_points=64, color=(80,180,255))
        self.waveform_grad_mid = CircularGradientEQWidget(self.waveform_grad_container, num_points=64, color=(255,80,180))
        self.waveform_grad_treble = CircularGradientEQWidget(self.waveform_grad_container, num_points=64, color=(220,255,120))
        self.visualizer_layout.addWidget(self.waveform_grad_container)
        self.waveform_grad_container.hide()
        self.waveform_grad_bass.hide()
        self.waveform_grad_mid.hide()
        self.waveform_grad_treble.hide()
        
        # Three overlapping blue gradient widgets for bass, mid, treble
        self.waveform_bluegrad_container = QWidget(self)
        self.waveform_bluegrad_container.setAttribute(Qt.WA_TranslucentBackground)
        self.waveform_bluegrad_container.setLayout(None)
        self.waveform_bluegrad_bg = QWidget(self.waveform_bluegrad_container)
        self.waveform_bluegrad_bg.setStyleSheet('background: black;')
        self.waveform_bluegrad_bg.lower()
        self.waveform_blue_bass = CircularGradientEQWidget(self.waveform_bluegrad_container, num_points=64, color=(80,180,255), alpha=255, radius_scale=1.0, radius_ratio=0.30, energy_mult=1.5)
        self.waveform_blue_mid = CircularGradientEQWidget(self.waveform_bluegrad_container, num_points=64, color=(100,140,255), alpha=255, radius_scale=0.9, radius_ratio=0.30, energy_mult=1.5)
        self.waveform_blue_treble = CircularGradientEQWidget(self.waveform_bluegrad_container, num_points=64, color=(120,220,255), alpha=255, radius_scale=0.81, radius_ratio=0.30, energy_mult=1.5)
        self.visualizer_layout.addWidget(self.waveform_bluegrad_container)
        self.waveform_bluegrad_container.hide()
        self.waveform_blue_bass.hide()
        self.waveform_blue_mid.hide()
        self.waveform_blue_treble.hide()
        
        # Connect signal to update bar values
        self.bar_values_updated.connect(self.bar_widget.set_eq_bars)
        
        vbox.addWidget(self.visualizer_stack, stretch=1)
        self.setCentralWidget(main_widget)
        self.resize(900, 600)
        # Audio state
        if HARDCODED_AUDIO_PATH:
            self.selected_audio_path = HARDCODED_AUDIO_PATH
            self.audio_path_label.setText(f"Selected: {HARDCODED_AUDIO_PATH}")
            # Highlight the default preset button if it exists
            for preset_name, preset_path in AUDIO_PRESETS.items():
                if preset_path == HARDCODED_AUDIO_PATH:
                    self.preset_buttons[preset_name].setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
                    break
        else:
            self.selected_audio_path = None
        self.is_playing = False
        self.is_muted = False
        self.play_thread = None
        self.use_system_audio = False
        
        # Auto-select first microphone if available (will be called after populate_device_list)
        QTimer.singleShot(100, self.auto_select_microphone)

    def switch_mode(self, idx):
        was_playing = self.is_playing
        if was_playing:
            self.stop_audio()
        if idx == 0:
            self.bar_widget.hide()
            self.bar_widget.stop_animation()
            self.circle_widget.show()
            self.circle_widget.start_animation()
            self.waveform_net_container.hide()
            self.waveform_bass.hide()
            self.waveform_mid.hide()
            self.waveform_treble.hide()
            self.waveform_grad_container.hide()
            self.waveform_grad_bass.hide()
            self.waveform_grad_mid.hide()
            self.waveform_grad_treble.hide()
            self.waveform_bluegrad_container.hide()
            self.waveform_blue_bass.hide()
            self.waveform_blue_mid.hide()
            self.waveform_blue_treble.hide()
        elif idx == 1:
            self.circle_widget.hide()
            self.circle_widget.stop_animation()
            self.bar_widget.show()
            self.bar_widget.start_animation()
            self.waveform_net_container.hide()
            self.waveform_bass.hide()
            self.waveform_mid.hide()
            self.waveform_treble.hide()
            self.waveform_grad_container.hide()
            self.waveform_grad_bass.hide()
            self.waveform_grad_mid.hide()
            self.waveform_grad_treble.hide()
            self.waveform_bluegrad_container.hide()
            self.waveform_blue_bass.hide()
            self.waveform_blue_mid.hide()
            self.waveform_blue_treble.hide()
        elif idx == 2:
            self.circle_widget.hide()
            self.circle_widget.stop_animation()
            self.bar_widget.hide()
            self.bar_widget.stop_animation()
            self.waveform_net_container.show()
            self.waveform_bass.show()
            self.waveform_bass.start_animation()
            self.waveform_mid.show()
            self.waveform_mid.start_animation()
            self.waveform_treble.show()
            self.waveform_treble.start_animation()
            self.waveform_grad_container.hide()
            self.waveform_grad_bass.hide()
            self.waveform_grad_mid.hide()
            self.waveform_grad_treble.hide()
            self.waveform_bluegrad_container.hide()
            self.waveform_blue_bass.hide()
            self.waveform_blue_mid.hide()
            self.waveform_blue_treble.hide()
        elif idx == 3:
            self.circle_widget.hide()
            self.circle_widget.stop_animation()
            self.bar_widget.hide()
            self.bar_widget.stop_animation()
            self.waveform_net_container.hide()
            self.waveform_bass.hide()
            self.waveform_mid.hide()
            self.waveform_treble.hide()
            self.waveform_grad_container.show()
            self.waveform_grad_bass.show()
            self.waveform_grad_bass.start_animation()
            self.waveform_grad_mid.show()
            self.waveform_grad_mid.start_animation()
            self.waveform_grad_treble.show()
            self.waveform_grad_treble.start_animation()
            self.waveform_bluegrad_container.hide()
            self.waveform_blue_bass.hide()
            self.waveform_blue_mid.hide()
            self.waveform_blue_treble.hide()
        else:
            self.circle_widget.hide()
            self.circle_widget.stop_animation()
            self.bar_widget.hide()
            self.bar_widget.stop_animation()
            self.waveform_net_container.hide()
            self.waveform_bass.hide()
            self.waveform_mid.hide()
            self.waveform_treble.hide()
            self.waveform_grad_container.hide()
            self.waveform_grad_bass.hide()
            self.waveform_grad_mid.hide()
            self.waveform_grad_treble.hide()
            self.waveform_bluegrad_container.show()
            self.waveform_blue_bass.show()
            self.waveform_blue_bass.start_animation()
            self.waveform_blue_mid.show()
            self.waveform_blue_mid.start_animation()
            self.waveform_blue_treble.show()
            self.waveform_blue_treble.start_animation()
        if was_playing:
            self.play_audio()

    def select_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.flac *.ogg);;All Files (*)")
        if file_path:
            self.selected_audio_path = file_path
            self.audio_path_label.setText(f"Selected: {file_path}")
        else:
            self.audio_path_label.setText("No audio file selected")

    def load_audio_preset(self, file_path, preset_name):
        """
        Load an audio file from a preset.
        
        Args:
            file_path: Path to the audio file
            preset_name: Name of the preset
        """
        if os.path.exists(file_path):
            self.selected_audio_path = file_path
            self.audio_path_label.setText(f"Selected: {preset_name}")
            print(f"Loaded preset: {preset_name} - {file_path}")
            
            # Highlight the selected preset button
            for name, btn in self.preset_buttons.items():
                if name == preset_name:
                    btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
                else:
                    btn.setStyleSheet("")  # Reset to default style
        else:
            print(f"Audio file not found: {file_path}")
            self.audio_path_label.setText(f"Error: File not found - {preset_name}")

    def play_audio(self):
        if not self.use_system_audio and not self.selected_audio_path:
            return
        if not self.is_playing:
            self.is_playing = True
            self.play_btn.setText("Stop")
            self.play_thread = threading.Thread(target=self._play_audio_thread, daemon=True)
            self.play_thread.start()
        else:
            self.stop_audio()

    def stop_audio(self):
        self.is_playing = False
        self.play_btn.setText("Play")
        self.circle_widget.set_eq_sections([0.1] * self.circle_widget.num_sections)
        self.bar_widget.set_idle()
        self.waveform_bass.set_idle()
        self.waveform_mid.set_idle()
        self.waveform_treble.set_idle()
        self.waveform_net_container.hide()
        self.waveform_bass.hide()
        self.waveform_mid.hide()
        self.waveform_treble.hide()
        self.waveform_grad_bass.set_idle()
        self.waveform_grad_mid.set_idle()
        self.waveform_grad_treble.set_idle()
        self.waveform_grad_container.hide()
        self.waveform_grad_bass.hide()
        self.waveform_grad_mid.hide()
        self.waveform_grad_treble.hide()
        self.waveform_blue_bass.set_idle()
        self.waveform_blue_mid.set_idle()
        self.waveform_blue_treble.set_idle()
        self.waveform_bluegrad_container.hide()
        self.waveform_blue_bass.hide()
        self.waveform_blue_mid.hide()
        self.waveform_blue_treble.hide()

    def toggle_mute(self):
        self.is_muted = self.mute_btn.isChecked()
        self.mute_btn.setText("Unmute" if self.is_muted else "Mute")

    def toggle_system_audio(self, state):
        self.use_system_audio = bool(state)
        if self.use_system_audio:
            # Auto-select first available microphone if none selected
            if self.system_audio_device_index is None and self.device_combo.count() > 1:
                self.device_combo.setCurrentIndex(1)  # Select first microphone device
            elif self.system_audio_device_index is not None:
                device_name = self.device_combo.currentText()
                self.audio_path_label.setText(f"Microphone: {device_name}")
            else:
                self.audio_path_label.setText("Microphone input will be visualized. (Select a device)")
        else:
            if self.selected_audio_path:
                self.audio_path_label.setText(f"Selected: {self.selected_audio_path}")
            else:
                self.audio_path_label.setText("No audio file selected")

    def on_device_selected(self, idx):
        if idx > 0:
            self.system_audio_device_index = self.device_combo.itemData(idx)
            device_name = self.device_combo.currentText()
            # Update status if using microphone mode
            if self.use_system_audio:
                self.audio_path_label.setText(f"Microphone: {device_name}")
        else:
            self.system_audio_device_index = None
            if self.use_system_audio:
                self.audio_path_label.setText("Microphone input will be visualized.")

    def _play_audio_thread(self):
        if self.use_system_audio:
            device_index = self.system_audio_device_index
            if device_index is None:
                print("[MIC] No microphone device selected!")
                self.is_playing = False
                self.play_btn.setText("Play")
                return
            print(f"[MIC] Using device index {device_index} for microphone input.")
            try:
                samplerate = 44100
                channels = 1  # Microphone typically mono
                blocksize = 2048
                with sd.InputStream(
                    device=device_index,
                    channels=channels,
                    samplerate=samplerate,
                    dtype='float32',
                    blocksize=blocksize,
                    latency='low'
                ) as stream:
                    audio_counter = 0
                    while self.is_playing:
                        data, overflowed = stream.read(blocksize)
                        if np.any(data != 0):
                            audio_counter = min(audio_counter + 1, 10)
                        
                        # Use the audio data directly (already mono)
                        chunk = data[:, 0] if data.shape[1] > 0 else np.zeros(blocksize)
                        
                        mode = self.mode_combo.currentIndex()
                        if mode == 0:
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            raw_circle_values = map_frequency_to_bars(mag, samplerate, self.circle_widget.num_sections)
                            if raw_circle_values and max(raw_circle_values) > 0:
                                max_val = max(raw_circle_values)
                                normalized_circle_vals = [0.1 + 0.9 * (v / max_val) for v in raw_circle_values]
                            else:
                                normalized_circle_vals = [0.1] * len(raw_circle_values)
                            if len(normalized_circle_vals) != self.circle_widget.num_sections:
                                if len(normalized_circle_vals) > self.circle_widget.num_sections:
                                    normalized_circle_vals = normalized_circle_vals[:self.circle_widget.num_sections]
                                else:
                                    normalized_circle_vals.extend([0.1] * (self.circle_widget.num_sections - len(normalized_circle_vals)))
                            self.circle_widget.set_eq_sections(normalized_circle_vals)
                        elif mode == 1:
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            raw_bar_values = map_frequency_to_bars(mag, samplerate, self.bar_widget.num_bars)
                            if raw_bar_values and max(raw_bar_values) > 0:
                                max_val = max(raw_bar_values)
                                normalized_vals = [0.1 + 0.9 * (v / max_val) for v in raw_bar_values]
                            else:
                                normalized_vals = [0.1] * len(raw_bar_values)
                            if len(normalized_vals) != self.bar_widget.num_bars:
                                if len(normalized_vals) > self.bar_widget.num_bars:
                                    normalized_vals = normalized_vals[:self.bar_widget.num_bars]
                                else:
                                    normalized_vals.extend([0.1] * (self.bar_widget.num_bars - len(normalized_vals)))
                            self.bar_values_updated.emit(normalized_vals)
                        elif mode == 2:
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            # Split FFT into bands
                            def band_energy(mag, sr, n_points, f_lo, f_hi):
                                freq_res = sr / (2 * len(mag))
                                lo_bin = int(f_lo / freq_res)
                                hi_bin = int(f_hi / freq_res)
                                hi_bin = min(hi_bin, len(mag)-1)
                                band = mag[lo_bin:hi_bin+1]
                                minval = 0.25
                                if len(band) == 0:
                                    return [minval]*n_points
                                bins_per = max(1, len(band)//n_points)
                                vals = []
                                for i in range(n_points):
                                    s = i*bins_per
                                    e = min(s+bins_per, len(band))
                                    if s < len(band):
                                        v = float(np.sqrt(np.mean(band[s:e]**2)))
                                        vals.append(v)
                                    else:
                                        vals.append(minval)
                                if max(vals) > 0:
                                    maxv = max(vals)
                                    return [minval+(1.0-minval)*(v/maxv) for v in vals]
                                else:
                                    return [minval]*n_points
                            npts = self.waveform_bass.num_points
                            bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                            mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                            treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                            self.waveform_bass.set_net_radii(bass_vals)
                            self.waveform_mid.set_net_radii(mid_vals)
                            self.waveform_treble.set_net_radii(treb_vals)
                        elif mode == 3:
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            def band_energy(mag, sr, n_points, f_lo, f_hi):
                                freq_res = sr / (2 * len(mag))
                                lo_bin = int(f_lo / freq_res)
                                hi_bin = int(f_hi / freq_res)
                                hi_bin = min(hi_bin, len(mag)-1)
                                band = mag[lo_bin:hi_bin+1]
                                minval = 0.25
                                if len(band) == 0:
                                    return [minval]*n_points
                                bins_per = max(1, len(band)//n_points)
                                vals = []
                                for i in range(n_points):
                                    s = i*bins_per
                                    e = min(s+bins_per, len(band))
                                    if s < len(band):
                                        v = float(np.sqrt(np.mean(band[s:e]**2)))
                                        vals.append(v)
                                    else:
                                        vals.append(minval)
                                if max(vals) > 0:
                                    maxv = max(vals)
                                    return [minval+(1.0-minval)*(v/maxv) for v in vals]
                                else:
                                    return [minval]*n_points
                            npts = self.waveform_grad_bass.num_points
                            bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                            mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                            treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                            self.waveform_grad_bass.set_net_radii(bass_vals)
                            self.waveform_grad_mid.set_net_radii(mid_vals)
                            self.waveform_grad_treble.set_net_radii(treb_vals)
                        elif mode == 4:
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            def band_energy(mag, sr, n_points, f_lo, f_hi):
                                freq_res = sr / (2 * len(mag))
                                lo_bin = int(f_lo / freq_res)
                                hi_bin = int(f_hi / freq_res)
                                hi_bin = min(hi_bin, len(mag)-1)
                                band = mag[lo_bin:hi_bin+1]
                                minval = 0.25
                                if len(band) == 0:
                                    return [minval]*n_points
                                bins_per = max(1, len(band)//n_points)
                                vals = []
                                for i in range(n_points):
                                    s = i*bins_per
                                    e = min(s+bins_per, len(band))
                                    if s < len(band):
                                        v = float(np.sqrt(np.mean(band[s:e]**2)))
                                        vals.append(v)
                                    else:
                                        vals.append(minval)
                                if max(vals) > 0:
                                    maxv = max(vals)
                                    return [minval+(1.0-minval)*(v/maxv) for v in vals]
                                else:
                                    return [minval]*n_points
                            npts = self.waveform_blue_bass.num_points
                            bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                            mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                            treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                            self.waveform_blue_bass.set_net_radii(bass_vals)
                            self.waveform_blue_mid.set_net_radii(mid_vals)
                            self.waveform_blue_treble.set_net_radii(treb_vals)
                        sd.sleep(20)
            except Exception as e:
                print(f"Microphone error: {e}")
            finally:
                self.is_playing = False
                self.play_btn.setText("Play")
                self.circle_widget.set_eq_sections([0.1] * self.circle_widget.num_sections)
                self.bar_widget.set_idle()
                self.waveform_bass.set_idle()
                self.waveform_mid.set_idle()
                self.waveform_treble.set_idle()
            return
        try:
            data, samplerate = sf.read(self.selected_audio_path, dtype='float32')
            frames_per_update = int(samplerate * 0.05)
            total_frames = len(data)
            idx = 0
            def callback(outdata, frames, time, status):
                nonlocal idx
                if self.is_muted:
                    outdata[:] = 0
                else:
                    chunk = data[idx:idx+frames]
                    if len(chunk.shape) > 1:
                        chunk = chunk.mean(axis=1)
                    outdata[:len(chunk), 0] = chunk
                    if chunk.shape[0] < frames:
                        outdata[chunk.shape[0]:, 0] = 0
                # Real FFT-based EQ for Bar mode
                if self.mode_combo.currentIndex() == 0:
                    # Circle EQ mode - use frequency mapping for circle sections
                    if len(chunk) > 0:
                        try:
                            # Perform FFT analysis
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            
                            # Use frequency mapping for circle sections (fewer sections)
                            raw_circle_values = map_frequency_to_bars(mag, samplerate, self.circle_widget.num_sections)
                            
                            # Normalize values to [0.1, 1.0] range
                            if raw_circle_values and max(raw_circle_values) > 0:
                                max_val = max(raw_circle_values)
                                normalized_circle_vals = [0.1 + 0.9 * (v / max_val) for v in raw_circle_values]
                            else:
                                normalized_circle_vals = [0.1] * len(raw_circle_values)
                            
                            # Ensure we have exactly num_sections values
                            if len(normalized_circle_vals) != self.circle_widget.num_sections:
                                if len(normalized_circle_vals) > self.circle_widget.num_sections:
                                    normalized_circle_vals = normalized_circle_vals[:self.circle_widget.num_sections]
                                else:
                                    normalized_circle_vals.extend([0.1] * (self.circle_widget.num_sections - len(normalized_circle_vals)))
                            
                            # Send to circle widget via signal
                            self.circle_widget.set_eq_sections(normalized_circle_vals)
                            
                        except Exception as e:
                            # Send idle values on error
                            idle_circle_vals = [0.1] * self.circle_widget.num_sections
                            self.circle_widget.set_eq_sections(idle_circle_vals)
                    else:
                        # No audio data, send random values for demo
                        random_vals = [0.1 + 0.38 * random.random() for _ in range(self.circle_widget.num_sections)]
                        self.circle_widget.set_eq_sections(random_vals)
                elif self.mode_combo.currentIndex() == 1:
                    if len(chunk) > 0:
                        try:
                            # Perform FFT analysis
                            fft = np.fft.rfft(chunk, n=2048)
                            mag = np.abs(fft)
                            
                            # Use frequency mapping for proper bass-mid-treble distribution
                            raw_bar_values = map_frequency_to_bars(mag, samplerate, self.bar_widget.num_bars)
                            
                            # Normalize values to [0.1, 1.0] range (minimum visible height)
                            if raw_bar_values and max(raw_bar_values) > 0:
                                max_val = max(raw_bar_values)
                                normalized_vals = [0.1 + 0.9 * (v / max_val) for v in raw_bar_values]
                            else:
                                # All values are zero, use minimum values
                                normalized_vals = [0.1] * len(raw_bar_values)
                            
                            # Ensure we have exactly num_bars values
                            if len(normalized_vals) != self.bar_widget.num_bars:
                                if len(normalized_vals) > self.bar_widget.num_bars:
                                    normalized_vals = normalized_vals[:self.bar_widget.num_bars]
                                else:
                                    normalized_vals.extend([0.1] * (self.bar_widget.num_bars - len(normalized_vals)))
                            
                            # Send to bar widget via signal (thread-safe)
                            self.bar_values_updated.emit(normalized_vals)
                            
                        except Exception as e:
                            # Send idle values on error
                            idle_vals = [0.1] * self.bar_widget.num_bars
                            self.bar_values_updated.emit(idle_vals)
                elif self.mode_combo.currentIndex() == 2:
                    fft = np.fft.rfft(chunk, n=2048)
                    mag = np.abs(fft)
                    def band_energy(mag, sr, n_points, f_lo, f_hi):
                        freq_res = sr / (2 * len(mag))
                        lo_bin = int(f_lo / freq_res)
                        hi_bin = int(f_hi / freq_res)
                        hi_bin = min(hi_bin, len(mag)-1)
                        band = mag[lo_bin:hi_bin+1]
                        minval = 0.25
                        if len(band) == 0:
                            return [minval]*n_points
                        bins_per = max(1, len(band)//n_points)
                        vals = []
                        for i in range(n_points):
                            s = i*bins_per
                            e = min(s+bins_per, len(band))
                            if s < len(band):
                                v = float(np.sqrt(np.mean(band[s:e]**2)))
                                vals.append(v)
                            else:
                                vals.append(minval)
                        if max(vals) > 0:
                            maxv = max(vals)
                            return [minval+(1.0-minval)*(v/maxv) for v in vals]
                        else:
                            return [minval]*n_points
                    npts = self.waveform_bass.num_points
                    bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                    mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                    treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                    self.waveform_bass.set_net_radii(bass_vals)
                    self.waveform_mid.set_net_radii(mid_vals)
                    self.waveform_treble.set_net_radii(treb_vals)
                elif self.mode_combo.currentIndex() == 3:
                    fft = np.fft.rfft(chunk, n=2048)
                    mag = np.abs(fft)
                    def band_energy(mag, sr, n_points, f_lo, f_hi):
                        freq_res = sr / (2 * len(mag))
                        lo_bin = int(f_lo / freq_res)
                        hi_bin = int(f_hi / freq_res)
                        hi_bin = min(hi_bin, len(mag)-1)
                        band = mag[lo_bin:hi_bin+1]
                        minval = 0.25
                        if len(band) == 0:
                            return [minval]*n_points
                        bins_per = max(1, len(band)//n_points)
                        vals = []
                        for i in range(n_points):
                            s = i*bins_per
                            e = min(s+bins_per, len(band))
                            if s < len(band):
                                v = float(np.sqrt(np.mean(band[s:e]**2)))
                                vals.append(v)
                            else:
                                vals.append(minval)
                        if max(vals) > 0:
                            maxv = max(vals)
                            return [minval+(1.0-minval)*(v/maxv) for v in vals]
                        else:
                            return [minval]*n_points
                    npts = self.waveform_grad_bass.num_points
                    bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                    mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                    treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                    self.waveform_grad_bass.set_net_radii(bass_vals)
                    self.waveform_grad_mid.set_net_radii(mid_vals)
                    self.waveform_grad_treble.set_net_radii(treb_vals)
                elif self.mode_combo.currentIndex() == 4:
                    fft = np.fft.rfft(chunk, n=2048)
                    mag = np.abs(fft)
                    def band_energy(mag, sr, n_points, f_lo, f_hi):
                        freq_res = sr / (2 * len(mag))
                        lo_bin = int(f_lo / freq_res)
                        hi_bin = int(f_hi / freq_res)
                        hi_bin = min(hi_bin, len(mag)-1)
                        band = mag[lo_bin:hi_bin+1]
                        minval = 0.25
                        if len(band) == 0:
                            return [minval]*n_points
                        bins_per = max(1, len(band)//n_points)
                        vals = []
                        for i in range(n_points):
                            s = i*bins_per
                            e = min(s+bins_per, len(band))
                            if s < len(band):
                                v = float(np.sqrt(np.mean(band[s:e]**2)))
                                vals.append(v)
                            else:
                                vals.append(minval)
                        if max(vals) > 0:
                            maxv = max(vals)
                            return [minval+(1.0-minval)*(v/maxv) for v in vals]
                        else:
                            return [minval]*n_points
                    npts = self.waveform_blue_bass.num_points
                    bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                    mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                    treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                    self.waveform_blue_bass.set_net_radii(bass_vals)
                    self.waveform_blue_mid.set_net_radii(mid_vals)
                    self.waveform_blue_treble.set_net_radii(treb_vals)
                idx += frames
            with sd.OutputStream(channels=1, samplerate=samplerate, callback=callback, blocksize=frames_per_update):
                while idx < total_frames and self.is_playing:
                    sd.sleep(50)
        except Exception as e:
            print(f"Audio playback error: {e}")
        finally:
            self.is_playing = False
            self.play_btn.setText("Play")
            # Reset bands to idle
            self.circle_widget.set_eq_sections([0.1] * self.circle_widget.num_sections)
            self.bar_widget.set_idle()
            self.waveform_bass.set_idle()
            self.waveform_mid.set_idle()
            self.waveform_treble.set_idle()

    def populate_device_list(self):
        import sounddevice as sd
        self.device_combo.clear()
        self.device_combo.addItem("Select microphone device...")
        self._device_list = sd.query_devices()
        for idx, dev in enumerate(self._device_list):
            # Only show devices with input channels (microphones)
            if dev['max_input_channels'] > 0:
                label = f"[{idx}] {dev['name']} (Channels: {dev['max_input_channels']})"
                self.device_combo.addItem(label, idx)
    
    def refresh_device_list(self):
        """Refresh the device list and repopulate the dropdown."""
        self.populate_device_list()
        # Auto-select first microphone if in microphone mode
        if self.use_system_audio and self.device_combo.count() > 1:
            self.device_combo.setCurrentIndex(1)  # Select first microphone device
        else:
            # Reset device selection
            self.system_audio_device_index = None

    def auto_select_microphone(self):
        """Auto-select the first available microphone device."""
        if self.device_combo.count() > 1:
            self.device_combo.setCurrentIndex(1)  # Select first microphone device

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Make the net container and all nets fill the available space
        if hasattr(self, 'waveform_net_container'):
            rect = self.visualizer_stack.geometry()
            self.waveform_net_container.setGeometry(0, 0, rect.width(), rect.height())
            if hasattr(self, 'waveform_bg'):
                self.waveform_bg.setGeometry(0, 0, rect.width(), rect.height())
            for net in (self.waveform_bass, self.waveform_mid, self.waveform_treble):
                net.setGeometry(0, 0, rect.width(), rect.height())
        if hasattr(self, 'waveform_grad_container'):
            rect = self.visualizer_stack.geometry()
            self.waveform_grad_container.setGeometry(0, 0, rect.width(), rect.height())
            if hasattr(self, 'waveform_grad_bg'):
                self.waveform_grad_bg.setGeometry(0, 0, rect.width(), rect.height())
            for grad in (self.waveform_grad_bass, self.waveform_grad_mid, self.waveform_grad_treble):
                grad.setGeometry(0, 0, rect.width(), rect.height())
        if hasattr(self, 'waveform_bluegrad_container'):
            rect = self.visualizer_stack.geometry()
            self.waveform_bluegrad_container.setGeometry(0, 0, rect.width(), rect.height())
            if hasattr(self, 'waveform_bluegrad_bg'):
                self.waveform_bluegrad_bg.setGeometry(0, 0, rect.width(), rect.height())
            for grad in (self.waveform_blue_bass, self.waveform_blue_mid, self.waveform_blue_treble):
                grad.setGeometry(0, 0, rect.width(), rect.height())

def print_sound_devices():
    
    devices = sd.query_devices()
    print("\n=== Sound Devices ===")
    for idx, dev in enumerate(devices):
        inout = []
        if dev['max_input_channels'] > 0:
            inout.append(f"IN:{dev['max_input_channels']}")
        if dev['max_output_channels'] > 0:
            inout.append(f"OUT:{dev['max_output_channels']}")
        marker = " <-- MICROPHONE" if dev['max_input_channels'] > 0 else " (no input)"
        print(f"[{idx}] {dev['name']} | {' '.join(inout) if inout else 'NO IN/OUT'}{marker}")
    print("====================\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.populate_device_list()  # <-- call this after window is created
    win.show()
    sys.exit(app.exec()) 