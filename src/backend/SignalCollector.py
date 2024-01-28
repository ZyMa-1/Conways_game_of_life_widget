from PySide6.QtCore import QObject, Signal


class SignalCollector(QObject):
    """
    Class for collecting cumulative signal data.
    """

    def __init__(self, signal: Signal, parent=None):
        super().__init__(parent)
        self.signal_cumulative_data = []
        signal.connect(self._handle_signal)

    def collect_signal_data(self):
        res = self.signal_cumulative_data.copy()
        self.signal_cumulative_data.clear()
        return res

    def _handle_signal(self, *args):
        self.signal_cumulative_data.append(args)
