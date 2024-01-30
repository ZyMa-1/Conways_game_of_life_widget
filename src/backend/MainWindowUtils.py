import pathlib
from types import MethodType
from typing import Optional

from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QFileDialog, QMainWindow, QMessageBox, QDockWidget

from src.backend.PathManager import PathManager


class _SlotFactory(QObject):
    """
    Class to create unique slot methods bounded to the class instance.
    """

    def __init__(self, action: QAction, dock_widget: QDockWidget, parent=None):
        super().__init__(parent)
        self.action = action
        self.dock_widget = dock_widget

    def get_slot(self, slot_name: str):
        method = self.SLOTS[slot_name]
        bound_method = MethodType(method, self)
        return bound_method

    @Slot(bool)
    def set_checked(self, is_visible: bool):
        self.action.setChecked(is_visible)

    @Slot()
    def set_visible(self):
        if self.action.isChecked():
            self.dock_widget.show()
        else:
            self.dock_widget.hide()

    SLOTS = {
        "set_checked": set_checked,
        "set_visible": set_visible
    }


class MainWindowUtils(QObject):
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

        self._slot_factories = []

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

    def create_warning_msg_box(self, text: str) -> QMessageBox:
        self.warning_msg_box.setText(text)
        return self.warning_msg_box

    def create_info_msg_box(self, text: str) -> QMessageBox:
        self.info_msg_box.setText(text)
        return self.info_msg_box

    def connect_action_and_dock_widget(self, action: QAction, dock_widget: QDockWidget):
        slot_factory = _SlotFactory(action, dock_widget, parent=dock_widget)
        self._slot_factories.append(slot_factory)
        dock_widget.visibilityChanged.connect(slot_factory.get_slot("set_checked"))
        action.triggered.connect(slot_factory.get_slot("set_visible"))
