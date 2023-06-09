"""
Config manager for game widget (saving properties and loading them).

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
        self.PROJECT_ROOT = PathManager.get_project_root()
        self.CONFIGS_DIR = self.PROJECT_ROOT / "configs"

        self._object_dict = {}

    def save_config(self, parent=None) -> None | str:
        """Saves widget properties to '.json' file. Returns filename is operation was completed, None otherwise."""
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
                json.dump(self._object_dict, file, indent=4)

            return file_path.name

        return None

    def load_config(self, parent=None) -> None | str:
        """Loads widget properties from a '.json' file. Returns filename is operation was completed, None otherwise."""
        file_dialog = QFileDialog(parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setDirectory(str(self.CONFIGS_DIR))
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Load Config")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            with open(file_path, 'r') as file:
                self._object_dict = json.load(file)

            self._load_properties()

            return file_path.name

        return None

    def _save_properties(self):
        self._object_dict.clear()
        for name in self.conways_game_of_life_widget.properties_name_list():
            property_obj = getattr(self.conways_game_of_life_widget, name)
            if isinstance(property_obj, QColor):
                property_obj = (property_obj.red(), property_obj.green(), property_obj.blue())

            self._object_dict[name] = property_obj
        # print(self._object_dict)

    def _load_properties(self):
        # print(self._object_dict)
        for name in self._object_dict:
            property_obj = self._object_dict[name]
            if isinstance(property_obj, QColor):
                property_obj = QColor(property_obj[0], property_obj[1], property_obj[2])

            setattr(self.conways_game_of_life_widget, name, property_obj)
