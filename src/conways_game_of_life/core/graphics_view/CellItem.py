from typing import Optional

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSceneMouseEvent

from ..GameEngine import GameEngine, CELL_ALIVE, CELL_DEAD
from ..enums import CellEditMode, SceneCellType


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
    Second approach breaks OOP and makes circular import error.
    Third approach was chosen.
    --------------------
    """

    def __init__(self, row: int, col: int, rect: QRectF,
                 *,
                 engine: GameEngine,
                 scene_cell_type: SceneCellType,
                 color_map: dict[SceneCellType, QColor],
                 edit_mode: CellEditMode):
        super().__init__(rect)
        self.setZValue(0)

        self._row = row
        self._col = col
        self._engine = engine
        self._scene_cell_type = scene_cell_type
        self._color_map = color_map
        self._edit_mode = edit_mode

        self._last_painted_rect: Optional[QRectF] = None
        self._last_scene_cell_type: Optional[SceneCellType] = None

    def set_edit_mode(self, value: CellEditMode):
        self._edit_mode = value

    def update_color_map(self, key: SceneCellType, color: QColor):
        self._color_map[key] = color

    def set_scene_cell_type(self, value: SceneCellType):
        self._scene_cell_type = value

    def paint(self, painter, option, widget=None):
        """
        In the paint method logic of the Engine and Scene merges together.
        """
        super().paint(painter, option, None)
        if self._last_painted_rect != self.rect() or self._last_scene_cell_type != self._scene_cell_type:
            color = self._color_map[self._scene_cell_type]
            self._last_scene_cell_type = self._scene_cell_type
            self._last_painted_rect = self.rect()
            painter.fillRect(self.rect(), color)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Handles propagated event.
        """
        super().mousePressEvent(event)
        if event.buttons() != Qt.MouseButton.LeftButton:
            return

        match self._edit_mode:
            case CellEditMode.DEFAULT:
                self._engine.change_cell_state_to_opposite(self._row, self._col)
            case CellEditMode.PAINT:
                self._engine.change_cell_state_at(self._row, self._col, CELL_ALIVE)
            case CellEditMode.ERASE:
                self._engine.change_cell_state_at(self._row, self._col, CELL_DEAD)

        self.update()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        """
        Handles propagated event.
        """
        super().mouseMoveEvent(event)
        if event.buttons() != Qt.MouseButton.LeftButton:
            return

        match self._edit_mode:
            case CellEditMode.PAINT:
                self._engine.change_cell_state_at(self._row, self._col, CELL_ALIVE)
                self.update()
            case CellEditMode.ERASE:
                self._engine.change_cell_state_at(self._row, self._col, CELL_DEAD)
                self.update()
