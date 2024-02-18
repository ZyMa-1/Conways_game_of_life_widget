import time
from typing import Final, Optional

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsView, QSizePolicy, QWidget

from ..GameEngine import GameEngine

MINIMUM_SIZE: Final[tuple[int, int]] = (264, 264)


class GameView(QGraphicsView):
    """
    A custom QGraphicsView for displaying the Game Scene.

    This view manages size hints, allows manipulation of view size constraints,
    and extends the 'paintEvent' to track average painting performance.
    """
    # Signals.

    # Emits after paintEvent method is done
    painted = Signal()

    def __init__(self, parent_widget: Optional[QWidget] = None):
        super().__init__(parent_widget)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.IgnoreAspectRatio)

        self._aspect_ratio_mode = Qt.AspectRatioMode.IgnoreAspectRatio
        self._sum_paint_performance: float = 0
        self._paint_count: int = 0

    def reset_avg_paint_performance(self):
        self._sum_paint_performance: float = 0
        self._paint_count: int = 0

    def get_avg_paint_performance(self) -> float:
        """
        Returns avg paint performance in seconds.
        """
        return self._sum_paint_performance / self._paint_count

    def set_keep_aspect_ratio_constraint(self, value: bool):
        """
        Sets whether the view should keep the aspect ratio constraint of the scene.
        """
        if value:
            self._aspect_ratio_mode = Qt.AspectRatioMode.KeepAspectRatio
        else:
            self._aspect_ratio_mode = Qt.AspectRatioMode.IgnoreAspectRatio

        self.fitInView(self.sceneRect(), self._aspect_ratio_mode)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), self._aspect_ratio_mode)

    def paintEvent(self, event):
        start_time = time.perf_counter()
        super().paintEvent(event)
        end_time = time.perf_counter()
        paint_duration = end_time - start_time
        self._sum_paint_performance += paint_duration
        self._paint_count += 1
        self.painted.emit()

    def minimumSizeHint(self):
        return QSize(*MINIMUM_SIZE)
