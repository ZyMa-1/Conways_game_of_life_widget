from PySide6.QtWidgets import QFileDialog


class FileDialogFactory:
    @staticmethod
    def create_save_config_file_dialog(*, parent, dir: str) -> QFileDialog:
        file_dialog = QFileDialog(parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setDirectory(dir)
        file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Save Config")
        return file_dialog

    @staticmethod
    def create_load_config_file_dialog(*, parent, dir: str) -> QFileDialog:
        file_dialog = QFileDialog(parent)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setDirectory(dir)
        file_dialog.setNameFilters(["JSON Files (*.json)"])
        file_dialog.setWindowTitle("Load Config")
        return file_dialog