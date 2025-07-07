import math
import random
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QBrush, QPainterPath
from PySide6.QtWidgets import QWidget

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