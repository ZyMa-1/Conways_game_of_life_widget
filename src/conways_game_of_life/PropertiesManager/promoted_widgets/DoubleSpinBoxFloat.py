from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDoubleSpinBox

from .abcs import QAbcMeta, IMyPropertyWidget


class DoubleSpinBoxFloat(QDoubleSpinBox, IMyPropertyWidget, metaclass=QAbcMeta):
    """
    'Float Qt-Property' <-> 'QDoubleSpinBox'
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def property_slot(self, value: float):
        self.setValue(value)

    def to_property_value(self) -> float:
        return float(self.value())
