import math
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QBrush
from PySide6.QtWidgets import QWidget

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