from types import MethodType
from typing import Any, Optional

from PySide6.QtCore import QObject, Slot, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget


class _SlotFactory(QObject):
    """Class to create unique slots"""

    def __init__(self, widget: QWidget, parent=None):
        super().__init__(parent)
        self.widget = widget

    def get_slot(self, property_name: str):
        method = self.SLOTS[property_name]
        bound_method = MethodType(method, self)
        return bound_method

    @Slot(QColor)
    def _label_color_slot(self, color: QColor):
        r, g, b = color.red(), color.green(), color.blue()
        self.widget.setStyleSheet(f"background-color: rgb({r},{g},{b});")

    @Slot(int)
    def _spin_box_int_slot(self, value: int):
        self.widget.setValue(value)

    @Slot(int)
    def _turn_number_int_slot(self, value: int):
        self.widget.setText(str(value))

    @Slot(bool)
    def _is_game_running_slot(self, value: bool):
        self.widget.setText(":)" if value else ":(")

    SLOTS = {
        "turn_number": _turn_number_int_slot,
        "is_game_running": _is_game_running_slot,
        "cols": _spin_box_int_slot,
        "rows": _spin_box_int_slot,
        "turn_duration": _spin_box_int_slot,
        "border_thickness": _spin_box_int_slot,
        "border_color": _label_color_slot,
        "cell_dead_color": _label_color_slot,
        "cell_alive_color": _label_color_slot
    }


class SlotPropertyConnector(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.slot_factories = []

    def connect_property_to_widget(self, property_name: str, property_value: Any,
                                   widget: QWidget, signal: Optional[Signal]) -> MethodType:
        slot_factory = _SlotFactory(widget, parent=self.parent())
        self.slot_factories.append(slot_factory)
        slot = slot_factory.get_slot(property_name)
        slot(property_value)
        if signal:
            signal.connect(slot)
        return slot
