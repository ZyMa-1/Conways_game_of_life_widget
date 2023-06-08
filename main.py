"""
Author: ZyMa-1
"""

import os
import pathlib
import sys

from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    os.environ['PROJECT_ROOT'] = str(pathlib.Path(__file__).parent)
    from src.widgets.MainWindow import MainWindow

    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.1")

    window = MainWindow()
    window.show()
    # app.exec()
    # pixmap = window.grab()
    # pixmap.save(str("readme_images/1.png"))
    sys.exit(app.exec())
