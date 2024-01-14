from PySide6.QtCore import QObject, QSettings

from src.backend.PathManager import PathManager


class SettingsManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings(str(PathManager.SETTINGS_INI),
                                  QSettings.Format.IniFormat)
        self.settings.sync()

    def settings_instance(self) -> QSettings:
        return self.settings
