"""
Author: ZyMa-1
"""

import importlib
import os
import pathlib
import sys

from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtWidgets import QApplication

import src.resources_py.rc_resources
from src.backend.PathManager import PathManager
from src.backend.SettingsManager import SettingsManager


# FOR DEBUGGING (to receive dumpObjectInfo output)
# def message_handler(mode, context, message):
#     print(message)
#
#
# qInstallMessageHandler(message_handler)

def __keep_alive():
    _ = src.resources_py.rc_resources


def ensure_if_ok_to_run():
    PathManager.set_project_root(pathlib.Path(__file__).absolute().parent)
    os.makedirs('configs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)


def init_language_settings():
    settings = SettingsManager(parent=app).settings_instance()
    lang = settings.value("Language", "en", type=str)
    if lang == "ru":
        lang = QLocale.Language.Russian
    elif lang == "en":
        lang = QLocale.Language.English

    # Initialize translations using resource file
    translator = QTranslator(app)
    path = ':/translations'
    if translator.load(lang, 'main_gui', '_', path):
        app.installTranslator(translator)


if __name__ == '__main__':
    ensure_if_ok_to_run()

    MainWindow = getattr(importlib.import_module('src.widgets.MainWindow'), 'MainWindow')

    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.1")

    # Retrieving language value from settings
    init_language_settings()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
