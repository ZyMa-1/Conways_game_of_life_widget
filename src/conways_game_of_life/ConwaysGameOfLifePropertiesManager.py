"""
Properties manager. Made to ease communication between widgets and properties.

Author: ZyMa-1
"""
from types import MappingProxyType

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QSpinBox

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife


class _SlotFactory(QObject):
    @staticmethod
    def create_label_bg_color_handler_slot(label: QLabel):
        @Slot(QColor)
        def slot(color: QColor):
            r, g, b = color.red(), color.green(), color.blue()
            label.setStyleSheet(f"background-color: rgb({r},{g},{b});")

        return slot

    @staticmethod
    def create_spin_box_int_handler_slot(spin_box: QSpinBox):
        @Slot(int)
        def slot(value: int):
            spin_box.setValue(value)

        return slot

    @staticmethod
    def create_turn_number_handler_slot(label: QLabel):
        @Slot(int)
        def slot(value: int):
            label.setText(str(value))

        return slot

    @staticmethod
    def create_is_game_running_handler_slot(label: QLabel):
        @Slot(bool)
        def slot(value: bool):
            label.setText(":)" if value else ":(")

        return slot

    @classmethod
    def create_slot_by_property_name(cls, *, property_name: str, widget):
        if property_name not in cls.PROPERTY_NAME_TO_SLOT:
            return None

        slot_factory_func = cls.PROPERTY_NAME_TO_SLOT[property_name]
        return slot_factory_func(widget)

    PROPERTY_NAME_TO_SLOT = MappingProxyType({
        "turn_number": create_turn_number_handler_slot,
        "is_game_running": create_is_game_running_handler_slot,
        "cols": create_spin_box_int_handler_slot,
        "rows": create_spin_box_int_handler_slot,
        "turn_duration": create_spin_box_int_handler_slot,
        "border_thickness": create_spin_box_int_handler_slot,
        "border_color": create_label_bg_color_handler_slot,
        "cell_dead_color": create_label_bg_color_handler_slot,
        "cell_alive_color": create_label_bg_color_handler_slot
    })


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for changing widget value on 'some property' changed signal.
    ASSUMING PROPERTY CHANGED SIGNAL HAVE '{property_name}_{PROPERTY_CHANGED_SIGNAL_SUFFIX}' NAME!!!
    """
    PROPERTY_CHANGED_SIGNAL_SUFFIX = "changed"  # for example: turn_number -> turn_number_changed
    notify_all = Signal()

    def __init__(self, conwaysGameOfLifeWidget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.conways_game_of_life_widget = conwaysGameOfLifeWidget
        self._slot_factory = _SlotFactory(parent=self)

        self._slot_dict = {}

    def sync(self):
        """Sync widget values with properties values."""
        self.notify_all.emit()

    def add_handler_by_property_name(self, *, widget, property_name: str):
        if property_name in self._slot_dict:
            return

        property_changed_signal = self._get_property_changed_signal(property_name)
        value = self._get_property_value(property_name)
        slot = self._slot_factory.create_slot_by_property_name(property_name=property_name,
                                                               widget=widget)

        # Add slot to dict and to notify_all signal
        self._slot_dict[property_name] = slot
        self.notify_all.connect(lambda: slot(value))
        slot(value)
        property_changed_signal.connect(slot)

    def _get_property_changed_signal(self, property_name: str) -> Signal:
        property_changed_signal = getattr(self.conways_game_of_life_widget,
                                          property_name + "_" + self.PROPERTY_CHANGED_SIGNAL_SUFFIX, None)
        if property_changed_signal is None:
            raise AttributeError("Property changed signal does not exists")

        if not isinstance(property_changed_signal, Signal):
            raise AttributeError(f"Property signal is not a signal. Property signal is {type(property_changed_signal)}")

        return property_changed_signal

    def _get_property_value(self, property_name: str):
        return getattr(self.conways_game_of_life_widget, property_name, None)
