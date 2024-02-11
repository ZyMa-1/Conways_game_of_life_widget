from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSpinBox

from .abcs import IMyPropertyWidget, QAbcMeta


class SpinBoxInt(QSpinBox, IMyPropertyWidget, metaclass=QAbcMeta):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def property_slot(self, value: int):
        self.setValue(value)

    def to_property_value(self) -> int:
        return self.value()
