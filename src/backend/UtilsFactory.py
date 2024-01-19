from PySide6.QtCore import QObject, QSettings

from src.backend.PathManager import PathManager


class UtilsFactory(QObject):
    _settings: QSettings

    @classmethod
    def create_resources(cls, parent=None):
        cls._settings = QSettings(str(PathManager.SETTINGS_INI),
                                  QSettings.Format.IniFormat)
        cls._settings.sync()

    @classmethod
    def get_settings(cls):
        return cls._settings
