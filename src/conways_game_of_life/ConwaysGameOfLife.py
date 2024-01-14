from enum import Enum
from typing import Optional

from PySide6.QtCore import QPoint, QTimer, Qt, Signal, Slot, Property, QPointF, QSizeF, QRectF, QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from .utils import *

MINIMUM_SIZE = (322, 322)

DEFAULT_COLS = 10  # px (assigned to attribute)
DEFAULT_ROWS = 10  # px (assigned to attribute)
DEFAULT_CELL_WIDTH = 30  # px (used only in size hints)
DEFAULT_BORDER_THICKNESS = 2  # (assigned to attribute)
DEFAULT_TURN_DURATION = 1500  # ms (assigned to attribute)
DEFAULT_CELL_DEAD_COLOR = QColor(255, 255, 255)  # (assigned to attribute)
DEFAULT_CELL_ALIVE_COLOR = QColor(173, 216, 230)  # (assigned to attribute)
DEFAULT_BORDER_COLOR = QColor(192, 192, 192)  # (assigned to attribute)
DEFAULT_ACTIVE_CELL_COLOR = QColor(235, 235, 235)  # (used)
CELL_ALIVE = '*'  # (used)
CELL_DEAD = '.'  # (used)

DEFAULT_STATE = [[CELL_DEAD for col in range(DEFAULT_COLS)] for row in
                 range(DEFAULT_ROWS)]  # (used nowhere)

StateMatrixT = List[List[str]]


def _default_state_matrix(rows: int, cols: int) -> StateMatrixT:
    return [[CELL_DEAD for _ in range(cols)] for _ in range(rows)]


class ConwaysGameOfLife(QWidget):
    class EditMode(Enum):
        DEFAULT = 0
        PAINT = 1
        ERASE = 2

    # Inner signals:
    _layout_changed = Signal()  # Emits when number of rows or cols changed
    property_setter_error_signal = Signal(str, str)  # Emits when invalid value passed to property setter

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set strong focus policy
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Set mouse tracking for better edit mode experience (it is not helping much)
        self.setMouseTracking(True)

        # Create widget parameters
        self._turn_number = 0
        self._border_thickness = DEFAULT_BORDER_THICKNESS
        self._border_color = ColorProperty(DEFAULT_BORDER_COLOR)
        self._cell_alive_color = ColorProperty(DEFAULT_CELL_ALIVE_COLOR)
        self._cell_dead_color = ColorProperty(DEFAULT_CELL_DEAD_COLOR)
        self._is_game_running = False
        self._edit_mode = ConwaysGameOfLife.EditMode.DEFAULT
        self._cols = DEFAULT_COLS
        self._rows = DEFAULT_ROWS
        self._turn_duration = DEFAULT_TURN_DURATION
        # Active cell is synced with '_is_game_running'
        self._active_cell: Optional[Tuple[int, int]] = (0, 0)
        # List[List[str]] str is char
        self._state: StateMatrixT = _default_state_matrix(self._rows, self._cols)

        # Turn timer
        self._timer = QTimer(self)

        # Connect signals to slots
        self._timer.timeout.connect(self._make_turn)
        self._layout_changed.connect(self._handle_layout_changed)

    def _reset_to_defaults(self):
        self._turn_number = 0
        self._border_thickness = DEFAULT_BORDER_THICKNESS
        self._border_color = ColorProperty(DEFAULT_BORDER_COLOR)
        self._cell_alive_color = ColorProperty(DEFAULT_CELL_ALIVE_COLOR)
        self._cell_dead_color = ColorProperty(DEFAULT_CELL_DEAD_COLOR)
        self._is_game_running = False
        self._edit_mode = ConwaysGameOfLife.EditMode.DEFAULT
        self._cols = DEFAULT_COLS
        self._rows = DEFAULT_ROWS
        self._turn_duration = DEFAULT_TURN_DURATION
        self._active_cell: None | Tuple[int, int] = (0, 0)
        self._state = _default_state_matrix(self._rows, self._cols)

    # Properties
    def get_turn_number(self):
        return self._turn_number

    def get_is_game_running(self):
        return self._is_game_running

    def get_state(self):
        return self._state

    @property_setter_error_handle
    def set_state(self, value: StateMatrixT):
        if not isinstance(value, list) or len(value) != self._rows:
            raise ValueError("State value is not correct")

        for row in range(self._rows):
            if len(value[row]) != self._cols:
                raise ValueError("State value is not correct")

            for col in range(self._cols):
                if len(value[row][col]) != 1 or (value[row][col] != CELL_DEAD and value[row][col] != CELL_ALIVE):
                    raise ValueError("State value is not correct")

        self._state = value
        self.update()
        self.state_changed.emit(self._state)

    def get_cols(self):
        return self._cols

    @property_setter_error_handle
    def set_cols(self, value: int):
        if value <= 0:
            raise ValueError("Columns value must be positive")
        self._cols = value
        self._layout_changed.emit()
        self.cols_changed.emit(self._cols)

    def get_rows(self):
        return self._rows

    @property_setter_error_handle
    def set_rows(self, value: int):
        if value <= 0:
            raise ValueError("Rows value must be positive")
        self._rows = value
        self._layout_changed.emit()
        self.rows_changed.emit(self._rows)

    def get_turn_duration(self):
        return self._turn_duration

    @property_setter_error_handle
    def set_turn_duration(self, value: int):
        if value <= 100:
            raise ValueError("Turn duration must be greater than 100")
        self._turn_duration = value
        self.turn_duration_changed.emit(self._turn_duration)

    def get_border_thickness(self):
        return self._border_thickness

    @property_setter_error_handle
    def set_border_thickness(self, value: int):
        if value < 0 or value > 10:
            raise ValueError("Border thickness must be an integer in the following range [0, 10]")
        self._border_thickness = value
        self.update()
        self.border_thickness_changed.emit(self._border_thickness)

    def get_border_color(self):
        return self._border_color.color

    @property_setter_error_handle
    def set_border_color(self, value: QColor | Tuple[int, int, int]):
        self._border_color.set_color(value)
        self.update()
        self.border_color_changed.emit(self._border_color.color)

    def get_cell_dead_color(self):
        return self._cell_dead_color.color

    @property_setter_error_handle
    def set_cell_dead_color(self, value: QColor | Tuple[int, int, int]):
        self._cell_dead_color.set_color(value)
        self.update()
        self.cell_dead_color_changed.emit(self._cell_dead_color.color)

    def get_cell_alive_color(self):
        return self._cell_alive_color.color

    @property_setter_error_handle
    def set_cell_alive_color(self, value: QColor | Tuple[int, int, int]):
        self._cell_alive_color.set_color(value)
        self.update()
        self.cell_alive_color_changed.emit(self._cell_alive_color.color)

    # API functionality to interact with the widget
    def set_edit_mode(self, value: EditMode):
        self._edit_mode = value

    def insert_pattern(self, pattern_data: PatternSchema):
        if self._is_game_running:
            return

        max_possible_rows = self._rows - self._active_cell[0]
        max_possible_cols = self._cols - self._active_cell[1]
        new_state = []
        for row in range(min(max_possible_rows, pattern_data["rows"])):
            new_row = []
            for col in range(min(max_possible_cols, pattern_data["cols"])):
                new_row.append(pattern_data["state"][row][col])
            new_state.append(new_row)

        self._insert_state_array_at(*self._active_cell, new_state)

    def set_perfect_size(self):
        old_width = self.width()
        old_height = self.height()
        w_border = self._border_thickness * (self._cols + 1)
        h_border = self._border_thickness * (self._rows + 1)
        new_width = (old_width - w_border) // self._cols * self._cols + w_border
        new_height = (old_height - h_border) // self._rows * self._rows + h_border
        # print(old_width, old_height, new_width, new_height)
        self.resize(new_width, new_height)

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
        self._state = _default_state_matrix(self._rows, self._cols)
        self.update()

    def reset_to_default(self):
        self.stop_game()
        self._reset_to_defaults()
        self.update()

    # Inner logic
    def _adjust_state(self):
        """Adjusts state according to new rows or cols count"""
        rows = len(self._state)
        cols = len(self._state[0])
        if rows != self._rows or cols != self._cols:
            new_state = []
            for row in range(self._rows):
                new_row = []
                for col in range(self._cols):
                    if row < rows and col < cols:
                        new_row.append(self._state[row][col])
                    else:
                        new_row.append(CELL_DEAD)
                new_state.append(new_row)
            self._state = new_state

    def _insert_state_array_at(self, row: int, col: int, state_array: StateMatrixT):
        for i in range(len(state_array)):
            for j in range(len(state_array[0])):
                self._state[i + row][j + col] = state_array[i][j]
        self.update()

    def _change_cell_state_at(self, row: int, col: int, new_cell_state: str):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            return
        self._state[row][col] = new_cell_state

    def _change_cell_state_to_opposite(self, row: int, col: int):
        if self._state[row][col] == CELL_ALIVE:
            self._change_cell_state_at(row, col, CELL_DEAD)
        elif self._state[row][col] == CELL_DEAD:
            self._change_cell_state_at(row, col, CELL_ALIVE)

    def _get_alive_neighbor_count(self, row: int, col: int):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i != row or j != col) and 0 <= i < self._rows and 0 <= j < self._cols:
                    if self._state[i][j] == CELL_ALIVE:
                        count += 1
        return count

    @Slot()
    def _make_turn(self):
        self._turn_number += 1
        new_state = []
        for row in range(self._rows):
            new_row = []
            for col in range(self._cols):
                cell_state = self._state[row][col]
                neighbor_count = self._get_alive_neighbor_count(row, col)

                # Apply the rules of Conway's Game of Life
                if cell_state == CELL_ALIVE and (neighbor_count < 2 or neighbor_count > 3):
                    new_row.append(CELL_DEAD)
                elif cell_state == CELL_DEAD and neighbor_count == 3:
                    new_row.append(CELL_ALIVE)
                else:
                    new_row.append(cell_state)

            new_state.append(new_row)

        self._state = new_state
        self.turn_number_changed.emit(self._turn_number)
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
                    self._change_cell_state_to_opposite(row, col)
                case ConwaysGameOfLife.EditMode.PAINT:
                    self._change_cell_state_at(row, col, CELL_ALIVE)
                case ConwaysGameOfLife.EditMode.ERASE:
                    self._change_cell_state_at(row, col, CELL_DEAD)

            self.update()

    def mouseMoveEvent(self, event):
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            if self._edit_mode == ConwaysGameOfLife.EditMode.PAINT:
                self._change_cell_state_at(row, col, CELL_ALIVE)
                self.update()
            elif self._edit_mode == ConwaysGameOfLife.EditMode.ERASE:
                self._change_cell_state_at(row, col, CELL_DEAD)
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
        self._change_cell_state_to_opposite(*self._active_cell)
        self.update()

    def _handle_arrow_key(self, row_delta: int, col_delta: int):
        new_row = self._active_cell[0] + row_delta
        new_col = self._active_cell[1] + col_delta
        if 0 <= new_row < self._rows and 0 <= new_col < self._cols:
            self._active_cell = (new_row, new_col)
            self.update()

    # Paint methods

    def _cell_coordinates_from_point(self, point: QPoint) -> Optional[Tuple[int, int]]:
        row = int((point.y() - self._border_thickness) / (self._border_thickness + self._cell_height()))
        col = int((point.x() - self._border_thickness) / (self._border_thickness + self._cell_width()))
        cell = self._cell_rect(row, col)
        return (row, col) if cell.contains(point) and 0 <= row < self._rows and 0 <= col <= self._cols else None

    def _cell_width(self) -> float:
        return (self.width() - (self._cols + 1) * self._border_thickness) / self._cols

    def _cell_height(self) -> float:
        return (self.height() - (self._rows + 1) * self._border_thickness) / self._rows

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
            for row in range(self._rows + 1):
                cell_point = self._cell_top_left_point(row, 0)
                line_rect = QRectF(cell_point.x() - self._border_thickness,
                                   cell_point.y() - self._border_thickness,
                                   self.width(),
                                   self._border_thickness)
                painter.fillRect(line_rect, self._border_color.color)
            for col in range(self._cols + 1):
                cell_point = self._cell_top_left_point(0, col)
                line_rect = QRectF(cell_point.x() - self._border_thickness,
                                   cell_point.y() - self._border_thickness,
                                   self._border_thickness,
                                   self.height())
                painter.fillRect(line_rect, self._border_color.color)

            # Draw cells
            for row in range(self._rows):
                for col in range(self._cols):
                    cell = self._cell_rect(row, col)
                    if self._active_cell == (row, col):
                        painter.fillRect(cell, DEFAULT_ACTIVE_CELL_COLOR)
                    elif self._state[row][col] == CELL_ALIVE:
                        painter.fillRect(cell, self._cell_alive_color.color)
                    else:
                        painter.fillRect(cell, self._cell_dead_color.color)

    # Inner signal handlers
    @Slot()
    def _handle_layout_changed(self):
        """Handles changes in a widget layout, that is number of 'rows' or 'cols' have changed."""
        self._adjust_state()
        if self._active_cell is not None and self._active_cell[0] >= self._rows:
            self._active_cell = (self._rows - 1, self._active_cell[1])
        if self._active_cell is not None and self._active_cell[1] >= self._cols:
            self._active_cell = (self._active_cell[0], self._cols - 1)
        self.update()

    # Size hint stuff
    def minimumSizeHint(self):
        return QSize(*MINIMUM_SIZE)

    def sizeHint(self):
        return QSize((self._border_thickness + self._cell_width()) * self._rows + self._border_thickness,
                     (self._border_thickness + self._cell_height()) * self._cols + self._border_thickness)

    def resizeEvent(self, event):
        # Square
        size = min(self.width(), self.height())
        self.resize(size, size)
        super().resizeEvent(event)

    def focusInEvent(self, event):
        # Set focus whenever widget is available
        # Consider grabKeyboard func.
        self.setFocus()
        super().focusInEvent(event)

    # Properties signals
    state_changed = Signal(list)
    cols_changed = Signal(int)
    rows_changed = Signal(int)
    turn_duration_changed = Signal(int)
    border_thickness_changed = Signal(int)
    border_color_changed = Signal(QColor)
    cell_dead_color_changed = Signal(QColor)
    cell_alive_color_changed = Signal(QColor)
    is_game_running_changed = Signal(bool)
    turn_number_changed = Signal(int)

    # Pyqt properties (notify is not 'automatic'):
    state = Property(list, get_state, set_state, notify=state_changed)  # Does not work in Qt-Designer
    cols = Property(int, get_cols, set_cols, notify=cols_changed)
    rows = Property(int, get_rows, set_rows, notify=rows_changed)
    turn_duration = Property(int, get_turn_duration, set_turn_duration, notify=turn_duration_changed)
    border_thickness = Property(int, get_border_thickness, set_border_thickness, notify=state_changed)
    border_color = Property(QColor, get_border_color, set_border_color, notify=border_color_changed)
    cell_dead_color = Property(QColor, get_cell_dead_color, set_cell_dead_color, notify=cell_dead_color_changed)
    cell_alive_color = Property(QColor, get_cell_alive_color, set_cell_alive_color, notify=cell_alive_color_changed)
    # read_only
    is_game_running = Property(bool, fget=get_is_game_running, constant=True)
    turn_number = Property(int, fget=get_turn_number, constant=True)

    @staticmethod
    def savable_properties_name_list() -> List[str]:
        """Returns list of savable properties associated specifically with this widget"""
        return ["cols", "rows", "turn_duration", "border_thickness", "border_color", "cell_dead_color",
                "cell_alive_color", "state"]

    @staticmethod
    def all_properties_name_list() -> List[str]:
        """Returns list of all properties associated specifically with this widget"""
        return ["cols", "rows", "turn_duration", "border_thickness", "border_color", "cell_dead_color",
                "cell_alive_color", "is_game_running", "turn_number", "state"]
