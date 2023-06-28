import os
import pathlib
import sys
import tempfile
import unittest
from typing import ClassVar

from PySide6.QtCore import QLocale, QTranslator, QSettings
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QLabel

from src.backend.PathManager import PathManager
from src.backend.SettingsManager import SettingsManager
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from src.widgets.MainWindow import MainWindow


def create_app():
    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.1.1")
    return app


def get_label_color(label: QLabel) -> QColor:
    return label.palette().color(label.backgroundRole())


class MainWindowTest(unittest.TestCase):
    """Tests the MainWidget GUI."""
    app: ClassVar[QApplication | None] = None
    temp_configs: ClassVar[tempfile.TemporaryDirectory | None] = None
    temp_exports: ClassVar[tempfile.TemporaryDirectory | None] = None
    settings_temp_file_path: ClassVar[pathlib.Path | None] = None
    settings: ClassVar[QSettings | None] = None

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

        PathManager.set_project_root(pathlib.Path(__file__).absolute().parent)

        cls.temp_configs = tempfile.TemporaryDirectory(prefix="config")
        cls.temp_exports = tempfile.TemporaryDirectory(prefix="exports")
        cls.settings_temp_file_path = PathManager.PROJECT_ROOT / 'settings.ini'

        cls.settings = SettingsManager(parent=cls.app).settings_instance()
        lang = cls.settings.value("Language", "en", type=str)
        if lang == "ru":
            lang = QLocale.Language.Russian
        elif lang == "en":
            lang = QLocale.Language.English

        # Initialize translations using resource file
        translator = QTranslator(cls.app)
        path = ':/translations'
        if translator.load(lang, 'main_gui', '_', path):
            cls.app.installTranslator(translator)

    def setUp(self):
        self.main_window = MainWindow()
        self.conways_game_of_life_widget = ConwaysGameOfLife()

    def tearDown(self):
        del self.main_window
        del self.conways_game_of_life_widget

    @classmethod
    def tearDownClass(cls):
        cls.temp_configs.cleanup()
        cls.temp_exports.cleanup()
        try:
            os.remove(str(cls.settings_temp_file_path))
        except FileNotFoundError:
            pass

    def test_defaults(self):
        self.assertEqual(int(self.main_window.ui.rows_spin_box.value()),
                         self.conways_game_of_life_widget.rows)
        self.assertEqual(int(self.main_window.ui.cols_spin_box.value()),
                         self.conways_game_of_life_widget.cols)
        self.assertEqual(int(self.main_window.ui.turn_duration_spin_box.value()),
                         self.conways_game_of_life_widget.turn_duration)
        self.assertEqual(int(self.main_window.ui.border_thickness_spin_box.value()),
                         self.conways_game_of_life_widget.border_thickness)
        self.assertEqual(get_label_color(self.main_window.ui.border_color_label),
                         self.conways_game_of_life_widget.border_color)
        self.assertEqual(get_label_color(self.main_window.ui.cell_dead_color_label),
                         self.conways_game_of_life_widget.cell_dead_color)
        self.assertEqual(get_label_color(self.main_window.ui.cell_alive_color_label),
                         self.conways_game_of_life_widget.cell_alive_color)


def suite():
    """Create a test suite."""
    test_suite = unittest.TestSuite()
    test_suite.addTest(MainWindowTest('main_window_test'))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
