from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLabel

from .abcs import IMyPropertyWidget, QAbcMeta


class LabelGameRunning(QLabel, IMyPropertyWidget, metaclass=QAbcMeta):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(bool)
    def property_slot(self, value: bool):
        self.setText(":)" if value else ":(")

    def to_property_value(self) -> bool:
        return self.text() == ":)"
