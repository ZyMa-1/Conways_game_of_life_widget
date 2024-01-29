import time
from typing import List

import numpy as np
from PySide6.QtCore import Signal, Property, QObject

from .utils import property_setter_error_handle

DEFAULT_COLS = 10  # px (assigned to attribute)
DEFAULT_ROWS = 10  # px (assigned to attribute)
CELL_ALIVE = '*'  # (used)
CELL_DEAD = '.'  # (used)

StateT = np.ndarray
StatePropertyT = List[List[str]]


def _default_state_array(rows: int, cols: int) -> StateT:
    return np.full((rows, cols), CELL_DEAD)


class ConwaysGameOfLifeEngine(QObject):
    """
    Engine class that represents the Conway's Game Of Life 2D board.
    Provides a viable way to interact with the game, encapsulating the logic.
    """

    # Signals:
    # Emits when state of the board or other properties are changed via property setters ONLY
    # Handling board changes is up to the widget class to prevent frequent updates and redraws
    board_changed = Signal()
    turn_made = Signal()
    # Emits when invalid value passed to property setter
    property_setter_error_signal = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create engine parameters
        self._turn_number = 0
        self._cols = DEFAULT_COLS
        self._rows = DEFAULT_ROWS
        self._state: StateT = _default_state_array(self._rows, self._cols)
        self._alive_cells = 0
        # Performance of the 'make_turn' in ms
        self._sum_turn_performance = 0

        # Connect signals to slots
        self.alive_cells_changed.connect(lambda val:
                                         self.dead_cells_changed.emit(self._rows * self._cols - val))

    # Properties
    def get_turn_number(self):
        return self._turn_number

    def get_alive_cells(self):
        return self._alive_cells

    def get_dead_cells(self):
        return self._rows * self._cols - self._alive_cells

    def get_avg_turn_performance(self):
        return self._sum_turn_performance / self._turn_number

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

    def get_state(self) -> StatePropertyT:
        return self._state.tolist()

    @property_setter_error_handle
    def set_state(self, value: StatePropertyT):
        if not isinstance(value, list) or len(value) != self._rows:
            raise ValueError("State value is not correct")
        for row in range(self._rows):
            if not isinstance(value[row], list) or len(value[row]) != self._cols:
                raise ValueError("State value is not correct")
            for col in range(self._cols):
                if len(value[row][col]) != 1 or (value[row][col] != CELL_DEAD and value[row][col] != CELL_ALIVE):
                    raise ValueError("State value is not correct")
        self._state = np.array(value)
        # Calculate alive_cells property from scratch
        self._alive_cells = np.sum(self._state == CELL_ALIVE)
        self.alive_cells_changed.emit(self._alive_cells)
        self.board_changed.emit()

    # API functionality to interact with the game
    def reset_to_defaults(self):
        self._turn_number = 0
        self._cols = DEFAULT_COLS
        self._rows = DEFAULT_ROWS
        self._state = _default_state_array(self._rows, self._cols)
        self._alive_cells = 0
        self._sum_turn_performance = 0
        self.alive_cells_changed.emit(self._alive_cells)
        self.turn_number_changed.emit(self._turn_number)

    def clear_state(self):
        self._state = _default_state_array(self._rows, self._cols)
        self._alive_cells = 0
        self.alive_cells_changed.emit(self._alive_cells)

    def insert_state_array_at(self, row: int, col: int, state_array: StatePropertyT):
        state_array = np.array(state_array)
        max_possible_rows = self._rows - row
        max_possible_cols = self._cols - col
        clipped_state_array = state_array[
                              :min(max_possible_rows, state_array.shape[0]),
                              :min(max_possible_cols, state_array.shape[1])]

        self._alive_cells -= np.sum(self._state[row:row + clipped_state_array.shape[0],
                                    col:col + clipped_state_array.shape[1]] == CELL_ALIVE)

        self._state[row:row + clipped_state_array.shape[0],
                    col:col + clipped_state_array.shape[1]] = clipped_state_array

        self._alive_cells += np.sum(clipped_state_array == CELL_ALIVE)
        self.alive_cells_changed.emit(self._alive_cells)

    # API + Inner logic (mixed)
    def change_cell_state_at(self, row: int, col: int, new_cell_state: str):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            return
        self._alive_cells -= self._state[row, col] == CELL_ALIVE
        self._state[row, col] = new_cell_state
        self._alive_cells += new_cell_state == CELL_ALIVE
        self.alive_cells_changed.emit(self._alive_cells)

    def change_cell_state_to_opposite(self, row: int, col: int):
        if self._state[row, col] == CELL_ALIVE:
            self.change_cell_state_at(row, col, CELL_DEAD)
        elif self._state[row, col] == CELL_DEAD:
            self.change_cell_state_at(row, col, CELL_ALIVE)

    # Inner logic
    def _adjust_state(self):
        """Adjusts state when number of rows or cols changes"""
        new_state = _default_state_array(self._rows, self._cols)
        new_state[:min(self._rows, self._state.shape[0]), :min(self._cols, self._state.shape[1])] \
            = self._state[:min(self._rows, self._state.shape[0]), :min(self._cols, self._state.shape[1])]

        self._alive_cells = np.sum(new_state == CELL_ALIVE)
        self._state = new_state
        self.alive_cells_changed.emit(self._alive_cells)

    # Make turn
    def make_turn(self):
        start_time = time.perf_counter()
        neighbor_counts = np.zeros_like(self._state, dtype=int)

        for i in range(self._rows):
            for j in range(self._cols):
                # Use max/min to ensure we don't go out of bounds
                neighbor_counts[i, j] = np.sum(
                    self._state[max(0, i - 1):min(i + 2, self._rows),
                                max(0, j - 1):min(j + 2, self._cols)] == CELL_ALIVE
                )
                neighbor_counts[i, j] -= self._state[i, j] == CELL_ALIVE

        # Duh.
        # Apply rules of Conway's Game Of Life.
        new_state = np.where((self._state == CELL_ALIVE) & ((neighbor_counts == 2) | (neighbor_counts == 3)) |
                             (self._state == CELL_DEAD) & (neighbor_counts == 3),
                             CELL_ALIVE, CELL_DEAD)

        self._alive_cells = np.sum(new_state == CELL_ALIVE)
        self._state = new_state
        self._turn_number += 1
        self.turn_number_changed.emit(self._turn_number)
        self.alive_cells_changed.emit(self._alive_cells)
        end_time = time.perf_counter()
        self._sum_turn_performance += (end_time - start_time)
        self.turn_made.emit()

    # Properties signals
    turn_number_changed = Signal(int)
    alive_cells_changed = Signal(int)
    dead_cells_changed = Signal(int)

    # Pyqt properties (notify is not 'automatic'):
    state = Property(list, get_state, set_state)  # Does not work in Qt-Designer
    cols = Property(int, get_cols, set_cols)
    rows = Property(int, get_rows, set_rows)
    # read_only
    turn_number = Property(int, get_turn_number, notify=turn_number_changed)
    alive_cells = Property(int, get_alive_cells, notify=alive_cells_changed)
    dead_cells = Property(int, get_dead_cells, notify=dead_cells_changed)
