import pathlib
from typing import Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget, QFileDialog, QMainWindow, QMessageBox

from backend import PathManager


class MainWindowUtils(QObject):
    """
    Helper class to create dialogs and message boxes.
    """

    def __init__(self, main_window: QMainWindow):
        super().__init__(main_window)
        self.main_window = main_window

        # Create some instances in advance
        self.info_msg_box = QMessageBox(main_window)
        self.info_msg_box.setWindowTitle("Message")
        self.info_msg_box.setIcon(QMessageBox.Icon.Information)

        self.warning_msg_box = QMessageBox(main_window)
        self.warning_msg_box.setWindowTitle("Warning")
        self.warning_msg_box.setIcon(QMessageBox.Icon.Warning)

    def save_widget_to_png(self, widget: QWidget) -> Optional[str]:
        file_dialog = QFileDialog(self.main_window)
        file_dialog.setDefaultSuffix('png')
        file_dialog.setDirectory(str(PathManager.EXPORTS_DIR))
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

    def create_warning_msg_box(self, text: str) -> QMessageBox:
        self.warning_msg_box.setText(text)
        return self.warning_msg_box

    def create_info_msg_box(self, text: str) -> QMessageBox:
        self.info_msg_box.setText(text)
        return self.info_msg_box
