from abc import ABC, abstractmethod

from PySide6.QtCore import Signal


class IMyPropertySignalAccessor(ABC):
    @abstractmethod
    def get_property_changed_signal(self, name: str) -> Signal:
        """Returns property changed signal"""
        pass
