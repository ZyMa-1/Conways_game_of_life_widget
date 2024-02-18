import json
import pathlib
from json import JSONDecodeError
from typing import Optional, Any, Iterable

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog, QWidget

from backend import PathManager
from conways_game_of_life.core.dynamic_types import gameWithPropertiesT
from .json_serialization import ConfigDecoder, ConfigEncoder

_keyT = str
_valT = dict[str, Any]


class GameConfigManager(QObject):
    """
    Class for saving and loading game properties using JSON format.
    """

    def __init__(self, game_objects: Iterable[gameWithPropertiesT], parent_widget: Optional[QWidget] = None):
        super().__init__(parent_widget)

        self._game_objects = game_objects
        self._parent_widget = parent_widget
        # class_name: {properties dict}
        self._property_dict: dict[_keyT, _valT] = {}

    def save_config(self) -> Optional[str]:
        """
        Saves game properties to JSON file.
        Returns filename if operation was completed, None otherwise.
        """
        file_dialog = QFileDialog(self._parent_widget)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setDirectory(str(PathManager.CONFIGS_DIR))
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Save Config")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self._property_dict.clear()
            for game_object in self._game_objects:
                self._save_obj_properties(game_object.__class__.__name__, game_object)

            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            with open(file_path, 'w') as file:
                json.dump(self._property_dict, file, cls=ConfigEncoder, indent=4)

            return file_path.name

        return None

    def load_config(self) -> Optional[str]:
        """
        Loads game properties from JSON file.
        Returns filename if operation was completed, None otherwise.
        """
        file_dialog = QFileDialog(self._parent_widget)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setDirectory(str(PathManager.CONFIGS_DIR))
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Load Config")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            try:
                with open(file_path, 'r') as file:
                    self._property_dict = json.load(file, cls=ConfigDecoder)
            except JSONDecodeError:
                return None

            for game_object in self._game_objects:
                properties_dict = self._property_dict.get(game_object.__class__.__name__)
                if properties_dict:
                    self._load_obj_properties(game_object, properties_dict)

            return file_path.name

        return None

    def _save_obj_properties(self, key: _keyT, obj: gameWithPropertiesT):
        self._property_dict[key] = {}
        for name in obj.savable_properties_names():
            value = obj.property(name)
            self._property_dict[key][name] = value

    @staticmethod
    def _load_obj_properties(obj: gameWithPropertiesT, properties: _valT):
        for name, value in properties.items():
            obj.setProperty(name, value)
