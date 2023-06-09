"""
Author: ZyMa-1
"""
from PySide6.QtCore import QCoreApplication, QObject
from PySide6.QtWidgets import QMessageBox


class MessageBoxFactory(QObject):
    @staticmethod
    def create_file_save_info_box(*, parent, filename: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle(QCoreApplication.translate("MessageBoxFactory", "Message"))
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(QCoreApplication.translate("MessageBoxFactory", "File save successfully at") + f"'exports/{filename}'")
        return box

    @staticmethod
    def create_config_save_info_box(*, parent, filename: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle(QCoreApplication.translate("MessageBoxFactory", "Message"))
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(f"Config saved at 'configs/{filename}'")
        return box

    @staticmethod
    def create_config_load_info_box(*, parent, filename: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle(QCoreApplication.translate("MessageBoxFactory", "Message"))
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(QCoreApplication.translate("MessageBoxFactory", "Config loaded from") + f"'configs/{filename}'")
        return box

    @staticmethod
    def create_language_changed_info_box(*, parent, lang: str) -> QMessageBox:
        box = QMessageBox(parent)
        box.setWindowTitle(QCoreApplication.translate("MessageBoxFactory", "Message"))
        box.setIcon(QMessageBox.Icon.Information)
        box.setText(QCoreApplication.translate("MessageBoxFactory", "Language changed to ") + lang +
                    QCoreApplication.translate("MessageBoxFactory", ". Restart app to see the changes"))
        return box
