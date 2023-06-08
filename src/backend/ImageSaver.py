"""
Author: ZyMa-1
"""

import pathlib

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QFileDialog

from .PathManager import PathManager


class ImageSaver(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.PROJECT_ROOT = PathManager.get_project_root()
        self.EXPORTS_DIR = self.PROJECT_ROOT / "exports"

    def save_widget_to_image(self, widget, *, file_type: str = "png", parent=None) -> None | str:
        if file_type == "png":
            return self.save_widget_to_png(widget, parent=parent)
        else:
            raise NotImplementedError

    def save_widget_to_png(self, widget, *, parent=None) -> None | str:
        file_dialog = QFileDialog(parent)
        file_dialog.setDefaultSuffix('png')
        file_dialog.setDirectory(str(self.EXPORTS_DIR))
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilters(["PNG Files (*.png)"])
        file_dialog.setWindowTitle("Save Widget")

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_path = pathlib.Path(file_dialog.selectedFiles()[0])
            pixmap = widget.grab()
            pixmap.save(str(file_path))
            return file_path.name

        return None
