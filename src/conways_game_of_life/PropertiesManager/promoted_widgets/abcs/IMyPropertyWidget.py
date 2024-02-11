from abc import ABC, abstractmethod


class IMyPropertyWidget(ABC):
    """
    Interface for creating widgets connected to Qt properties.

    This interface defines methods for handling property signals and
    converting widget states to property values.
    """

    @abstractmethod
    def property_slot(self, value):
        """Slot for the property's notify signal"""
        pass

    @abstractmethod
    def to_property_value(self):
        """Converts current widget state to property value"""
        pass
