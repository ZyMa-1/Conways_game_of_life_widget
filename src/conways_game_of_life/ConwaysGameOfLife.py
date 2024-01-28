from enum import Enum
from typing import Optional, Tuple, List

from PySide6.QtCore import QPoint, QTimer, Qt, Signal, Slot, Property, QPointF, QSizeF, QRectF, QSize
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

from .utils import property_setter_error_handle, ColorProperty, PatternSchema
from .ConwaysGameOfLifeEngine import CELL_ALIVE, CELL_DEAD, ConwaysGameOfLifeEngine

MINIMUM_SIZE = (240, 240)

DEFAULT_CELL_WIDTH = 30  # px (used only in size hints)
DEFAULT_BORDER_THICKNESS = 2  # (assigned to attribute)
DEFAULT_TURN_DURATION = 1500  # ms (assigned to attribute)
DEFAULT_CELL_DEAD_COLOR = QColor(255, 255, 255)  # (assigned to attribute)
DEFAULT_CELL_ALIVE_COLOR = QColor(173, 216, 230)  # (assigned to attribute)
DEFAULT_BORDER_COLOR = QColor(192, 192, 192)  # (assigned to attribute)
DEFAULT_ACTIVE_CELL_COLOR = QColor(235, 235, 235)  # (used)


class ConwaysGameOfLife(QWidget):
    """
    The main game widget class.
    Uses 'ConwaysGameOfLifeEngine' as an engine of the game.
    """

    class EditMode(Enum):
        DEFAULT = 0
        PAINT = 1
        ERASE = 2

    # Signals:
    # Emits when invalid value passed to property setter
    property_setter_error_signal = Signal(str, str)
    # Wrapped signals
    turn_number_changed = Signal(int)
    alive_cells_changed = Signal(int)
    dead_cells_changed = Signal(int)
    turn_made = Signal()
    # 1. Create wrapped signals
    # 2. Connect them in __init__
    # 3. Put them as notify signals

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set strong focus policy
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Set mouse tracking for better edit mode experience (it is not helping much)
        self.setMouseTracking(True)

        # Create game engine
        self.engine = ConwaysGameOfLifeEngine(parent)

        # Create widget attributes
        self._border_thickness = DEFAULT_BORDER_THICKNESS
        self._border_color = ColorProperty(DEFAULT_BORDER_COLOR)
        self._cell_alive_color = ColorProperty(DEFAULT_CELL_ALIVE_COLOR)
        self._cell_dead_color = ColorProperty(DEFAULT_CELL_DEAD_COLOR)
        self._is_game_running = False
        self._edit_mode = ConwaysGameOfLife.EditMode.DEFAULT
        self._turn_duration = DEFAULT_TURN_DURATION
        # Active cell should be (if not messed up) synced with '_is_game_running'
        # (_is_game_running == False) -> _active cell is None, since no editing is allowed
        self._active_cell: Optional[Tuple[int, int]] = (0, 0)
        self._square_size_constraint = False

        # Turn timer
        self._timer = QTimer(self)

        # Connect signals to slots
        self._timer.timeout.connect(self.engine.make_turn)
        # Connect engine signals
        self.engine.property_setter_error_signal.connect(self.property_setter_error_signal)
        self.engine.board_changed.connect(self._handle_board_changed)
        self.engine.turn_made.connect(self.update)
        self.engine.turn_number_changed.connect(self.turn_number_changed)
        self.engine.alive_cells_changed.connect(self.alive_cells_changed)
        self.engine.dead_cells_changed.connect(self.dead_cells_changed)
        self.engine.turn_made.connect(self.turn_made)

    def _reset_to_defaults(self):
        self._border_thickness = DEFAULT_BORDER_THICKNESS
        self._border_color = ColorProperty(DEFAULT_BORDER_COLOR)
        self._cell_alive_color = ColorProperty(DEFAULT_CELL_ALIVE_COLOR)
        self._cell_dead_color = ColorProperty(DEFAULT_CELL_DEAD_COLOR)
        self._is_game_running = False
        # Nuh-uh,
        # self._edit_mode = ConwaysGameOfLife.EditMode.DEFAULT
        self._turn_duration = DEFAULT_TURN_DURATION
        self._active_cell = (0, 0)

        self.engine.reset_to_defaults()

    # Properties
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
    def set_border_thickness(self, value: int):
        if value < 0 or value > 10:
            raise ValueError("Border thickness must be an integer in the following range [0, 10]")
        self._border_thickness = value
        self.update()

    def get_border_color(self):
        return self._border_color.color

    @property_setter_error_handle
    def set_border_color(self, value: QColor | Tuple[int, int, int]):
        self._border_color.set_color(value)
        self.update()

    def get_cell_dead_color(self):
        return self._cell_dead_color.color

    @property_setter_error_handle
    def set_cell_dead_color(self, value: QColor | Tuple[int, int, int]):
        self._cell_dead_color.set_color(value)
        self.update()

    def get_cell_alive_color(self):
        return self._cell_alive_color.color

    @property_setter_error_handle
    def set_cell_alive_color(self, value: QColor | Tuple[int, int, int]):
        self._cell_alive_color.set_color(value)
        self.update()

    # API functionality to interact with the widget
    def set_edit_mode(self, value: EditMode):
        self._edit_mode = value

    def insert_pattern(self, pattern_data: PatternSchema):
        if self._is_game_running:
            return

        self.engine.insert_state_array_at(self._active_cell[0],
                                          self._active_cell[1],
                                          pattern_data["state"])
        self.update()

    def set_perfect_size(self):
        # not used/deprecated
        old_width = self.width()
        old_height = self.height()
        w_border = self._border_thickness * (self.engine.cols + 1)
        h_border = self._border_thickness * (self.engine.rows + 1)
        new_width = (old_width - w_border) // self.engine.cols * self.engine.cols + w_border
        new_height = (old_height - h_border) // self.engine.rows * self.engine.rows + h_border
        # print(old_width, old_height, new_width, new_height)
        self.resize(new_width, new_height)

    def set_square_size_constraint(self, value: bool):
        self._square_size_constraint = value
        if self._square_size_constraint:
            size = min(self.width(), self.height())
            self.resize(size, size)
        self.updateGeometry()
        self.update()

    # Game control methods
    def start_game(self):
        if self._is_game_running:
            return

        self._is_game_running = True
        self._active_cell = None
        self._timer.setInterval(self._turn_duration)
        self._timer.start()

        self.is_game_running_changed.emit(self._is_game_running)
        self.update()

    def stop_game(self):
        if not self._is_game_running:
            return

        self._is_game_running = False
        self._active_cell = (0, 0)
        self._timer.stop()

        self.is_game_running_changed.emit(self._is_game_running)
        self.update()

    def clear_state(self):
        self.engine.clear_state()
        self.update()

    def reset_to_default(self):
        self.stop_game()
        self._reset_to_defaults()
        self.update()

    # Event handlers
    def mousePressEvent(self, event):
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            match self._edit_mode:
                case ConwaysGameOfLife.EditMode.DEFAULT:
                    self.engine.change_cell_state_to_opposite(row, col)
                case ConwaysGameOfLife.EditMode.PAINT:
                    self.engine.change_cell_state_at(row, col, CELL_ALIVE)
                case ConwaysGameOfLife.EditMode.ERASE:
                    self.engine.change_cell_state_at(row, col, CELL_DEAD)

            self.update()

    def mouseMoveEvent(self, event):
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            if self._edit_mode == ConwaysGameOfLife.EditMode.PAINT:
                self.engine.change_cell_state_at(row, col, CELL_ALIVE)
                self.update()
            elif self._edit_mode == ConwaysGameOfLife.EditMode.ERASE:
                self.engine.change_cell_state_at(row, col, CELL_DEAD)
                self.update()

    def keyPressEvent(self, event):
        if self._is_game_running:
            return

        key = event.key()
        if key == Qt.Key.Key_Return:  # Enter key, not on the numeric keypad
            self._handle_enter_key()
        elif key == Qt.Key.Key_Up:
            self._handle_arrow_key(-1, 0)
        elif key == Qt.Key.Key_Down:
            self._handle_arrow_key(1, 0)
        elif key == Qt.Key.Key_Left:
            self._handle_arrow_key(0, -1)
        elif key == Qt.Key.Key_Right:
            self._handle_arrow_key(0, 1)

    def _handle_enter_key(self):
        self.engine.change_cell_state_to_opposite(*self._active_cell)
        self.update()

    def _handle_arrow_key(self, row_delta: int, col_delta: int):
        new_row = self._active_cell[0] + row_delta
        new_col = self._active_cell[1] + col_delta
        if 0 <= new_row < self.engine.rows and 0 <= new_col < self.engine.cols:
            self._active_cell = (new_row, new_col)
            self.update()

    # Widget's geometry/paint methods
    def _cell_coordinates_from_point(self, point: QPoint) -> Optional[Tuple[int, int]]:
        row = int((point.y() - self._border_thickness) / (self._border_thickness + self._cell_height()))
        col = int((point.x() - self._border_thickness) / (self._border_thickness + self._cell_width()))
        cell = self._cell_rect(row, col)
        if cell.contains(point) and 0 <= row < self.engine.rows and 0 <= col <= self.engine.cols:
            return row, col
        return None

    def _cell_width(self) -> float:
        return (self.width() - (self.engine.cols + 1) * self._border_thickness) / self.engine.cols

    def _cell_height(self) -> float:
        return (self.height() - (self.engine.rows + 1) * self._border_thickness) / self.engine.rows

    def _cell_top_left_point(self, row: int, col: int) -> QPointF:
        h_margin = row * (self._border_thickness + self._cell_height()) + self._border_thickness
        w_margin = col * (self._border_thickness + self._cell_width()) + self._border_thickness
        return QPointF(w_margin, h_margin)

    def _cell_rect(self, row, col) -> QRectF:
        h_margin = row * (self._border_thickness + self._cell_height()) + self._border_thickness
        w_margin = col * (self._border_thickness + self._cell_width()) + self._border_thickness
        pos = QPoint(w_margin, h_margin)
        size = QSizeF(self._cell_width(), self._cell_height())
        return QRectF(pos, size)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw borders
            for row in range(self.engine.rows + 1):
                cell_point = self._cell_top_left_point(row, 0)
                line_rect = QRectF(cell_point.x() - self._border_thickness,
                                   cell_point.y() - self._border_thickness,
                                   self.width(),
                                   self._border_thickness)
                painter.fillRect(line_rect, self._border_color.color)
            for col in range(self.engine.cols + 1):
                cell_point = self._cell_top_left_point(0, col)
                line_rect = QRectF(cell_point.x() - self._border_thickness,
                                   cell_point.y() - self._border_thickness,
                                   self._border_thickness,
                                   self.height())
                painter.fillRect(line_rect, self._border_color.color)

            # Draw cells
            game_state = self.engine.state
            for row in range(self.engine.rows):
                for col in range(self.engine.cols):
                    cell = self._cell_rect(row, col)
                    if self._active_cell == (row, col):
                        painter.fillRect(cell, DEFAULT_ACTIVE_CELL_COLOR)
                    elif game_state[row][col] == CELL_ALIVE:
                        painter.fillRect(cell, self._cell_alive_color.color)
                    else:
                        painter.fillRect(cell, self._cell_dead_color.color)

    # Handlers for the inner signals
    @Slot()
    def _handle_board_changed(self):
        """Handles 'board_changed' signal of the engine"""
        if self._active_cell is not None:
            if self._active_cell[0] >= self.engine.rows:
                self._active_cell = (self.engine.rows - 1, self._active_cell[1])
            if self._active_cell[1] >= self.engine.cols:
                self._active_cell = (self._active_cell[0], self.engine.cols - 1)

        self.update()

    # Miscellaneous stuff
    def minimumSizeHint(self):
        return QSize(*MINIMUM_SIZE)

    def sizeHint(self):
        return QSize((self._border_thickness + self._cell_width()) * self.engine.rows + self._border_thickness,
                     (self._border_thickness + self._cell_height()) * self.engine.cols + self._border_thickness)

    def resizeEvent(self, event):
        if self._square_size_constraint:
            size = min(self.width(), self.height())
            self.resize(size, size)
        super().resizeEvent(event)

    # Signal suffix for the properties signals
    _SIGNAL_SUFFIX = "_changed"

    # Properties signals
    is_game_running_changed = Signal(bool)

    # Pyqt properties (notify is not 'automatic'):
    turn_duration = Property(int, get_turn_duration, set_turn_duration)
    border_thickness = Property(int, get_border_thickness, set_border_thickness)
    border_color = Property(QColor, get_border_color, set_border_color)
    cell_dead_color = Property(QColor, get_cell_dead_color, set_cell_dead_color)
    cell_alive_color = Property(QColor, get_cell_alive_color, set_cell_alive_color)
    # Read only
    is_game_running = Property(bool, get_is_game_running, notify=is_game_running_changed)

    # Wrapped properties of the engine (using lambdas)
    state = Property(list, lambda self: self.engine.get_state(), lambda self, val: self.engine.set_state(val))
    rows = Property(int, lambda self: self.engine.get_rows(), lambda self, val: self.engine.set_rows(val))
    cols = Property(int, lambda self: self.engine.get_cols(), lambda self, val: self.engine.set_cols(val))
    turn_number = Property(int, lambda self: self.engine.get_turn_number(), notify=turn_number_changed)
    alive_cells = Property(int, lambda self: self.engine.get_alive_cells(), notify=alive_cells_changed)
    dead_cells = Property(int, lambda self: self.engine.get_dead_cells(), notify=dead_cells_changed)

    # Stuff to json serialize the widget
    _SELF_SAVABLE_PROPERTIES = \
        ["turn_duration",
         "border_thickness",
         "border_color",
         "cell_dead_color",
         "cell_alive_color"]
    _ENGINE_SAVABLE_PROPERTIES = \
        ["cols",
         "rows",
         "state"]
    _SAVABLE_PROPERTIES = _SELF_SAVABLE_PROPERTIES + _ENGINE_SAVABLE_PROPERTIES

    # Extra methods regarding properties and their signals
    def get_property_changed_signal(self, name: str) -> Signal:
        name += self._SIGNAL_SUFFIX
        if isinstance(signal := getattr(self, name, None), Signal):
            return signal
        raise ValueError

    @classmethod
    def savable_properties_names(cls) -> List[str]:
        """Returns list of savable properties associated specifically with this widget"""
        return cls._SAVABLE_PROPERTIES
