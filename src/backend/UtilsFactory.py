from PySide6.QtCore import QObject

from src.backend.SettingsManager import SettingsManager


class UtilsFactory(QObject):
    settings_manager: SettingsManager

    @classmethod
    def create_resources(cls, parent=None):
        cls.settings_manager = SettingsManager(parent=parent)

    @classmethod
    def get_settings_manager(cls):
        return cls.settings_manager

    @classmethod
    def get_settings(cls):
        return cls.settings_manager.settings_instance()
