import pathlib
import sys
import tempfile
import unittest
from typing import ClassVar, List

from PySide6.QtCore import QTranslator, QSettings
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QLabel

from src.backend.PathManager import PathManager
from src.backend.SettingsManager import SettingsManager
from src.backend.UtilsFactory import UtilsFactory
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from src.widgets.MainWindow import MainWindow


def create_app():
    app = QApplication(sys.argv)

    app.setOrganizationName("ZyMa-1")
    app.setApplicationName("Conway's Game Of Life Widget")
    app.setApplicationVersion("0.5")
    return app


def get_label_color(label: QLabel) -> QColor:
    return label.palette().color(label.backgroundRole())


class MainWindowTest(unittest.TestCase):
    """Tests the MainWidget GUI."""
    app: ClassVar[QApplication]
    temp_dirs: ClassVar[List[tempfile.mkdtemp]]
    settings: ClassVar[QSettings]

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

        PathManager.set_project_root(pathlib.Path(__file__).absolute().parent)
        UtilsFactory.create_resources(cls.app)

        print('wow')
        cls.temp_dirs = [tempfile.TemporaryDirectory("configs"),
                         tempfile.TemporaryDirectory("exports"),
                         tempfile.TemporaryDirectory("pattern_gallery")]

        cls.settings = SettingsManager(parent=cls.app).settings_instance()
        lang = cls.settings.value("Language", "en", type=str)
        translator = QTranslator(cls.app)
        path = f':/translations/main_gui_{lang}.qm'
        if translator.load(path):
            cls.app.installTranslator(translator)

    def setUp(self):
        self.main_window = MainWindow()
        self.conways_game_of_life_widget = ConwaysGameOfLife()

    def tearDown(self):
        del self.main_window
        del self.conways_game_of_life_widget

    @classmethod
    def tearDownClass(cls):
        pass

    def test_setup_values(self):
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
