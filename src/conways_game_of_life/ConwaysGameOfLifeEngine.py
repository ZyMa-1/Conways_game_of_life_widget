from typing import List

from PySide6.QtCore import Signal, Property, QObject

from .utils import property_setter_error_handle

DEFAULT_COLS = 10  # px (assigned to attribute)
DEFAULT_ROWS = 10  # px (assigned to attribute)
CELL_ALIVE = '*'  # (used)
CELL_DEAD = '.'  # (used)

StateMatrixT = List[List[str]]


def _default_state_matrix(rows: int, cols: int) -> StateMatrixT:
    return [[CELL_DEAD for _ in range(cols)] for _ in range(rows)]


class ConwaysGameOfLifeEngine(QObject):
    """
    Engine class that represents the Conway's Game Of Life 2D board.
    Provides a viable way to interact with the game, encapsulating the logic.
    """

    # Signals:
    # Emits when state of the board or other properties are changed via property setters ONLY
    # Handling board changes is up to the widget class to prevent frequent updates and redraws
    board_changed = Signal()
    # Back to back
    turn_made = Signal()
    # Emits when invalid value passed to property setter
    property_setter_error_signal = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create engine parameters
        self._turn_number = 0
        self._cols = DEFAULT_COLS
        self._rows = DEFAULT_ROWS
        # List[List[str]]
        self._state: StateMatrixT = _default_state_matrix(self._rows, self._cols)

    # Properties
    def get_turn_number(self):
        return self._turn_number

    def get_cols(self):
        return self._cols

    @property_setter_error_handle
    def set_cols(self, value: int):
        if value <= 0:
            raise ValueError("Columns value must be positive")
        self._cols = value
        self._adjust_state()
        self.board_changed.emit()

    def get_rows(self):
        return self._rows

    @property_setter_error_handle
    def set_rows(self, value: int):
        if value <= 0:
            raise ValueError("Rows value must be positive")
        self._rows = value
        self._adjust_state()
        self.board_changed.emit()

    def get_state(self):
        return self._state

    @property_setter_error_handle
    def set_state(self, value: StateMatrixT):
        if not isinstance(value, list) or len(value) != self._rows:
            raise ValueError("State value is not correct")
        for row in range(self._rows):
            if not isinstance(value[row], list) or len(value[row]) != self._cols:
                raise ValueError("State value is not correct")
            for col in range(self._cols):
                if len(value[row][col]) != 1 or (value[row][col] != CELL_DEAD and value[row][col] != CELL_ALIVE):
                    raise ValueError("State value is not correct")
        self._state = value
        self.board_changed.emit()

    # API functionality to interact with the game
    def reset_to_defaults(self):
        self._turn_number = 0
        self._cols = DEFAULT_COLS
        self._rows = DEFAULT_ROWS
        self._state = _default_state_matrix(self._rows, self._cols)
        self.turn_number_changed.emit(self._turn_number)

    def clear_state(self):
        self._state = _default_state_matrix(self._rows, self._cols)

    def insert_state_array_at(self, row: int, col: int, state_array: StateMatrixT):
        max_possible_rows = self._rows - row
        max_possible_cols = self._cols - col
        for i in range(min(max_possible_rows, len(state_array))):
            for j in range(min(max_possible_cols, len(state_array[i]))):
                self._state[i + row][j + col] = state_array[i][j]

    # API + Inner logic (mixed)
    def change_cell_state_at(self, row: int, col: int, new_cell_state: str):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            return
        self._state[row][col] = new_cell_state

    def change_cell_state_to_opposite(self, row: int, col: int):
        if self._state[row][col] == CELL_ALIVE:
            self.change_cell_state_at(row, col, CELL_DEAD)
        elif self._state[row][col] == CELL_DEAD:
            self.change_cell_state_at(row, col, CELL_ALIVE)

    # Inner logic
    def _adjust_state(self):
        """Adjusts state when number of rows or cols changes"""
        rows = len(self._state)
        cols = len(self._state[0])
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

    def _get_alive_neighbor_count(self, row: int, col: int):
        count = 0
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (i != row or j != col) and 0 <= i < self._rows and 0 <= j < self._cols:
                    if self._state[i][j] == CELL_ALIVE:
                        count += 1
        return count

    # Make turn
    def make_turn(self):
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
        self._turn_number += 1
        self.turn_number_changed.emit(self._turn_number)
        self.turn_made.emit()

    # Properties signals
    turn_number_changed = Signal(int)

    # Pyqt properties (notify is not 'automatic'):
    state = Property(list, get_state, set_state)  # Does not work in Qt-Designer
    cols = Property(int, get_cols, set_cols)
    rows = Property(int, get_rows, set_rows)
    # read_only
    turn_number = Property(int, get_turn_number, notify=turn_number_changed)
