from types import MethodType
from typing import Dict, Tuple

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from src.conways_game_of_life.ConwaysGameOfLifeEngine import ConwaysGameOfLifeEngine
from .QtPropertyWidgetConverter import convert_widget_value
from .SlotPropertyConnector import SlotPropertyConnector

_objT = ConwaysGameOfLife | ConwaysGameOfLifeEngine


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for linking game properties to the widgets values representing them and vice versa.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._slot_property_connector = SlotPropertyConnector(self)
        self._property_to_widget: Dict[Tuple[_objT, str], QWidget] = {}  # {property_name: widget}
        self._property_to_widget_slot: Dict[Tuple[_objT, str], MethodType] = {}  # {property_name: slot}

    def connect_widget_and_obj_property(self, widget: QWidget,
                                        obj: _objT,
                                        property_name: str,
                                        property_has_signal: bool = False,
                                        property_read_only: bool = False):
        """
        Connects widget to the object property and vice versa.
        By default, creates a way to convert:
        'widget value' -> 'object property'
        'object property' -> 'widget value'

        If 'property_has_signal' is True,
        connect property changed signal to the widget.

        If 'property_read_only' is True,
        disable widget to property connection.
        """
        value = obj.property(property_name)
        signal = None
        if property_has_signal:
            signal = obj.get_property_changed_signal(property_name)
        slot = self._slot_property_connector.connect_property_to_widget(property_name=property_name,
                                                                        property_value=value,
                                                                        widget=widget,
                                                                        signal=signal)
        self._property_to_widget_slot[(obj, property_name)] = slot
        if not property_read_only:
            self._property_to_widget[(obj, property_name)] = widget

    def assign_widget_values_to_properties(self):
        """Assigns widget values to properties"""
        for (obj, name), widget in self._property_to_widget.items():
            value = convert_widget_value(widget, name)
            obj.setProperty(name, value)

    def assign_properties_values_to_widgets(self):
        """Assigns properties to widget values"""
        for (obj, name), slot in self._property_to_widget_slot.items():
            value = obj.property(name)
            slot(value)
