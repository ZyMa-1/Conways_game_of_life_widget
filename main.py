import os
import pathlib
import sys

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from src.backend.PathManager import PathManager
from src.backend.UtilsFactory import UtilsFactory


# FOR DEBUGGING (to receive dumpObjectInfo output)
# def message_handler(mode, context, message):
#     print(message)
#
#
# qInstallMessageHandler(message_handler)


def ensure_if_ok_to_run():
    PathManager.set_project_root(pathlib.Path(__file__).absolute().parent)
    os.makedirs('configs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)
    os.makedirs('pattern_gallery', exist_ok=True)


def init_language_settings():
    UtilsFactory.create_resources()
    settings = UtilsFactory.get_settings()
    lang = settings.value("Language", "en", type=str)
    translator = QTranslator(app)
    path = f':/translations/main_gui_{lang}.qm'
    if translator.load(path):
        app.installTranslator(translator)


if __name__ == '__main__':
    ensure_if_ok_to_run()

    from src.widgets.MainWindow import MainWindow
    app = QApplication(sys.argv)
    app.setProperty("author_name", "Mikhail Ponomaryov")

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.5")

    # Retrieving language value from settings
    init_language_settings()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
