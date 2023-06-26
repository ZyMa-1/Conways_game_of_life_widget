from types import MappingProxyType

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QSpinBox


class SlotPropertyConnector(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.signal_slot_dict = {}

    @staticmethod
    def _border_color_slot(label: QLabel):
        @Slot(QColor)
        def slot(color: QColor):
            r, g, b = color.red(), color.green(), color.blue()
            label.setStyleSheet(f"background-color: rgb({r},{g},{b});")

        return slot

    @staticmethod
    def _cell_dead_color_slot(label: QLabel):
        @Slot(QColor)
        def slot(color: QColor):
            r, g, b = color.red(), color.green(), color.blue()
            label.setStyleSheet(f"background-color: rgb({r},{g},{b});")

        return slot

    @staticmethod
    def _cell_alive_color_slot(label: QLabel):
        @Slot(QColor)
        def slot(color: QColor):
            r, g, b = color.red(), color.green(), color.blue()
            label.setStyleSheet(f"background-color: rgb({r},{g},{b});")

        return slot

    @staticmethod
    def _rows_slot(spin_box: QSpinBox):
        @Slot(int)
        def slot(value: int):
            spin_box.setValue(value)

        return slot

    @staticmethod
    def _cols_slot(spin_box: QSpinBox):
        @Slot(int)
        def slot(value: int):
            spin_box.setValue(value)

        return slot

    @staticmethod
    def _border_thickness_slot(spin_box: QSpinBox):
        @Slot(int)
        def slot(value: int):
            spin_box.setValue(value)

        return slot

    @staticmethod
    def _turn_duration_slot(spin_box: QSpinBox):
        @Slot(int)
        def slot(value: int):
            spin_box.setValue(value)

        return slot

    @staticmethod
    def _turn_number_slot(label: QLabel):
        @Slot(int)
        def slot(value: int):
            label.setText(str(value))

        return slot

    @staticmethod
    def _is_game_running_slot(label: QLabel):
        @Slot(bool)
        def slot(value: bool):
            label.setText(":)" if value else ":(")

        return slot

    @classmethod
    def connect_property_to_widget(cls, *, property_name, property_value, signal, widget):
        if property_name not in cls.SLOTS:
            return

        slot = cls.SLOTS[property_name](widget)
        slot(property_value)
        signal.connect(slot)

    SLOTS = MappingProxyType({
        "turn_number": _turn_number_slot,
        "is_game_running": _is_game_running_slot,
        "cols": _cols_slot,
        "rows": _rows_slot,
        "turn_duration": _turn_duration_slot,
        "border_thickness": _border_thickness_slot,
        "border_color": _border_color_slot,
        "cell_dead_color": _cell_dead_color_slot,
        "cell_alive_color": _cell_alive_color_slot
    })
