import math
import random
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

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