from PySide6.QtCore import QObject, QSettings

from backend import PathManager


class SettingsManager(QObject):
    """
    Class to handle QSettings instance.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings(str(PathManager.SETTINGS_INI),
                                  QSettings.Format.IniFormat)
        self.settings.sync()

    def settings_instance(self) -> QSettings:
        return self.settings
