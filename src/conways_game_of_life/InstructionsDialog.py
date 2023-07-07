from PySide6.QtCore import Qt, Slot, QPoint
from PySide6.QtWidgets import QDialog

from src.ui.Ui_InstructionsDialog import Ui_InstructionsDialog


class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup UI
        self.ui = Ui_InstructionsDialog()
        self.ui.setupUi(self)
        self.setVisible(False)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        # Connect signals to slots
        self.ui.close_button.clicked.connect(self.handle_close_button_clicked)

        self.draggable = False
        self.offset = QPoint()

    @Slot()
    def handle_close_button_clicked(self):
        self.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draggable = False
