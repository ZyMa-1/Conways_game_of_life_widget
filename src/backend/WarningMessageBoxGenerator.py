"""
Author: ZyMa-1
"""

from PySide6.QtCore import QObject, QCoreApplication
from PySide6.QtWidgets import QMessageBox

from src.backend.SignalCollector import SignalCollector


class WarningMessageBoxGenerator(QObject):
    def __init__(self, signal_collector: SignalCollector, parent=None):
        super().__init__(parent)
        self.signal_collector = signal_collector

    def generate_warning_message_box(self, parent=None) -> None | QMessageBox:
        """Returns 'QMessageBox' object if signal_collector data is not None, None otherwise."""
        signal_data = self.signal_collector.collect_signal_data()
        if signal_data:
            message = "\n".join([str(d) for d in signal_data])
            warning_box = QMessageBox(parent)
            warning_box.setIcon(QMessageBox.Icon.Warning)
            warning_box.setWindowTitle(QCoreApplication.translate("WarningDialogGenerator", "Warning"))
            warning_box.setText(message)
            return warning_box
        return None
