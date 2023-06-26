"""
Properties manager. Made to ease communication between widgets and properties.

Author: ZyMa-1
"""
from PySide6.QtCore import QObject, Signal

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from .QtPropertyWidgetConverter import QtPropertyWidgetConverter
from .SlotPropertyConnector import SlotPropertyConnector


class ConwaysGameOfLifePropertiesManager(QObject):
    """
    Class for changing widget value on 'some property' changed signal and more.
    ASSUMING PROPERTY CHANGED SIGNAL HAVE '{property_name}_{PROPERTY_CHANGED_SIGNAL_SUFFIX}' NAME!!!
    """
    PROPERTY_CHANGED_SIGNAL_SUFFIX = "changed"  # for example: turn_number -> turn_number_changed

    def __init__(self, conwaysGameOfLifeWidget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.conways_game_of_life_widget = conwaysGameOfLifeWidget
        self._slot_property_connector = SlotPropertyConnector(parent=self)
        self._widget_value_converter = QtPropertyWidgetConverter()

        self._slots_exist = {}  # property_name: True
        self._widgets = {}  # property_name: widget

    def add_handler_by_property_name(self, *, widget, property_name: str, is_both_way: bool = True):
        if property_name in self._slots_exist or \
                property_name not in self.conways_game_of_life_widget.all_dynamic_properties_name_list():
            return

        property_changed_signal = self._get_property_changed_signal(property_name)
        value = getattr(self.conways_game_of_life_widget, property_name)
        self._slot_property_connector.connect_property_to_widget(property_name=property_name,
                                                                 property_value=value,
                                                                 signal=property_changed_signal,
                                                                 widget=widget)
        self._slots_exist[property_name] = True
        if is_both_way:
            self._widgets[property_name] = widget

    def assign_all_widget_values_to_properties(self):
        for property_name, widget in self._widgets.items():
            value = self._widget_value_converter.convert_widget_value(property_name=property_name,
                                                                      widget=widget)
            setattr(self.conways_game_of_life_widget, property_name, value)

    def _get_property_changed_signal(self, property_name: str) -> Signal:
        property_changed_signal = getattr(self.conways_game_of_life_widget,
                                          property_name + "_" + self.PROPERTY_CHANGED_SIGNAL_SUFFIX, None)
        if property_changed_signal is None:
            raise AttributeError("Property changed signal does not exists")

        if not isinstance(property_changed_signal, Signal):
            raise AttributeError(f"Property signal is not a signal. Property signal is {type(property_changed_signal)}")

        return property_changed_signal
