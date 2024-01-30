import time
from abc import ABCMeta
from enum import Enum
from typing import Optional, Tuple, List

from PySide6.QtCore import QPoint, QTimer, Qt, Signal, Slot, Property, QPointF, QSizeF, QRectF, QSize
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget

from .abcs import MySerializable, MyPropertySignalAccessor
from .utils import property_setter_error_handle, ColorProperty, PatternSchema
from .ConwaysGameOfLifeEngine import CELL_ALIVE, CELL_DEAD, ConwaysGameOfLifeEngine

MINIMUM_SIZE = (264, 264)

DEFAULT_CELL_WIDTH = 30  # px (used only in size hints)
DEFAULT_BORDER_THICKNESS = 2  # (assigned to attribute)
DEFAULT_TURN_DURATION = 1500  # ms (assigned to attribute)
DEFAULT_CELL_DEAD_COLOR = QColor(255, 255, 255)  # (assigned to attribute)
DEFAULT_CELL_ALIVE_COLOR = QColor(173, 216, 230)  # (assigned to attribute)
DEFAULT_BORDER_COLOR = QColor(192, 192, 192)  # (assigned to attribute)
DEFAULT_ACTIVE_CELL_COLOR = QColor(235, 235, 235)  # (used)


class _MyMeta(type(QWidget), ABCMeta):
    pass


class ConwaysGameOfLife(QWidget, MySerializable, MyPropertySignalAccessor, metaclass=_MyMeta):
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
    # Emits after every paintEvent method
    paint_event_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set strong focus policy
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Set mouse tracking true
        self.setMouseTracking(True)

        # Create game engine
        self._engine = ConwaysGameOfLifeEngine(parent)

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
        self._perfect_size_constraint = False
        self._last_update_time = time.perf_counter()
        self._sum_paint_performance = 0
        self._paint_count = 0

        # Turn timer
        self._timer = QTimer(self)

        # Connect signals to slots
        self._timer.timeout.connect(self._engine.make_turn)
        # Connect engine signals
        self._engine.property_setter_error_signal.connect(self.property_setter_error_signal)
        self._engine.board_changed.connect(self._handle_board_changed)
        self._engine.turn_made.connect(self.update)

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
        self._sum_paint_performance = 0
        self._paint_count = 0

        self._engine.reset_to_defaults()

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

    # Public stuff
    def engine(self):
        return self._engine

    def get_avg_paint_performance(self):
        return self._sum_paint_performance / self._paint_count

    def set_edit_mode(self, value: EditMode):
        self._edit_mode = value

    def insert_pattern(self, pattern_data: PatternSchema):
        if self._is_game_running:
            return

        self._engine.insert_state_array_at(self._active_cell[0],
                                           self._active_cell[1],
                                           pattern_data["state"])
        self.update()

    def set_square_size_constraint(self, value: bool):
        self._square_size_constraint = value
        cur_size = self.size()
        if value:
            cur_size = self._get_square_size(cur_size)
        self.resize(cur_size)

    def set_perfect_size_constraint(self, value: bool):
        self._perfect_size_constraint = value
        cur_size = self.size()
        if value:
            cur_size = self._get_perfect_size(cur_size)
        self.resize(cur_size)

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
        self._engine.clear_state()
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
                    self._engine.change_cell_state_to_opposite(row, col)
                case ConwaysGameOfLife.EditMode.PAINT:
                    self._engine.change_cell_state_at(row, col, CELL_ALIVE)
                case ConwaysGameOfLife.EditMode.ERASE:
                    self._engine.change_cell_state_at(row, col, CELL_DEAD)

            self.update()

    def mouseMoveEvent(self, event):
        if self._is_game_running or event.buttons() != Qt.MouseButton.LeftButton:
            return

        res = self._cell_coordinates_from_point(event.position().toPoint())
        if res is not None:
            row, col = res
            if self._edit_mode == ConwaysGameOfLife.EditMode.PAINT:
                self._engine.change_cell_state_at(row, col, CELL_ALIVE)
                self.update()
            elif self._edit_mode == ConwaysGameOfLife.EditMode.ERASE:
                self._engine.change_cell_state_at(row, col, CELL_DEAD)
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
        self._engine.change_cell_state_to_opposite(*self._active_cell)
        self.update()

    def _handle_arrow_key(self, row_delta: int, col_delta: int):
        new_row = self._active_cell[0] + row_delta
        new_col = self._active_cell[1] + col_delta
        if 0 <= new_row < self._engine.rows and 0 <= new_col < self._engine.cols:
            self._active_cell = (new_row, new_col)
            self.update()

    # Widget's geometry/paint methods
    def _cell_coordinates_from_point(self, point: QPoint) -> Optional[Tuple[int, int]]:
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
        cell_size = self._cell_size()
        h_margin = row * cell_size.height()
        w_margin = col * cell_size.width()
        pos = QPointF(w_margin, h_margin)
        return QRectF(pos, cell_size)

    def paintEvent(self, event):
        start_time = time.perf_counter()

        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw cells
            for row in range(self._engine.rows):
                for col in range(self._engine.cols):
                    cell = self._cell_rect(row, col)
                    if self._active_cell == (row, col):
                        painter.fillRect(cell, DEFAULT_ACTIVE_CELL_COLOR)
                    elif self._engine.get_cell_state_at(row, col) == CELL_ALIVE:
                        painter.fillRect(cell, self._cell_alive_color.color)
                    else:
                        painter.fillRect(cell, self._cell_dead_color.color)

            # Draw borders
            thickness_half = self._border_thickness // 2
            for row in range(self._engine.rows + 1):
                cell_point = self._cell_top_left_point(row + 1, 0)
                line_rect = QRectF(0,
                                   cell_point.y() - thickness_half,
                                   self.width(),
                                   self._border_thickness)
                painter.fillRect(line_rect, self._border_color.color)
            for col in range(self._engine.cols + 1):
                cell_point = self._cell_top_left_point(0, col + 1)
                line_rect = QRectF(cell_point.x() - thickness_half,
                                   0,
                                   self._border_thickness,
                                   self.height())
                painter.fillRect(line_rect, self._border_color.color)

            # Row top
            line_rect = QRectF(0, 0, self.width(), thickness_half)
            painter.fillRect(line_rect, self._border_color.color)
            # Row bottom
            line_rect = QRectF(0, self.height() - thickness_half, self.width(), thickness_half)
            painter.fillRect(line_rect, self._border_color.color)
            # Col left
            line_rect = QRectF(0, 0, thickness_half, self.height())
            painter.fillRect(line_rect, self._border_color.color)
            # Col right
            line_rect = QRectF(self.width() - thickness_half, 0, thickness_half, self.height())
            painter.fillRect(line_rect, self._border_color.color)

        end_time = time.perf_counter()
        self._sum_paint_performance += (end_time - start_time)
        self._paint_count += 1
        self.paint_event_signal.emit()

    # Handlers for the inner signals
    @Slot()
    def _handle_board_changed(self):
        """Handles 'board_changed' signal of the engine"""
        if self._active_cell is not None:
            if self._active_cell[0] >= self._engine.rows:
                self._active_cell = (self._engine.rows - 1, self._active_cell[1])
            if self._active_cell[1] >= self._engine.cols:
                self._active_cell = (self._active_cell[0], self._engine.cols - 1)

        self.update()

    # Miscellaneous stuff
    def update(self):
        # Small optimization
        cur_time = time.perf_counter()
        if cur_time - self._last_update_time < 0.05:
            return
        self._last_update_time = cur_time
        super().update()

    def minimumSizeHint(self):
        return QSize(*MINIMUM_SIZE)

    def sizeHint(self):
        return QSize(self._cell_width() * self._engine.rows,
                     self._cell_height() * self._engine.cols)

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
        cur_size = self.size()
        resize_needed = False
        if self._perfect_size_constraint:
            cur_size = self._get_perfect_size(cur_size)
            resize_needed = True
        if self._square_size_constraint:
            cur_size = self._get_square_size(cur_size)
            resize_needed = True
        if resize_needed:
            self.resize(cur_size)
        super().resizeEvent(event)

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

    # Abstract methods implementation
    _SAVABLE_PROPERTIES = \
        ["turn_duration",
         "border_thickness",
         "border_color",
         "cell_dead_color",
         "cell_alive_color"]

    @classmethod
    def savable_properties_names(cls) -> List[str]:
        return cls._SAVABLE_PROPERTIES

    _SIGNAL_SUFFIX = "_changed"

    def get_property_changed_signal(self, name: str) -> Signal:
        name += self._SIGNAL_SUFFIX
        if isinstance(signal := getattr(self, name, None), Signal):
            return signal
        raise ValueError
