from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel

from .abcs import IMyPropertyWidget, QAbcMeta


class LabelInt(QLabel, IMyPropertyWidget, metaclass=QAbcMeta):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def property_slot(self, value: int):
        self.setText(str(value))

    def to_property_value(self) -> int:
        return int(self.text())
