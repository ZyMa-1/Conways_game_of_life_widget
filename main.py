"""
Author: ZyMa-1
"""

import importlib
import os
import pathlib
import sys

from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    os.environ['PROJECT_ROOT'] = str(pathlib.Path(__file__).absolute().parent)
    os.makedirs('configs', exist_ok=True)
    os.makedirs('exports', exist_ok=True)

    MainWindow = getattr(importlib.import_module('src.widgets.MainWindow'), 'MainWindow')

    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.1")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
