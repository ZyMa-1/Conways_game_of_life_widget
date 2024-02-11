from typing import Any, Callable

from PySide6.QtCore import QObject

from .promoted_widgets.types import propertyWidgetT
from conways_game_of_life.core.dynamic_types import gameWithPropertiesT

_keyT = tuple[gameWithPropertiesT, str]  # obj, property_name


class GamePropertiesManager(QObject):
    """
    Class for linking game properties to the widgets values representing them and vice versa.

    Provides a way to assign all widget values to properties at once.
    Provides a way to assign all properties to widget values at once.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._property_to_widget: dict[_keyT, propertyWidgetT] = {}
        self._property_to_widget_slot: dict[_keyT, Callable[[Any], None]] = {}

    def connect_widget_and_obj_property(self, widget: propertyWidgetT,
                                        obj: gameWithPropertiesT,
                                        property_name: str,
                                        property_has_signal: bool = False,
                                        property_read_only: bool = False):
        """
        Connects widget to the object property and vice versa.
        By default, creates a way to convert:
        'widget value' -> 'property'
        'property' -> 'widget value'

        If 'property_has_signal' is True,
        connects property changed signal to the widget.

        If 'property_read_only' is True,
        disables widget to property connection.
        """
        value = obj.property(property_name)
        widget.property_slot(value)
        self._property_to_widget_slot[(obj, property_name)] = widget.property_slot

        if property_has_signal:
            signal = obj.get_property_notify_signal(property_name)
            signal.connect(widget.property_slot)

        if not property_read_only:
            self._property_to_widget[(obj, property_name)] = widget

    def assign_widget_values_to_properties(self):
        """
        Assigns widget values to properties.
        """
        for (obj, name), widget in self._property_to_widget.items():
            value = widget.to_property_value()
            obj.setProperty(name, value)

    def assign_properties_values_to_widgets(self):
        """
        Assigns properties to widget values.
        """
        for (obj, name), slot in self._property_to_widget_slot.items():
            value = obj.property(name)
            slot(value)
