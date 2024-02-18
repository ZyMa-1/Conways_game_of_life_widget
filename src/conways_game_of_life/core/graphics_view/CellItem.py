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
        self.setAcceptDrops(False)  # Disables receiving mouse events bypassing scene

        self._row = row
        self._col = col
        self._scene_cell_type = scene_cell_type
        self._color_map = color_map
        self._last_data: Optional[dict] = None  # The key for optimizing paint method

    def update_color_map(self, key: SceneCellType, color: QColor):
        self._color_map[key] = color

    def set_scene_cell_type(self, value: SceneCellType):
        self._scene_cell_type = value

    def paint(self, painter, option, widget=None):
        """
        tl;dr
        Somehow upon updating item with row=x, col=y,
        adjacent items are being updated too, and their paint method invokes too.
        Upon inspecting the issue found out that
        "self.boundingRect()" is not completely equal to "self.rect()".
        The values of their x, y, w, h differ between each other from around 0.5 to 1.0 pixels.
        That fucking sucks.

        Tried to apply margin to the board, since the cell(0, 0) have (-0.5, -0.5) top left point,
        but it seems that the problem with item coordinates, but not the margins.

        On the other hand I do not think that optimization of limiting cell redraws
        would impact performance so much,
        since the Qt should already perform such optimization.
        But nevertheless I think that my optimization would impact the performance anyway in some
        or another way.
        """
        # print(self._row, self._col, self.boundingRect(), self.rect())
        super().paint(painter, option, None)
        color = self._color_map[self._scene_cell_type]
        painter.fillRect(self.rect(), color)
