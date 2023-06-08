"""
Author: ZyMa-1
"""

from PySide6.QtWidgets import QMessageBox


class MessageBoxFactory:
    @staticmethod
    def create_file_save_info_box(*, parent, filename: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle("Message")
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(f"File save successfully at 'exports/{filename}'")
        return box

    @staticmethod
    def create_config_save_info_box(*, parent, filename: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle("Message")
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(f"Config saved at 'configs/{filename}'")
        return box

    @staticmethod
    def create_config_load_info_box(*, parent, filename: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle("Message")
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(f"Config loaded from 'configs/{filename}'")
        return box
