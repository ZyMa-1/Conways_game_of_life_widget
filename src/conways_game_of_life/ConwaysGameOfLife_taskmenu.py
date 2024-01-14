from PySide6.QtCore import Slot
from PySide6.QtDesigner import (QExtensionFactory, QPyDesignerTaskMenuExtension)
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from src.ui.Ui_ConwaysGameOfLifeDialog import Ui_ConwaysGameOfLifeDialog


# The task menu extensions by the tutorial
class ConwaysGameOfLifeDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        # Setup UI
        self.ui = Ui_ConwaysGameOfLifeDialog()
        self.ui.setupUi(self)

        # Connect signals to slots
        self.ui.button_box.accepted.connect(self.accept)
        self.ui.button_box.rejected.connect(self.reject)

    def set_values(self, conways_game_of_life_widget: ConwaysGameOfLife):
        self.ui.conways_game_of_life_widget.state = conways_game_of_life_widget.state


class ConwaysGameOfLifeTaskMenu(QPyDesignerTaskMenuExtension):
    def __init__(self, conways_game_of_life_widget: ConwaysGameOfLife, parent):
        super().__init__(parent)
        self._conways_game_of_life_widget = conways_game_of_life_widget
        self._edit_widget_action = QAction('Edit Widget...', None)
        self._edit_widget_action.triggered.connect(self._edit_widget)

    def taskActions(self):
        return [self._edit_widget_action]

    def preferredEditAction(self):
        return self._edit_widget_action

    @Slot()
    def _edit_widget(self):
        dialog = ConwaysGameOfLifeDialog(self._conways_game_of_life_widget)
        dialog.set_values(self._conways_game_of_life_widget)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self._conways_game_of_life_widget.state = dialog.ui.conways_game_of_life_widget.state


class ConwaysGameOfLifeTaskMenuFactory(QExtensionFactory):
    def __init__(self, extension_manager):
        super().__init__(extension_manager)

    @staticmethod
    def task_menu_iid():
        return 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != ConwaysGameOfLifeTaskMenuFactory.task_menu_iid():
            return None
        if object.__class__.__name__ != 'ConwaysGameOfLife':
            return None
        return ConwaysGameOfLifeTaskMenu(object, parent)
