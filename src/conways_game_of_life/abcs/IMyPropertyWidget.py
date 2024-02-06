from abc import ABC, abstractmethod


class IMyPropertyWidget(ABC):

    @abstractmethod
    def property_slot(self, value):
        """Slot for the property's notify signal"""
        pass

    @abstractmethod
    def to_property_value(self):
        """Returns value passed to property's slot last time"""
        pass
