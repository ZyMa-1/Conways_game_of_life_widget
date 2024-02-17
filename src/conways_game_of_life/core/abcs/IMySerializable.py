from abc import ABC, abstractmethod


class IMySerializable(ABC):
    """
    Interface for creating widgets, which properties can be serialized.
    """
    @abstractmethod
    def savable_properties_names(self) -> list[str]:
        """
        Returns list of savable properties associated specifically with the widget.
        """
        pass
