from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *
from PySide6.QtWidgets import QSizePolicy
import math


class LoadingWaveWidget(QWidget):
    """
    A loading animation widget with 3/4 dots that create a wave effect.
    
    This widget displays animated dots that move in a wave pattern to indicate
    that the system is processing or waiting for a response.
    """
    
    def __init__(self, parent=None, num_dots=4, dot_size=8, spacing=12, 
                 animation_speed=0.8, wave_amplitude=0.3, wave_frequency=2.0):
        super().__init__(parent)
        self.num_dots = num_dots
        self.dot_size = dot_size
        self.spacing = spacing
        self.animation_speed = animation_speed
        self.wave_amplitude = wave_amplitude
        self.wave_frequency = wave_frequency
        self._animation_time = 0.0
        self._is_animating = False
        self.dot_color = QColor(0, 120, 212)  # Blue color
        self.dot_color_alpha = QColor(0, 120, 212, 100)  # Semi-transparent
        self._setup_animation_timer()
        self.setMinimumSize(self._calculate_minimum_size())
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    def _setup_animation_timer(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_animation)
        self._timer.setInterval(16)  # ~60 FPS
    def _calculate_minimum_size(self):
        width = (self.num_dots - 1) * self.spacing + self.dot_size
        height = self.dot_size + 10  # Extra height for wave movement
        return QSize(width, height)
    def start_animation(self):
        if not self._is_animating:
            self._is_animating = True
            self._animation_time = 0.0
            self._timer.start()
    def stop_animation(self):
        if self._is_animating:
            self._is_animating = False
            self._timer.stop()
            self._animation_time = 0.0
            self.update()
    def is_animating(self):
        return self._is_animating
    def _update_animation(self):
        if self._is_animating:
            self._animation_time += self.animation_speed * 0.016  # 16ms at 60 FPS
            self.update()
    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._is_animating:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center_x = self.width() // 2
        center_y = self.height() // 2
        total_width = (self.num_dots - 1) * self.spacing
        start_x = center_x - total_width // 2
        for i in range(self.num_dots):
            wave_offset = math.sin(self._animation_time + i * self.wave_frequency) * self.wave_amplitude
            x = start_x + i * self.spacing
            y = center_y + wave_offset * self.dot_size
            opacity_factor = 0.3 + 0.7 * (math.sin(self._animation_time + i * self.wave_frequency) + 1) / 2
            color = QColor(self.dot_color)
            color.setAlpha(int(255 * opacity_factor))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(color)
            painter.drawEllipse(QPointF(x, y), self.dot_size // 2, self.dot_size // 2)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.width() < self._calculate_minimum_size().width():
            self.setMinimumWidth(self._calculate_minimum_size().width())
    def showEvent(self, event):
        super().showEvent(event)
        if self._is_animating:
            self._timer.start()
    def hideEvent(self, event):
        super().hideEvent(event)
        self._timer.stop()
    def set_dot_color(self, color):
        self.dot_color = color
        self.dot_color_alpha = QColor(color)
        self.dot_color_alpha.setAlpha(100)
        self.update()
    def set_animation_speed(self, speed):
        self.animation_speed = speed
    def set_wave_amplitude(self, amplitude):
        self.wave_amplitude = amplitude
    def set_wave_frequency(self, frequency):
        self.wave_frequency = frequency 