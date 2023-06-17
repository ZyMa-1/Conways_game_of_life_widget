"""
Config manager for saving properties and loading them from the widget.

Author: ZyMa-1
"""

import json
import pathlib

from PySide6.QtCore import QObject
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QFileDialog

from src.backend.PathManager import PathManager
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife


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
        file_dialog = QFileDialog(parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setDirectory(str(self.CONFIGS_DIR))
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

        return None

    def load_config(self, parent=None) -> None | str:
        """Loads widget properties from a '.json' file. Returns filename if operation was completed, None otherwise."""
        file_dialog = QFileDialog(parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setDirectory(str(self.CONFIGS_DIR))
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Load Config")

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
            value = self.conways_game_of_life_widget.property(property_name)
            value = self._convert_value_to_json(value)

            self._property_dict[property_name] = value
        # print(self._object_dict)

    def _load_properties(self):
        # print(self._object_dict)
        for property_name in self._property_dict:
            value = self.conways_game_of_life_widget.property(property_name)
            value = self._convert_value_from_json(value)

            setattr(self.conways_game_of_life_widget, property_name, value)

    @staticmethod
    def _convert_value_from_json(value):
        if isinstance(value, QColor):
            value = QColor(value[0], value[1], value[2])

        return value

    @staticmethod
    def _convert_value_to_json(value):
        if isinstance(value, QColor):
            value = (value.red(), value.green(), value.blue())

        return value
