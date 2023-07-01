from typing import List, Tuple, Dict

from PySide6.QtCore import QObject
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QComboBox


class PatternsDataComboBoxLoader(QObject):
    @staticmethod
    def load_patterns_data_to_combo_box(patterns_data: List[Tuple[Dict, QPixmap]], combo_box: QComboBox):
        combo_box.clear()
        for pattern_data in patterns_data:
            combo_box.addItem(QIcon(pattern_data[1]), pattern_data[0]["pattern_name"],
                              userData=pattern_data[0])

