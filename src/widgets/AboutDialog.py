from PySide6.QtWidgets import QDialog, QApplication

from src.ui.Ui_AboutDialog import Ui_AboutDialog


class AboutDialog(QDialog):
    """
    Dialog to display info about app
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup UI
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

        # Update app_version and app_name labels
        app_instance = QApplication.instance()
        app_version = app_instance.applicationVersion()
        app_name = app_instance.applicationName()
        app_organization_name = app_instance.organizationName()
        app_author_name = "Mikhail Ponomaryov"

        self.ui.app_name_label.setText(app_name)
        self.ui.author_name_label.setText(f"{app_organization_name} ({app_author_name})")
        self.ui.app_version_label.setText(app_version)
        self.ui.text_label.setText(f"Spend my free time on this project (:\nv{app_version} is for AITU python project.")

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
