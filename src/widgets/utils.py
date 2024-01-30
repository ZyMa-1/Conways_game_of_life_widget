from types import MethodType

from PySide6.QtCore import Slot, QObject
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDockWidget


class _SlotFactory(QObject):
    """
    Class to create unique slot methods bounded to the class instance.
    """

    def __init__(self, action: QAction, dock_widget: QDockWidget, parent=None):
        super().__init__(parent)
        self.action = action
        self.dock_widget = dock_widget

    def get_slot(self, slot_name: str):
        method = self.SLOTS[slot_name]
        bound_method = MethodType(method, self)
        return bound_method

    @Slot(bool)
    def set_checked(self, is_visible: bool):
        self.action.setChecked(is_visible)

    @Slot()
    def set_visible(self):
        if self.action.isChecked():
            self.dock_widget.show()
        else:
            self.dock_widget.hide()

    SLOTS = {
        "set_checked": set_checked,
        "set_visible": set_visible
    }


def connect_action_and_dock_widget(action: QAction, dock_widget: QDockWidget):
    slot_factory = _SlotFactory(action, dock_widget, parent=dock_widget)
    dock_widget.visibilityChanged.connect(slot_factory.get_slot("set_checked"))
    action.triggered.connect(slot_factory.get_slot("set_visible"))
