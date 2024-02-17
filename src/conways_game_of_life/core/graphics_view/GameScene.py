from typing import Optional, Final, Literal, Tuple

from PySide6.QtCore import QTimer, Signal, QPoint, QPointF, QRectF, QSizeF, Property, Slot, Qt, QLineF
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsScene

from ..GameEngine import GameEngine, CELL_ALIVE, CELL_DEAD
from ..abcs import IMySerializable, IMyPropertySignalAccessor, QAbcMeta
from ..private_utils import property_setter_error_handle
from ..static_types import PatternSchema
from .BorderItem import BorderItem
from .CellItem import CellItem
from ..enums import CellEditMode, SceneCellType

DEFAULT_SIZE: Final[Tuple[int, int]] = (1536, 1536)

DEFAULT_BORDER_THICKNESS: Final[float] = 1  # (assigned to attribute)
DEFAULT_TURN_DURATION: Final[int] = 1500  # ms (assigned to attribute)
DEFAULT_CELL_DEAD_COLOR: Final[QColor] = QColor(255, 255, 255)  # (assigned to attribute)
DEFAULT_CELL_ALIVE_COLOR: Final[QColor] = QColor(173, 216, 230)  # (assigned to attribute)
DEFAULT_BORDER_COLOR: Final[QColor] = QColor(192, 192, 192)  # (assigned to attribute)
DEFAULT_ACTIVE_CELL_COLOR: Final[QColor] = QColor(235, 235, 235)  # (used)

_cellKT = tuple[int, int]
_borderKT = tuple[int, Literal['Row', 'Col']]


class GameScene(QGraphicsScene, IMySerializable, IMyPropertySignalAccessor, metaclass=QAbcMeta):
    """
    Class representing the Main Scene of the Game.

    Accepts engine as a parameter, operates the game and manages scene items.
    Manages item map by itself, so the methods like 'itemAt()' and 'items()' are not used at all,
    but instead class uses own methods to store and search the items.
    """

    def __init__(self, engine: GameEngine, parent=None):
        super().__init__(parent)
        self.setSceneRect(QRectF(0, 0, DEFAULT_SIZE[0], DEFAULT_SIZE[1]))

        self._engine = engine
        self._cell_item_map: dict[_cellKT, CellItem] = {}
        self._border_item_map: dict[_borderKT, BorderItem] = {}

        # Attributes
        self._border_thickness = DEFAULT_BORDER_THICKNESS
        self._border_color = DEFAULT_BORDER_COLOR
        self._cell_alive_color = DEFAULT_CELL_ALIVE_COLOR
        self._cell_dead_color = DEFAULT_CELL_DEAD_COLOR
        self._is_game_running = False
        self._cell_edit_mode = CellEditMode.DEFAULT
        self._turn_duration = DEFAULT_TURN_DURATION
        # Active cell should be synced with '_is_game_running'
        # In case when '_is_game_running' is False, then 'active_cell' should always be None
        self._active_cell: Optional[tuple[int, int]] = (0, 0)

        # Create the scene
        self._create_scene()

        # Turn timer
        self._timer = QTimer(self)

        # Connect timer
        self._timer.timeout.connect(self._make_turn)

        # Connect engine signals
        self._engine.board_changed.connect(self._handle_board_changed)

    # Scene/Item methods
    def _create_border_item(self, val: _borderKT) -> BorderItem:
        coord, literal = val
        if literal == 'Row':
            cell_point = self._cell_top_left_point(coord, 0)
            return BorderItem(
                QLineF(0, cell_point.y(),
                       self.width(),
                       cell_point.y()),
                color=self.get_border_color(),
                thickness_percentage=self.get_border_thickness(),
                scene_width=self.sceneRect().width())
        elif literal == 'Col':
            cell_point = self._cell_top_left_point(0, coord)
            return BorderItem(
                QLineF(cell_point.x(),
                       0, cell_point.x(),
                       self.height()),
                color=self.get_border_color(),
                thickness_percentage=self.get_border_thickness(),
                scene_width=self.sceneRect().width())

    def _create_cell_item(self, val: _cellKT) -> CellItem:
        row, col = val
        cell_rect = self._cell_rect(row, col)
        color_map = {
            SceneCellType.ACTIVE: DEFAULT_ACTIVE_CELL_COLOR,
            SceneCellType.DEAD: self.get_cell_dead_color(),
            SceneCellType.ALIVE: self.get_cell_alive_color()
        }
        return CellItem(row, col, cell_rect,
                        scene_cell_type=self._get_scene_cell_type_at(row, col),
                        color_map=color_map)

    def _create_scene(self):
        """
        Creates the scene and adds items to it.
        Manages the '_cell_item_map' and '_border_item_map' dictionaries.
        """
        # Create cell items
        for row in range(self._engine.rows):
            for col in range(self._engine.cols):
                cell_item = self._create_cell_item((row, col))
                self.addItem(cell_item)
                self._cell_item_map[(row, col)] = cell_item

        # Create horizontal borders
        for row in range(self._engine.rows + 1):
            border_item = self._create_border_item((row, 'Row'))
            self._border_item_map[(row, 'Row')] = border_item
            self.addItem(border_item)

        # Draw vertical borders
        for col in range(self._engine.cols + 1):
            border_item = self._create_border_item((col, 'Col'))
            self._border_item_map[(col, 'Col')] = border_item
            self.addItem(border_item)

    def _update_scene_items(self):
        """
        Updates the scene based on the new dimensions of the game.
        Manages '_cell_item_map' and '_border_item_map' dictionaries.
        """
        # Remove all items from the scene and dictionaries
        self.clear()
        self._cell_item_map.clear()
        self._border_item_map.clear()

        # Create the scene from scratch
        self._create_scene()

    def _reset_scene(self):
        """
        Resets scene to initial state.
        """
        self._border_thickness = DEFAULT_BORDER_THICKNESS
        self._border_color = DEFAULT_BORDER_COLOR
        self._cell_alive_color = DEFAULT_CELL_ALIVE_COLOR
        self._cell_dead_color = DEFAULT_CELL_DEAD_COLOR
        self._is_game_running = False
        self._turn_duration = DEFAULT_TURN_DURATION
        self._active_cell = (0, 0)

        self._update_scene_items()
        self._engine.reset_to_defaults()

    def _update_cell_item_type(self, row: int, col: int):
        """
        Updates cell item type at the given position.
        """
        cell_item = self._cell_item_map[(row, col)]
        cell_item.set_scene_cell_type(self._get_scene_cell_type_at(row, col))
        cell_item.update()

    def _update_cell_item_types(self):
        """
        Updates all cell item types.
        """
        for (row, col), cell_item in self._cell_item_map.items():
            cell_item.set_scene_cell_type(self._get_scene_cell_type_at(row, col))
            cell_item.update()

    # Helper methods
    def _get_scene_cell_type_at(self, row: int, col: int) -> SceneCellType:
        if self._active_cell == (row, col):
            return SceneCellType.ACTIVE
        if self._engine.get_cell_state_at(row, col) == CELL_ALIVE:
            return SceneCellType.ALIVE
        else:
            return SceneCellType.DEAD

    # Qt-Properties
    def get_is_game_running(self):
        return self._is_game_running

    def get_turn_duration(self):
        return self._turn_duration

    @property_setter_error_handle
    def set_turn_duration(self, value: int):
        if value < 100:
            raise ValueError("Turn duration must be greater than or equal to 100")
        self._turn_duration = value

    def get_border_thickness(self):
        return self._border_thickness

    @property_setter_error_handle
    def set_border_thickness(self, value: float):
        if value < 0 or value > 100:
            raise ValueError("Border thickness must be an percentage float number in the following range [0, 100]")
        self._border_thickness = value
        for border_item in self._border_item_map.values():
            border_item.set_thickness_percentage(value, scene_width=self.sceneRect().width())
        self.update()

    def get_border_color(self):
        return self._border_color

    @property_setter_error_handle
    def set_border_color(self, value: QColor):
        self._border_color = value
        for border_item in self._border_item_map.values():
            border_item.set_color(value)
        self.update()

    def get_cell_dead_color(self):
        return self._cell_dead_color

    @property_setter_error_handle
    def set_cell_dead_color(self, value: QColor):
        self._cell_dead_color = value
        for cell_item in self._cell_item_map.values():
            cell_item.update_color_map(SceneCellType.DEAD, value)
        self.update()

    def get_cell_alive_color(self):
        return self._cell_alive_color

    @property_setter_error_handle
    def set_cell_alive_color(self, value: QColor):
        self._cell_alive_color = value
        for cell_item in self._cell_item_map.values():
            cell_item.update_color_map(SceneCellType.ALIVE, value)
        self.update()

    # Public API
    def get_edit_mode(self):
        return self._cell_edit_mode

    def set_cell_edit_mode(self, value: CellEditMode):
        self._cell_edit_mode = value

    def insert_pattern(self, pattern_data: PatternSchema):
        if self._is_game_running:
            return

        self._engine.insert_state_array_at(self._active_cell[0],
                                           self._active_cell[1],
                                           pattern_data["state"])
        self._update_cell_item_types()

    # Game control
    def start_game(self):
        if self._is_game_running:
            return

        self._is_game_running = True
        self._active_cell = None
        self._timer.setInterval(self._turn_duration)
        self._timer.start()

        self.is_game_running_changed.emit(self._is_game_running)

    def stop_game(self):
        if not self._is_game_running:
            return

        self._is_game_running = False
        self._active_cell = (0, 0)
        self._timer.stop()

        self.is_game_running_changed.emit(self._is_game_running)

    def clear_state(self):
        self._engine.clear_state()
        self._update_cell_item_types()

    def reset_to_default(self):
        self.stop_game()
        self._reset_scene()
        self.update()

    # Event handlers
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.scenePos())
        if res is not None:
            row, col = res
            match self._cell_edit_mode:
                case CellEditMode.DEFAULT:
                    self._engine.change_cell_state_to_opposite(row, col)
                case CellEditMode.PAINT:
                    self._engine.change_cell_state_at(row, col, CELL_ALIVE)
                case CellEditMode.ERASE:
                    self._engine.change_cell_state_at(row, col, CELL_DEAD)

            self._update_cell_item_type(row, col)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.scenePos())
        if res is not None:
            row, col = res
            match self._cell_edit_mode:
                case CellEditMode.PAINT:
                    self._engine.change_cell_state_at(row, col, CELL_ALIVE)
                    self._update_cell_item_type(row, col)
                case CellEditMode.ERASE:
                    self._engine.change_cell_state_at(row, col, CELL_DEAD)
                    self._update_cell_item_type(row, col)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if self._is_game_running:
            return

        key = event.key()
        if key == Qt.Key.Key_Return:  # Enter key, not on the numeric keypad
            self._handle_return_key()
        elif key == Qt.Key.Key_Up:
            self._handle_arrow_key(-1, 0)
        elif key == Qt.Key.Key_Down:
            self._handle_arrow_key(1, 0)
        elif key == Qt.Key.Key_Left:
            self._handle_arrow_key(0, -1)
        elif key == Qt.Key.Key_Right:
            self._handle_arrow_key(0, 1)

    def _handle_return_key(self):
        self._engine.change_cell_state_to_opposite(*self._active_cell)
        self._update_cell_item_type(*self._active_cell)

    def _handle_arrow_key(self, row_delta: int, col_delta: int):
        new_row = self._active_cell[0] + row_delta
        new_col = self._active_cell[1] + col_delta
        old_active_cell = self._active_cell
        if 0 <= new_row < self._engine.rows and 0 <= new_col < self._engine.cols:
            self._active_cell = (new_row, new_col)
            self._update_cell_item_type(*old_active_cell)
            self._update_cell_item_type(new_row, new_col)

    # Geometry methods
    def _cell_coordinates_from_point(self, point: QPoint | QPointF) -> Optional[tuple[int, int]]:
        """
        Maps Scene point to the cell coordinates.
        """
        cell_size = self._cell_size()
        row = int(point.y() / cell_size.height())
        col = int(point.x() / cell_size.width())
        h_margin = row * cell_size.height()
        w_margin = col * cell_size.width()
        pos = QPointF(w_margin, h_margin)
        cell = QRectF(pos, cell_size)
        if cell.contains(point) and 0 <= row < self._engine.rows and 0 <= col < self._engine.cols:
            return row, col
        return None

    def _cell_width(self) -> float:
        return self.width() / self._engine.cols

    def _cell_height(self) -> float:
        return self.height() / self._engine.rows

    def _cell_size(self) -> QSizeF:
        return QSizeF(self._cell_width(), self._cell_height())

    def _cell_top_left_point(self, row: int, col: int) -> QPointF:
        h_margin = row * self._cell_height()
        w_margin = col * self._cell_width()
        return QPointF(w_margin, h_margin)

    def _cell_rect(self, row: int, col: int) -> QRectF:
        """
        Bound rect for the cell.
        """
        cell_size = self._cell_size()
        h_margin = row * cell_size.height()
        w_margin = col * cell_size.width()
        pos = QPointF(w_margin, h_margin)
        return QRectF(pos, cell_size)

    # Slots
    @Slot()
    def _handle_board_changed(self):
        """
        Handles 'board_changed' signal of an engine.
        """
        # Update the active cell, so it does not go off board
        if self._active_cell is not None:
            if self._active_cell[0] >= self._engine.rows:
                self._active_cell = (self._engine.rows, self._active_cell[1])
            if self._active_cell[1] >= self._engine.cols:
                self._active_cell = (self._active_cell[0], self._engine.cols - 1)

        self._update_scene_items()

    @Slot()
    def _make_turn(self):
        self._engine.make_turn()
        self._update_cell_item_types()

    # Signals.

    # Emits when invalid value passed to Qt-Property setter
    property_setter_error_signal = Signal(str, str)

    # Properties signals.

    # Must have '_NOTIFY_SIGNAL_SUFFIX' suffix.
    is_game_running_changed = Signal(bool)
    # Qt-Properties (notify is not 'automatic'):
    turn_duration = Property(int, get_turn_duration, set_turn_duration)
    border_thickness = Property(float, get_border_thickness, set_border_thickness)
    border_color = Property(QColor, get_border_color, set_border_color)
    cell_dead_color = Property(QColor, get_cell_dead_color, set_cell_dead_color)
    cell_alive_color = Property(QColor, get_cell_alive_color, set_cell_alive_color)
    # Read only
    is_game_running = Property(bool, get_is_game_running, notify=is_game_running_changed)

    # Abstract methods implementation
    _SAVABLE_PROPERTIES = \
        ["turn_duration",
         "border_thickness",
         "border_color",
         "cell_dead_color",
         "cell_alive_color"]

    @classmethod
    def savable_properties_names(cls) -> list[str]:
        return cls._SAVABLE_PROPERTIES

    _NOTIFY_SIGNAL_SUFFIX = "_changed"

    def get_property_notify_signal(self, name: str) -> Signal:
        name += self._NOTIFY_SIGNAL_SUFFIX
        if isinstance(signal := getattr(self, name, None), Signal):
            return signal
        raise ValueError
