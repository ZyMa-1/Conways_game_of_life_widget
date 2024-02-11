import time
from typing import Final, Optional

from PySide6.QtCore import Qt, QSize
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

    def __init__(self, parent_widget: QWidget = None):
        super().__init__(parent_widget)

        self._engine: Optional[GameEngine] = None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)

        self._square_size_constraint = False
        self._perfect_size_constraint = False
        self._sum_paint_performance: float = 0
        self._paint_count: int = 0

    def set_engine(self, engine: GameEngine):
        self._engine = engine

    def engine(self):
        return self._engine

    def get_avg_paint_performance(self) -> float:
        """
        Returns avg paint performance in seconds.
        """
        return self._sum_paint_performance / self._paint_count

    def set_square_size_constraint(self, value: bool):
        """
        Sets whether the widget should maintain a square size constraint.
        """
        self._square_size_constraint = value
        if value:
            new_size = self._get_square_size(self.size())
            self.resize(new_size)
        else:
            self.updateGeometry()

    def set_perfect_size_constraint(self, value: bool):
        """
        Sets whether the widget should maintain a perfect size constraint,
        ensuring the sizes of the game items are integer values.
        """
        self._perfect_size_constraint = value
        if value:
            new_size = self._get_perfect_size(self.size())
            self.resize(new_size)
        else:
            self.updateGeometry()

    def _get_perfect_size(self, old_size: QSize) -> QSize:
        old_width, old_height = old_size.width(), old_size.height()
        new_width = old_width - old_width % self._engine.rows
        new_height = old_height - old_height % self._engine.cols
        return QSize(new_width, new_height)

    @staticmethod
    def _get_square_size(old_size: QSize) -> QSize:
        old_width, old_height = old_size.width(), old_size.height()
        size = min(old_width, old_height)
        return QSize(size, size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cur_size = event.size()
        if self._perfect_size_constraint:
            cur_size = self._get_perfect_size(cur_size)
        if self._square_size_constraint:
            cur_size = self._get_square_size(cur_size)
        if cur_size != event.size():
            self.resize(cur_size)

    def paintEvent(self, event):
        start_time = time.perf_counter()
        super().paintEvent(event)
        end_time = time.perf_counter()
        paint_duration = end_time - start_time
        self._sum_paint_performance += paint_duration
        self._paint_count += 1

    def minimumSizeHint(self):
        return QSize(*MINIMUM_SIZE)
