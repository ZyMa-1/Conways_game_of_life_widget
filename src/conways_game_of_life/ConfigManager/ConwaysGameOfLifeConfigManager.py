import json
import pathlib
from json import JSONDecodeError
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

from src.backend.PathManager import PathManager
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from .QtPropertyJsonConverter import to_json_type, to_property_type


class ConwaysGameOfLifeConfigManager(QObject):
    """Class for saving and loading widget properties."""

    def __init__(self, conways_game_of_life_widget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.conways_game_of_life_widget = conways_game_of_life_widget
        self._parent = parent
        self._property_dict = {}

    def save_config(self) -> Optional[str]:
        """
        Saves widget properties to '.json' file.
        Returns filename if operation was completed, None otherwise.
        """
        file_dialog = QFileDialog(self._parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setDirectory(str(PathManager.CONFIGS_DIR))
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Save Config")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self._save_properties()
            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            with open(file_path, 'w') as file:
                json.dump(self._property_dict, file, indent=4)

            return file_path.name

    def load_config(self) -> Optional[str]:
        """
        Loads widget properties from '.json' file.
        Returns filename if operation was completed, None otherwise.
        """
        file_dialog = QFileDialog(self._parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setDirectory(str(PathManager.CONFIGS_DIR))
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Load Config")
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            try:
                with open(file_path, 'r') as file:
                    self._property_dict = json.load(file)
            except JSONDecodeError:
                return None

            self._load_properties()
            return file_path.name

    def _save_properties(self):
        self._property_dict.clear()
        for property_name in self.conways_game_of_life_widget.savable_properties_name_list():
            value = getattr(self.conways_game_of_life_widget, property_name)
            value = to_json_type(value)
            self._property_dict[property_name] = value

    def _load_properties(self):
        for property_name, value in self._property_dict.items():
            value = to_property_type(value)
            setattr(self.conways_game_of_life_widget, property_name, value)
