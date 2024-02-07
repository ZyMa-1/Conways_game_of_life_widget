from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel

from src.conways_game_of_life.abcs import IMyPropertyWidget, QAbcMeta


class LabelColor(QLabel, IMyPropertyWidget, metaclass=QAbcMeta):
    bg_color_changed = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(QColor)
    def property_slot(self, value: QColor):
        r, g, b, a = value.getRgb()
        self.setStyleSheet(f"background-color: rgba({r},{g},{b},{a});")
        self.bg_color_changed.emit(value)

    def to_property_value(self) -> QColor:
        return self.palette().color(self.backgroundRole())
