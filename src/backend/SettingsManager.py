"""
Author: ZyMa-1
"""
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
        self.settings = QSettings()
        self.settings.setDefaultFormat(QSettings.Format.IniFormat)
        self.settings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(PathManager.SETTINGS_INI))

    def settings_instance(self) -> QSettings:
        return self.settings
