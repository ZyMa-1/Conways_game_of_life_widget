from PySide6.QtCore import QRectF
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsRectItem

from ..enums import SceneCellType


class CellItem(QGraphicsRectItem):
    """
    A QGraphicsRectItem representing a cell in the Graphics Scene.

    Receives information from the Scene via setters.

    Approach Discussion:
    --------------------
    Three approaches were considered:
    1. Using the Signal/Slot mechanism to receive updates.
    2. Accepting Scene instance and grabbing values from it directly.
    3. Creating 'setters' methods and making item updates responsibility of the Scene.

    First approach makes item less flexible and dependent to Signals.
    Second approach breaks OOP principles and makes circular import error.
    Third approach was chosen.
    --------------------
    """

    def __init__(self, row: int, col: int, rect: QRectF,
                 *,
                 scene_cell_type: SceneCellType,
                 color_map: dict[SceneCellType, QColor]):
        super().__init__(rect)
        self.setZValue(0)
        self.setAcceptDrops(False)  # Disables automatic mouse events handling

        self._row = row
        self._col = col
        self._scene_cell_type = scene_cell_type
        self._color_map = color_map

    def update_color_map(self, key: SceneCellType, color: QColor):
        self._color_map[key] = color

    def set_scene_cell_type(self, value: SceneCellType):
        self._scene_cell_type = value

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, None)
        color = self._color_map[self._scene_cell_type]
        painter.fillRect(self.rect(), color)
