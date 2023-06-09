"""
Author: ZyMa-1
"""

import importlib
import os
import pathlib
import sys

from PySide6.QtCore import QCoreApplication, QTranslator, QLocale, QSettings
from PySide6.QtWidgets import QApplication

import src.resources_py.rc_resources


def __keep_alive():
    _ = src.resources_py.rc_resources


if __name__ == '__main__':
    os.environ['PROJECT_ROOT'] = str(pathlib.Path(__file__).absolute().parent)
    os.makedirs('configs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)

    MainWindow = getattr(importlib.import_module('src.widgets.MainWindow'), 'MainWindow')

    app = QApplication(sys.argv)

    app.setOrganizationName(QCoreApplication.translate("Application", "ZyMa-1"))
    app.setApplicationName(QCoreApplication.translate("Application", "Conway's Game Of Life Widget"))
    app.setApplicationVersion("0.1")

    # Retrieving language value from settings
    settings = QSettings()
    lang = settings.value("Language", QLocale.Language.English, type=str)
    if lang == "ru":
        lang = QLocale.Language.Russian
    elif lang == "en":
        lang = QLocale.Language.English

    # Initialize translations using resource file
    translator = QTranslator(app)
    path = ':/translations'
    if translator.load(lang, 'main_gui', '_', path):
        app.installTranslator(translator)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
