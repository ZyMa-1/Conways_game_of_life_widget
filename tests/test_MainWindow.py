import pathlib
import sys
import unittest
from typing import ClassVar

from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QLabel

from src.conways_game_of_life.core import GameEngine, GameScene, GameView


def create_app():
    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.7")
    return app


def get_label_color(label: QLabel) -> QColor:
    return label.palette().color(label.backgroundRole())


class MainWindowTest(unittest.TestCase):
    """
    Tests If the application can launch xD.
    """
    app: ClassVar[QApplication]
    project_dirs: ClassVar[list[pathlib.Path]]
    settings: ClassVar[QSettings]

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

    def setUp(self):
        self._game_engine = GameEngine()
        self._game_scene = GameScene(self._game_engine)
        self._game_view = GameView()
        self._game_view.setScene(self._game_scene)

    def tearDown(self):
        del self._game_engine
        del self._game_scene
        del self._game_view

    @classmethod
    def tearDownClass(cls):
        pass

    def test_setup_values(self):
        ...


def suite():
    """
    Create a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(MainWindowTest('main_window_test'))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
