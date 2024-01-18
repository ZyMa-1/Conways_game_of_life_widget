from types import MethodType
from typing import Dict

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from .QtPropertyWidgetConverter import convert_widget_value
from .SlotPropertyConnector import SlotPropertyConnector


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for linking game properties to the widgets representing them and vice versa.
    """

    def __init__(self, game_widget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.game_widget = game_widget
        self._slot_property_connector = SlotPropertyConnector(self)
        self._property_to_widget: Dict[str, QWidget] = {}  # {property_name: widget}
        self._property_to_widget_slot: Dict[str, MethodType] = {}  # {property_name: slot}

    def connect_widget_and_property(self, widget: QWidget, property_name: str, property_has_signal: bool = False):
        """
        Connecting widget to the property.
        If 'property_has_signal' is True
        connecting property changed signal to the widget also.
        """
        # Exception can occur in that, so catching it and raising another one is meh
        value = self.game_widget.get_property(property_name)
        signal = None
        if property_has_signal:
            signal = self.game_widget.get_property_changed_signal(property_name)
        slot = self._slot_property_connector.connect_property_to_widget(property_name=property_name,
                                                                        property_value=value,
                                                                        widget=widget,
                                                                        signal=signal)
        self._property_to_widget[property_name] = widget
        self._property_to_widget_slot[property_name] = slot

    def assign_widget_values_to_properties(self):
        for name, widget in self._property_to_widget.items():
            value = convert_widget_value(widget, name)
            self.game_widget.set_property(name, value)

    def assign_properties_values_to_widgets(self):
        for name, slot in self._property_to_widget_slot.items():
            value = self.game_widget.get_property(name)
            slot(value)
