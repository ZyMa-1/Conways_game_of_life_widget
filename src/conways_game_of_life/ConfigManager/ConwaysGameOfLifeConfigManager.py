"""
Config manager for saving properties to json file and loading them from the widget.

Author: ZyMa-1
"""

import json
import pathlib

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

from src.backend.PathManager import PathManager
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from .FileDialogFactory import FileDialogFactory
from .QtPropertyJsonConverter import QtPropertyJsonConverter


class ConwaysGameOfLifeConfigManager(QObject):
    """Class for saving and loading widget properties."""

    def __init__(self, conwaysGameOfLifeWidget: ConwaysGameOfLife, parent=None):
        super().__init__(parent)

        self.conways_game_of_life_widget = conwaysGameOfLifeWidget
        self.PROJECT_ROOT = PathManager.PROJECT_ROOT
        self.CONFIGS_DIR = PathManager.CONFIGS_DIR

        self._property_dict = {}

    def save_config(self, parent=None) -> None | str:
        """Saves widget properties to '.json' file. Returns filename if operation was completed, None otherwise."""
        file_dialog = FileDialogFactory.create_save_config_file_dialog(parent=parent,
                                                                       dir=str(self.CONFIGS_DIR))
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            self._save_properties()

            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            with open(file_path, 'w') as file:
                json.dump(self._property_dict, file, indent=4)

            return file_path.name

        return None

    def load_config(self, parent=None) -> None | str:
        """Loads widget properties from a '.json' file. Returns filename if operation was completed, None otherwise."""
        file_dialog = FileDialogFactory.create_load_config_file_dialog(parent=parent,
                                                                       dir=str(self.CONFIGS_DIR))
        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            with open(file_path, 'r') as file:
                self._property_dict = json.load(file)

            self._load_properties()

            return file_path.name

        return None

    def _save_properties(self):
        self._property_dict.clear()
        for property_name in self.conways_game_of_life_widget.savable_properties_name_list():
            value = getattr(self.conways_game_of_life_widget, property_name)
            value = QtPropertyJsonConverter.to_json_type(value)

            self._property_dict[property_name] = value

    def _load_properties(self):
        for property_name, value in self._property_dict.items():
            value = QtPropertyJsonConverter.to_property_type(value)
            setattr(self.conways_game_of_life_widget, property_name, value)
