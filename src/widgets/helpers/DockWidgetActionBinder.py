from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDockWidget


class DockWidgetActionBinder(QObject):
    def __init__(self, parent, w1: QAction | QDockWidget, w2: QAction | QDockWidget):
        super().__init__(parent)

        if isinstance(w1, QAction) and isinstance(w2, QDockWidget):
            self.dock_widget = w2
            self.action = w1
        elif isinstance(w1, QDockWidget) and isinstance(w2, QAction):
            self.dock_widget = w1
            self.action = w2
        else:
            raise ValueError

        # Connect signals to slots
        self.action.triggered.connect(self.set_visible)
        self.dock_widget.visibilityChanged.connect(self.set_checked)

    @Slot(bool)
    def set_checked(self, is_visible: bool):
        self.action.setChecked(is_visible)

    @Slot()
    def set_visible(self):
        if self.action.isChecked():
            self.dock_widget.show()
        else:
            self.dock_widget.hide()
