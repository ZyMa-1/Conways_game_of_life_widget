"""
Author: ZyMa-1
"""
import os

from PySide6.QtCore import QObject, QSettings

from src.backend.PathManager import PathManager


# Chat GPT woo-hoo
class _SingletonMeta(type(QObject), type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SettingsManager(QObject, metaclass=_SingletonMeta):
    def __init__(self, parent=None):
        super().__init__(parent)
        settings_path = str(PathManager.SETTINGS_INI)

        # Check if the INI file exists, and create it if not
        if not os.path.exists(settings_path):
            with open(settings_path, 'w'):
                pass

        self.settings = QSettings(settings_path, QSettings.Format.IniFormat)
        if not self.settings.contains("Language"):
            self.settings.setValue("Language", "en")

    def settings_instance(self) -> QSettings:
        return self.settings
