from abc import ABC, abstractmethod

from PySide6.QtCore import Signal


class IMyPropertySignalAccessor(ABC):
    @abstractmethod
    def get_property_notify_signal(self, name: str) -> Signal:
        """Returns notify(changed) signal of a property"""
        pass
