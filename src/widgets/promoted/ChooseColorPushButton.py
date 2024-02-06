from typing import Optional

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QColorDialog

from src.conways_game_of_life.PropertiesManager.promoted_widgets import LabelColor


class ChooseColorPushButton(QPushButton):
    selected_color_changed = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked.connect(self.open_color_dialog)
        self._selected_color: Optional[QColor] = None

    def open_color_dialog(self):
        color = QColorDialog.getColor(self.get_selected_color(), self.parentWidget())
        if color.isValid():
            self._selected_color = color
            self.selected_color_changed.emit(color)

    def get_selected_color(self):
        return self._selected_color

    @Slot(QColor)
    def handle_label_bg_color_changed(self, color: QColor):
        self.selected_color_changed = color

    def connect_label(self, label: LabelColor):
        self.selected_color_changed.connect(label.property_slot)
        label.bg_color_changed.connect(self.handle_label_bg_color_changed)
