from types import MappingProxyType, MethodType

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QColor


class _SlotFactory(QObject):
    """Class purpose of which is to create unique slots."""

    def __init__(self, widget, parent=None):
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

    SLOTS = MappingProxyType({
        "turn_number": _turn_number_int_slot,
        "is_game_running": _is_game_running_slot,
        "cols": _spin_box_int_slot,
        "rows": _spin_box_int_slot,
        "turn_duration": _spin_box_int_slot,
        "border_thickness": _spin_box_int_slot,
        "border_color": _label_color_slot,
        "cell_dead_color": _label_color_slot,
        "cell_alive_color": _label_color_slot
    })


class SlotPropertyConnector(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def connect_property_to_widget(self, *, property_name, property_value, signal, widget):
        slot = _SlotFactory(widget, parent=self.parent()).get_slot(property_name)
        slot(property_value)
        signal.connect(slot)
