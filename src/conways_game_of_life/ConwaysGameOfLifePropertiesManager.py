"""
"Idk if this thing work" - Probably me.

Author: ZyMa-1
"""

from PySide6.QtCore import QObject, Property, Signal, Slot
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


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for changing widget value on 'some property' changed signal.
    ASSUMING PROPERTY CHANGED SIGNAL HAVE '{property_name}_{PROPERTY_CHANGED_SIGNAL_SUFFIX}' NAME!!!
    """
    PROPERTY_CHANGED_SIGNAL_SUFFIX = "changed"  # like turn_number -> turn_number_changed

    def __init__(self, conwaysGameOfLifeWidget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.conways_game_of_life_widget = conwaysGameOfLifeWidget

    # Only one way handlers (widget_property -> widget_value)

    def add_turn_number_handler(self, widget):
        if isinstance(widget, QLabel):
            self.conways_game_of_life_widget.turn_number_changed.connect(lambda num: widget.setText(str(num)))
            widget.setText(str(self.conways_game_of_life_widget.turn_number))
        else:
            raise TypeError("Handler for this type of widget is not supported")

    def add_is_game_running_handler(self, widget):
        if isinstance(widget, QLabel):
            self.conways_game_of_life_widget.is_game_running_changed.connect(
                lambda b: widget.setText(":)" if b else ":("))
            widget.setText(":)" if self.conways_game_of_life_widget.is_game_running else ":(")
        else:
            raise TypeError("Handler for this type of widget is not supported")

    # Idk if things below even work :P

    def add_handler(self, widget, *, property_name: str):
        property_obj = getattr(self.conways_game_of_life_widget, property_name, None)
        if property_obj is None:
            raise AttributeError("Property name is not valid")

        if not isinstance(property_obj, Property):
            raise AttributeError("Property is not a property")

        property_type = property_obj.fget.__annotations__['return']  # Uhhhhhh, gets TYPE ANNOTATION for return type
        if isinstance(property_type, QColor):
            if isinstance(widget, QLabel):
                self._add_label_bg_color_handler(widget, property_name)
            else:
                raise AttributeError("Property is not supported")
        elif isinstance(property_type, int):
            if isinstance(widget, QSpinBox):
                self._add_spin_box_int_handler(widget, property_name)
            else:
                raise AttributeError("Property is not supported")
        else:
            raise AttributeError("Property is not supported")

    def _add_label_bg_color_handler(self, widget: QLabel, property_name: str):
        property_changed_signal = getattr(self.conways_game_of_life_widget,
                                          property_name + "_" + self.PROPERTY_CHANGED_SIGNAL_SUFFIX, None)
        if property_changed_signal is None:
            raise AttributeError("Property changed signal does not exists")

        if not isinstance(property_changed_signal, Signal):
            raise AttributeError("Property signal is not a signal")

        slot = _SlotFactory.create_label_bg_color_handler_slot(widget)
        property_changed_signal.connect(slot)

    def _add_spin_box_int_handler(self, widget: QSpinBox, property_name: str):
        property_changed_signal = getattr(self.conways_game_of_life_widget,
                                          property_name + "_" + self.PROPERTY_CHANGED_SIGNAL_SUFFIX, None)
        if property_changed_signal is None:
            raise AttributeError("Property changed signal does not exists")

        if not isinstance(property_changed_signal, Signal):
            raise AttributeError("Property signal is not a signal")

        slot = _SlotFactory.create_spin_box_int_handler_slot(widget)
        property_changed_signal.connect(slot)
