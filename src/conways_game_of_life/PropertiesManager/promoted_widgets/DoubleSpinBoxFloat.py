from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDoubleSpinBox

from conways_game_of_life.PropertiesManager.promoted_widgets.abcs import IMyPropertyWidget
from conways_game_of_life.core.abcs import QAbcMeta


class DoubleSpinBoxFloat(QDoubleSpinBox, IMyPropertyWidget, metaclass=QAbcMeta):
    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int)
    def property_slot(self, value: float):
        self.setValue(value)

    def to_property_value(self) -> float:
        return float(self.value())
