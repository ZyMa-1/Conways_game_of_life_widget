"""
Config manager for game widget (saving properties and loading them).

Author: ZyMa-1
"""

import json
import pathlib

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

from src.backend.PathManager import PathManager


class ConwaysGameOfLifeConfigManager(QObject):
    def __init__(self, conwaysGameOfLifeWidget, parent=None):
        super().__init__(parent)
        self.conways_game_of_life_widget = conwaysGameOfLifeWidget
        self.PROJECT_ROOT = PathManager.get_project_root()
        self.CONFIGS_DIR = self.PROJECT_ROOT / "configs"

        self._object_dict = {}

    def save_config(self, parent=None) -> None | str:
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
            self._object_dict[name] = getattr(self.conways_game_of_life_widget, name)
        # print(self._object_dict)

    def _load_properties(self):
        # print(self._object_dict)
        for name in self._object_dict:
            setattr(self.conways_game_of_life_widget, name, self._object_dict[name])
