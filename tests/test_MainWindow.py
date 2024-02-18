import os
import pathlib
import sys
import unittest
from typing import ClassVar

from PySide6.QtCore import QTranslator, QSettings
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QLabel

from backend import PathManager, UtilsFactory
from conways_game_of_life.core import GameEngine, GameScene, GameView
from widgets.MainWindow import MainWindow


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

        PathManager.set_project_root(pathlib.Path(__file__).absolute().parent)
        os.chdir(PathManager.PROJECT_ROOT)
        UtilsFactory.create_resources()
        os.makedirs('configs', exist_ok=True)
        os.makedirs('exports', exist_ok=True)
        os.makedirs('pattern_gallery', exist_ok=True)
        cls.project_dirs = [PathManager.CONFIGS_DIR,
                            PathManager.EXPORTS_DIR,
                            PathManager.PATTERN_GALLERY_DIR]

        cls.settings = UtilsFactory.get_settings()
        lang = cls.settings.value("Language", "en", type=str)
        translator = QTranslator(cls.app)
        path = f':/translations/main_gui_{lang}.qm'
        if translator.load(path):
            cls.app.installTranslator(translator)

    def setUp(self):
        self.main_window = MainWindow()
        self._game_engine = GameEngine(parent=self.main_window)
        self._game_scene = GameScene(self._game_engine, parent=self.main_window)
        self._game_view = GameView(parent_widget=self.main_window)
        self._game_view.setScene(self._game_scene)

    def tearDown(self):
        del self.main_window
        del self._game_engine
        del self._game_scene
        del self._game_view

    @classmethod
    def tearDownClass(cls):
        for dir in cls.project_dirs:
            os.rmdir(dir)

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
