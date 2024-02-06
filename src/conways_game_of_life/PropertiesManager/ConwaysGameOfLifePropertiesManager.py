from typing import Dict, Tuple, TypeVar, Any, Callable

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife  # type: ignore
from src.conways_game_of_life.ConwaysGameOfLifeEngine import ConwaysGameOfLifeEngine  # type: ignore
from src.conways_game_of_life.abcs import IMyPropertyWidget  # type: ignore

_objT = ConwaysGameOfLife | ConwaysGameOfLifeEngine
_widgetT = TypeVar('_widgetT', bound=QWidget | IMyPropertyWidget)


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for linking game properties to the widgets values representing them and vice versa.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._property_to_widget: Dict[Tuple[_objT, str], _widgetT] = {}  # {property_name: widget}
        self._property_to_widget_slot: Dict[Tuple[_objT, str], Callable[[Any], None]] = {}  # {property_name: slot}

    def connect_widget_and_obj_property(self, widget: _widgetT,
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
        widget.property_slot(value)
        self._property_to_widget_slot[(obj, property_name)] = widget.property_slot

        if property_has_signal:
            signal = obj.get_property_changed_signal(property_name)
            signal.connect(widget.property_slot)

        if not property_read_only:
            self._property_to_widget[(obj, property_name)] = widget

    def assign_widget_values_to_properties(self):
        """Assigns widget values to properties"""
        for (obj, name), widget in self._property_to_widget.items():
            widget: _widgetT = widget  # type hint
            value = widget.to_property_value()
            obj.setProperty(name, value)

    def assign_properties_values_to_widgets(self):
        """Assigns properties to widget values"""
        for (obj, name), slot in self._property_to_widget_slot.items():
            value = obj.property(name)
            slot(value)
