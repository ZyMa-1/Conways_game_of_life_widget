from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QApplication

from ui.Ui_AboutDialog import Ui_AboutDialog


class AboutDialog(QDialog):
    """
    Dialog to display info about app.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup UI
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

        # Update app_version and app_name labels
        app = QApplication.instance()
        app_version = app.applicationVersion()
        app_name = app.applicationName()
        app_organization_name = app.organizationName()
        app_author_name = app.property("author_name")

        self.ui.app_name_label.setText(app_name)
        self.ui.author_name_label.setText(f"{app_organization_name} ({app_author_name})")
        self.ui.app_version_label.setText(app_version)

        text = (f"Spend my free time on this project (:<br>v{app_version} is for AITU python project.<br><a "
                f"href='https://github.com/ZyMa-1/Conways_game_of_life_widget/blob/master/LICENCE'>LICENSE</a>")
        self.ui.text_label.setTextFormat(Qt.TextFormat.RichText)
        self.ui.text_label.setOpenExternalLinks(True)
        self.ui.text_label.setText(text)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
