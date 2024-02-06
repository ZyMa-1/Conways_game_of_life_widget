from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel

from src.conways_game_of_life.abcs import IMyPropertyWidget
from src.conways_game_of_life.abcs import QAbcMeta


class LabelInt(QLabel, IMyPropertyWidget, metaclass=QAbcMeta):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def property_slot(self, value: int):
        self.setText(str(value))

    def to_property_value(self) -> int:
        return int(self.text())
