from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDockWidget


def connect_action_and_dock_widget(action: QAction, dock_widget: QDockWidget):
    dock_widget.visibilityChanged.connect(lambda is_visible: action.setChecked(is_visible))
    action.triggered.connect(lambda is_checked: dock_widget.setVisible(is_checked))
