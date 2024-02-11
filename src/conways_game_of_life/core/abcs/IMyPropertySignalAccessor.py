from abc import ABC, abstractmethod

from PySide6.QtCore import Signal


class IMyPropertySignalAccessor(ABC):
    """
    Interface for accessing notify signals of the Qt-Properties.
    """
    @abstractmethod
    def get_property_notify_signal(self, property_name: str) -> Signal:
        """
        Returns notify(changed) signal of the property.
        """
        pass
