from types import MethodType
from typing import Dict

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from .QtPropertyWidgetConverter import convert_widget_value
from .SlotPropertyConnector import SlotPropertyConnector


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for syncing changed singles of the properties to the widgets representing them.
    Let's agree that signal=f"{property_name}_{PROPERTY_CHANGED_SIGNAL_SUFFIX}"
    """
    PROPERTY_CHANGED_SIGNAL_SUFFIX = "changed"  # for example: turn_number -> turn_number_changed

    def __init__(self, conways_game_of_life_widget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.conways_game_of_life_widget = conways_game_of_life_widget
        self._parent = parent
        self._slot_property_connector = SlotPropertyConnector(parent=self)
        self._property_to_widget: Dict[str, QWidget] = {}  # {property_name: widget}, for both mutual connection
        self._property_to_widget_slot: Dict[str, MethodType] = {}  # {property_name: slot}

    def link_widget_and_property(self, widget: QWidget, property_name: str, is_both_way: bool = True):
        if property_name not in self.conways_game_of_life_widget.all_properties_name_list():
            raise ValueError("Property name is not valid")

        property_changed_signal = self._get_property_changed_signal(property_name)
        value = getattr(self.conways_game_of_life_widget, property_name)
        slot = self._slot_property_connector.connect_property_to_widget(property_name=property_name,
                                                                        property_value=value,
                                                                        signal=property_changed_signal,
                                                                        widget=widget)
        self._property_to_widget_slot[property_name] = slot
        if is_both_way:
            self._property_to_widget[property_name] = widget

    def assign_widget_values_to_properties(self):
        for property_name, widget in self._property_to_widget.items():
            value = convert_widget_value(widget, property_name)
            setattr(self.conways_game_of_life_widget, property_name, value)

    def assign_properties_values_to_widgets(self):
        for property_name, widget in self._property_to_widget.items():
            value = getattr(self.conways_game_of_life_widget, property_name)
            self._property_to_widget_slot[property_name](value)

    def _get_property_changed_signal(self, property_name: str) -> Signal:
        property_changed_signal = getattr(self.conways_game_of_life_widget,
                                          property_name + "_" + self.PROPERTY_CHANGED_SIGNAL_SUFFIX, None)
        if property_changed_signal is None:
            raise AttributeError("Property changed signal does not exists")

        if not isinstance(property_changed_signal, Signal):
            raise AttributeError(
                f"Property signal is not a signal. Retrieved object type is {type(property_changed_signal)}")

        return property_changed_signal
