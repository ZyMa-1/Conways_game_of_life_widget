from PySide6.QtCore import QObject, QSettings

from backend import PathManager


class UtilsFactory(QObject):
    """
    Factory for resources of the project.
    """
    _settings: QSettings

    @classmethod
    def create_resources(cls):
        cls._settings = QSettings(str(PathManager.SETTINGS_INI),
                                  QSettings.Format.IniFormat)
        cls._settings.sync()

    @classmethod
    def get_settings(cls):
        return cls._settings
