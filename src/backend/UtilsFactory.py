from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow

from src.backend.SettingsManager import SettingsManager


class UtilsFactory(QObject):
    settings_manager: SettingsManager

    @classmethod
    def create_resources(cls, main_widget: QMainWindow):
        cls.settings_manager = SettingsManager(main_widget)

    @classmethod
    def get_settings_manager(cls):
        return cls.settings_manager

    @classmethod
    def get_settings(cls):
        return cls.settings_manager.settings_instance()
