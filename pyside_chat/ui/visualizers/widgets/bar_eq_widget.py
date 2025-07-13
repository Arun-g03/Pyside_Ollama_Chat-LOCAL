from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush
from PySide6.QtWidgets import QWidget

class BarEQWidget(QWidget):
    """
    A bar equalizer widget that displays audio frequency data as animated bars.
    
    This widget renders a series of vertical bars that respond to audio frequency data,
    creating a visual equalizer effect. The bars animate smoothly between target values
    and include reflection effects for enhanced visual appeal.
    """
    
    # Configuration constants
    DEFAULT_NUM_BARS = 24
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
        # Calculate optimal bar width and gap to fill the widget width
        num_bars = self.num_bars
        total_gap_ratio = 0.18  # 18% of width is gaps, 82% is bars
        gap = max(2, int(widget_width * total_gap_ratio / (num_bars + 1)))
        bar_width = max(4, int((widget_width * (1 - total_gap_ratio)) / num_bars))
        total_width = num_bars * bar_width + (num_bars + 1) * gap
        start_x = (widget_width - total_width) // 2 + gap  # Centered, first bar after initial gap
        max_bar_height = int(widget_height * self.BAR_HEIGHT_RATIO)
        base_y = int(widget_height * self.BASE_Y_RATIO)
        
        return {
            'bar_width': bar_width,
            'gap': gap,
            'max_bar_height': max_bar_height,
            'base_y': base_y,
            'start_x': start_x
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
        
        # Draw all bars, centered horizontally
        for i, value in enumerate(self._bar_values):
            x = geometry['start_x'] + i * (geometry['bar_width'] + geometry['gap'])
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