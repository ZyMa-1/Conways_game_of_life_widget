from functools import wraps
from typing import Tuple, TypedDict, List

from PySide6.QtGui import QColor


def property_setter_error_handle(func):
    @wraps(func)
    def wrapper(self, value):
        try:
            func(self, value)  # Call the original setter function
        except (ValueError, TypeError, AttributeError) as e:
            error_message = str(e)
            property_name = func.__name__
            self.property_setter_error_signal.emit(property_name, error_message)

    return wrapper


class ColorProperty:
    def __init__(self, color: QColor):
        self._color = color

    @property
    def rgb(self):
        return self._color.red(), self._color.green(), self._color.blue()

    @property
    def color(self):
        return self._color

    @staticmethod
    def _check_rgb_boundaries(rgb: Tuple[int, int, int]):
        return 0 <= rgb[0] <= 255 and 0 <= rgb[1] <= 255 and 0 <= rgb[2] <= 255

    def set_color(self, value: QColor | Tuple[int, int, int]):
        if isinstance(value, QColor):
            self._color = value
        elif isinstance(value, tuple) and len(value) == 3 and self._check_rgb_boundaries(value):
            self._color = QColor(*value)
        else:
            raise ValueError("Invalid color value")


class PatternSchema(TypedDict):
    rows: int
    cols: int
    state: List[List[str]]
    pattern_name: str
