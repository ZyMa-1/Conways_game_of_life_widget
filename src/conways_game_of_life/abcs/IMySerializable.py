from abc import ABC, abstractmethod
from typing import List


class IMySerializable(ABC):
    @abstractmethod
    def savable_properties_names(self) -> List[str]:
        """Returns list of savable properties associated specifically with the widget"""
        pass
