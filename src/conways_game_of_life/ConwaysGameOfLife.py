"""
Conway's game of life.

Author: ZyMa-1
"""
from enum import Enum
from typing import List

from PySide6.QtCore import QPoint, QRect, QSize, QTimer, Qt, Signal, Slot, Property
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QWidget

from .utils import *

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


# ...*......
# ...*......
# ..***.....
# ..........
# ..........

class ConwaysGameOfLife(QWidget):
    class EditMode(Enum):
        DEFAULT = 0
        PAINT = 1
        ERASE = 2

    # Inner signals:
    _layout_changed = Signal()  # Emits when number of rows or cols changed
    property_setter_error_signal = Signal(str, str)  # Emits when  invalid value passed to property setter

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
        self._active_cell: None | Tuple[int, int] = (0, 0)
        self._state = [[CELL_DEAD for col in range(self._cols)] for row in range(self._rows)]

        # Other widget parts
        self._timer = QTimer(self)

        # Connect signals to slots
        self._timer.timeout.connect(self._make_turn)
        self._layout_changed.connect(self._handle_layout_changed)

    def _assign_default_attribute_values(self):
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
        self._state = [[CELL_DEAD for col in range(self._cols)] for row in range(self._rows)]

    # Properties :[
    def get_turn_number(self):
        return self._turn_number

    def get_is_game_running(self):
        return self._is_game_running

    def get_state(self):
        return self._state

    @property_setter_error_handle
    def set_state(self, value: List[List[str]]):
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
            raise ValueError("Border thickness must be a non negative and not very big integer")
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

    # API functionality

    def setEditMode(self, value: EditMode):
        self._edit_mode = value

    def insert_pattern(self, pattern_data: dict):
        if self._is_game_running or self._active_cell is None:
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

    # :Logic functions:

    def _adjust_state(self):
        """Adjusts state according to new rows or cols count."""
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

    def _insert_state_array_at(self, row, col, state_array):
        for i in range(len(state_array)):
            for j in range(len(state_array[0])):
                self._state[i + row][j + col] = state_array[i][j]
        self.update()

    def _change_cell_state_at(self, row, col, new_cell_state):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            return

        self._state[row][col] = new_cell_state

    def _change_cell_state_to_opposite(self, row, col):
        if self._state[row][col] == CELL_ALIVE:
            self._change_cell_state_at(row, col, CELL_DEAD)
        elif self._state[row][col] == CELL_DEAD:
            self._change_cell_state_at(row, col, CELL_ALIVE)

    def _get_alive_neighbor_count(self, row, col):
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

    # !Game control functions!

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
        self._state = [[CELL_DEAD for col in range(self._cols)] for row in range(self._rows)]
        self.update()

    def reset_to_default(self):
        self.stop_game()
        self._assign_default_attribute_values()
        self.update()

        # ?Some interaction stuff?

    def mousePressEvent(self, event):
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            self._change_cell_state_to_opposite(row, col)
            self.update()

    def mouseMoveEvent(self, event):
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        match self._edit_mode:
            case ConwaysGameOfLife.EditMode.DEFAULT:
                self.mouseMoveEventDefault(event)
            case ConwaysGameOfLife.EditMode.PAINT:
                self.mouseMoveEventPaint(event)
            case ConwaysGameOfLife.EditMode.ERASE:
                self.mouseMoveEventErase(event)

    def mouseMoveEventDefault(self, event):
        pass

    def mouseMoveEventPaint(self, event):
        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            self._change_cell_state_at(row, col, CELL_ALIVE)
            self.update()

    def mouseMoveEventErase(self, event):
        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            self._change_cell_state_at(row, col, CELL_DEAD)
            self.update()

    def keyPressEvent(self, event):
        if self._is_game_running or self._active_cell is None:
            return

        if event.key() == Qt.Key.Key_Return:  # Enter key, not on the numeric keypad
            self._change_cell_state_to_opposite(*self._active_cell)
            self.update()
        elif event.key() == Qt.Key.Key_Up:
            if self._active_cell[0] != 0:
                self._active_cell = (self._active_cell[0] - 1, self._active_cell[1])
            self.update()
        elif event.key() == Qt.Key.Key_Down:
            if self._active_cell[0] != self._rows - 1:
                self._active_cell = (self._active_cell[0] + 1, self._active_cell[1])
            self.update()
        elif event.key() == Qt.Key.Key_Left:
            if self._active_cell[1] != 0:
                self._active_cell = (self._active_cell[0], self._active_cell[1] - 1)
            self.update()
        elif event.key() == Qt.Key.Key_Right:
            if self._active_cell[1] != self._cols - 1:
                self._active_cell = (self._active_cell[0], self._active_cell[1] + 1)
            self.update()

        super().keyPressEvent(event)

    # !!Paint related functions!!

    def _cell_coordinates_from_point(self, point: QPoint) -> Tuple[int, int] | None:
        row = int((point.y() - self._border_thickness) / (self._border_thickness + self._cell_height()))
        col = int((point.x() - self._border_thickness) / (self._border_thickness + self._cell_width()))
        cell = self._cell_rect(row, col)
        return (row, col) if cell.contains(point) and 0 <= row < self._rows and 0 <= col <= self._cols else None

    def _cell_width(self):
        return (self.width() - (self._cols + 1) * self._border_thickness) / self._cols

    def _cell_height(self):
        return (self.height() - (self._rows + 1) * self._border_thickness) / self._rows

    def _cell_top_left_point(self, row, col):
        h_margin = row * (self._border_thickness + self._cell_height()) + self._border_thickness
        w_margin = col * (self._border_thickness + self._cell_width()) + self._border_thickness
        return QPoint(w_margin, h_margin)

    def _cell_rect(self, row, col):
        h_margin = row * (self._border_thickness + self._cell_height()) + self._border_thickness
        w_margin = col * (self._border_thickness + self._cell_width()) + self._border_thickness
        pos = QPoint(w_margin, h_margin)
        size = QSize(self._cell_width(), self._cell_height())
        return QRect(pos, size)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw borders

            for row in range(self._rows + 1):
                cell_point = self._cell_top_left_point(row, 0)
                line_rect = QRect(cell_point.x() - self._border_thickness,
                                  cell_point.y() - self._border_thickness,
                                  self.width(),
                                  self._border_thickness)
                painter.fillRect(line_rect, self._border_color.color)
            for col in range(self._cols + 1):
                cell_point = self._cell_top_left_point(0, col)
                line_rect = QRect(cell_point.x() - self._border_thickness,
                                  cell_point.y() - self._border_thickness,
                                  self._border_thickness,
                                  self.height())
                painter.fillRect(line_rect, self._border_color.color)

            # Draw cells

            for row in range(self._rows):
                for col in range(self._cols):
                    cell = self._cell_rect(row, col)
                    if self._active_cell is not None and self._active_cell == (row, col):
                        painter.fillRect(cell, DEFAULT_ACTIVE_CELL_COLOR)
                    elif self._state[row][col] == CELL_ALIVE:
                        painter.fillRect(cell, self._cell_alive_color.color)
                    else:
                        painter.fillRect(cell, self._cell_dead_color.color)

    # !!!Inner signals handlers!!!

    @Slot()
    def _handle_layout_changed(self):
        """Handles changes in a widget layout, that is number of 'rows' or 'cols' have changed."""
        self._adjust_state()
        if self._active_cell is not None and self._active_cell[0] >= self._rows:
            self._active_cell = (self._rows - 1, self._active_cell[1])
        if self._active_cell is not None and self._active_cell[1] >= self._cols:
            self._active_cell = (self._active_cell[0], self._cols - 1)
        self.update()

    # .Other overriden functions.

    def minimumSizeHint(self):
        return QSize(322, 322)

    def sizeHint(self):
        return QSize((self._border_thickness + self._cell_width()) * self._rows + self._border_thickness,
                     (self._border_thickness + self._cell_height()) * self._cols + self._border_thickness)

    def resizeEvent(self, event):
        # Square
        size = min(self.width(), self.height())
        self.resize(size, size)

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

    # Pyqt properties:
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
        """Returns list of savable properties associated specifically with this widget."""
        return ["cols", "rows", "turn_duration", "border_thickness", "border_color", "cell_dead_color",
                "cell_alive_color", "state"]

    @staticmethod
    def all_dynamic_properties_name_list() -> List[str]:
        """Returns list of all properties associated specifically with this widget."""
        return ["cols", "rows", "turn_duration", "border_thickness", "border_color", "cell_dead_color",
                "cell_alive_color", "is_game_running", "turn_number", "state"]
