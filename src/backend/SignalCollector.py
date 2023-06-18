"""
Author: ZyMa-1
"""

from copy import copy

from PySide6.QtCore import QObject, Signal


class SignalCollector(QObject):
    """Class for accumulating signal data."""

    def __init__(self, signal: Signal, parent=None):
        super().__init__(parent)
        self.signal_cumulative_data = []

        signal.connect(self._handle_signal)

    def collect_signal_data(self):
        res = copy(self.signal_cumulative_data)
        self._delete_signal_data()
        return res

    def _handle_signal(self, *args):
        self.signal_cumulative_data.append(args)

    def _delete_signal_data(self):
        self.signal_cumulative_data.clear()
