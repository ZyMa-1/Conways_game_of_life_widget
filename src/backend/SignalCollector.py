from typing import Iterable

from PySide6.QtCore import QObject, Signal


class SignalCollector(QObject):
    """
    Class for collecting cumulative data from the given list of Signals.
    """

    def __init__(self, signals: Iterable[Signal], parent=None):
        super().__init__(parent)
        self.signals_cumulative_data = []
        for signal in signals:
            signal.connect(self._handle_signal)

    def collect_signal_data(self):
        res = self.signals_cumulative_data.copy()
        self.signals_cumulative_data.clear()
        return res

    def _handle_signal(self, *args):
        self.signals_cumulative_data.append(args)
