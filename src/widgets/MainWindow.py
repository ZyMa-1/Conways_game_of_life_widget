"""
Author: ZyMa-1
"""

from PySide6.QtCore import Slot, QObject
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QLabel, QColorDialog, QPushButton

from src.backend.ImageSaver import ImageSaver
from src.backend.MessageBoxFactory import MessageBoxFactory
from src.backend.SignalCollector import SignalCollector
from src.backend.WarningDialogGenerator import WarningDialogGenerator
from src.conways_game_of_life.ConwaysGameOfLifeConfigManager import ConwaysGameOfLifeConfigManager
from src.ui.Ui_MainWindow import Ui_MainWindow
from src.widgets.AboutDialog import AboutDialog


class ColorDialogHandler(QObject):
    def __init__(self, button: QPushButton, label: QLabel, parent=None):
        super().__init__(parent)
        self._label = label
        button.clicked.connect(self.open_color_dialog)

    @Slot()
    def open_color_dialog(self):
        color = QColorDialog.getColor(parent=self.parent())
        if color.isValid():
            self._label.setStyleSheet(f"background-color: rgb({color.red()},{color.green()},{color.blue()});")


class MainWindow(QMainWindow):
    """
    Main window of an application
    """

    def __init__(self):
        super().__init__()

        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self._create_all_annoying_stuff()

        self._connect_signals_to_slots()

    def init_ui(self):
        self._game_properties_to_widgets_values()
        self.ui.conways_game_of_life_widget.setFocus()

    @Slot()
    def handle_start_button_clicked(self):
        self.ui.conways_game_of_life_widget.start_game()

    @Slot()
    def handle_stop_button_clicked(self):
        self.ui.conways_game_of_life_widget.stop_game()
        self.ui.conways_game_of_life_widget.setFocus()

    @Slot()
    def handle_clear_board_button_clicked(self):
        self.ui.conways_game_of_life_widget.clear_state()
        self.ui.conways_game_of_life_widget.setFocus()

    @Slot()
    def handle_apply_button_clicked(self):
        self._widgets_values_to_game_properties()

        warning = self.warning_dialog_generator.generate_warning_dialog(parent=self)
        if warning is not None:
            warning.exec()

    @Slot()
    def handle_action_about_triggered(self):
        dialog = AboutDialog(self)
        dialog.setModal(True)
        dialog.show()

    @Slot()
    def handle_action_export_to_image_triggered(self):
        filename = ImageSaver().save_widget_to_image(self.ui.conways_game_of_life_widget,
                                                     file_type="png")
        if filename is not None:
            message_box = MessageBoxFactory.create_file_save_info_box(parent=self,
                                                                      filename=filename)
            message_box.exec()

    @Slot()
    def handle_action_save_config_triggered(self):
        filename = self.game_config_manager.save_config(parent=self)
        if filename is not None:
            message_box = MessageBoxFactory.create_config_save_info_box(parent=self,
                                                                        filename=filename)
            message_box.exec()

    @Slot()
    def handle_action_load_config_triggered(self):
        filename = self.game_config_manager.load_config(parent=self)
        if filename is not None:
            self._game_properties_to_widgets_values()
            message_box = MessageBoxFactory.create_config_load_info_box(parent=self,
                                                                        filename=filename)
            message_box.exec()

    @Slot(bool)
    def handle_action_view_dock_widget_triggered(self, is_checked: bool):
        if is_checked:
            self.ui.dockWidget.show()
        else:
            self.ui.dockWidget.hide()

    @Slot()
    def handle_reset_to_default_button_clicked(self):
        self.ui.conways_game_of_life_widget.reset_to_default()
        self._widgets_values_to_game_properties()
        self.ui.conways_game_of_life_widget.setFocus()

    # :Annoying functions that my eyes are afraid of:
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away
    # Get away

    def _widgets_values_to_game_properties(self):
        self.ui.conways_game_of_life_widget.rows = int(self.ui.rows_spin_box.value())
        self.ui.conways_game_of_life_widget.cols = int(self.ui.cols_spin_box.value())
        self.ui.conways_game_of_life_widget.turn_duration = int(self.ui.turn_duration_spin_box.value())
        self.ui.conways_game_of_life_widget.border_thickness = int(self.ui.border_thickness_spin_box.value())
        self.ui.conways_game_of_life_widget.border_color = self._get_label_bg_color(self.ui.border_color_label)
        self.ui.conways_game_of_life_widget.cell_dead_color = self._get_label_bg_color(self.ui.cell_dead_color_label)
        self.ui.conways_game_of_life_widget.cell_alive_color = self._get_label_bg_color(self.ui.cell_alive_color_label)

    def _game_properties_to_widgets_values(self):
        self.ui.rows_spin_box.setValue(self.ui.conways_game_of_life_widget.rows)
        self.ui.cols_spin_box.setValue(self.ui.conways_game_of_life_widget.cols)
        self.ui.turn_duration_spin_box.setValue(self.ui.conways_game_of_life_widget.turn_duration)
        self.ui.border_thickness_spin_box.setValue(self.ui.conways_game_of_life_widget.border_thickness)
        color = self.ui.conways_game_of_life_widget.border_color
        r, g, b = color.red(), color.green(), color.blue()
        self.ui.border_color_label.setStyleSheet(f"background-color: rgb({r},{g},{b});")
        color = self.ui.conways_game_of_life_widget.cell_dead_color
        r, g, b = color.red(), color.green(), color.blue()
        self.ui.cell_dead_color_label.setStyleSheet(f"background-color: rgb({r},{g},{b});")
        color = self.ui.conways_game_of_life_widget.cell_alive_color
        r, g, b = color.red(), color.green(), color.blue()
        self.ui.cell_alive_color_label.setStyleSheet(f"background-color: rgb({r},{g},{b});")

    @staticmethod
    def _get_label_bg_color(label: QLabel) -> QColor:
        return label.palette().color(label.backgroundRole())

    def _create_all_annoying_stuff(self):
        # Add game widget handlers
        self.ui.conways_game_of_life_widget.add_turn_number_handler(self.ui.turn_number_label)
        self.ui.conways_game_of_life_widget.add_is_game_running_handler(self.ui.is_game_running_label)

        # Create Warning dialog generator with 'SignalCollector' of 'property_setter_error_signal'
        self.warning_dialog_generator = WarningDialogGenerator(
            SignalCollector(self.ui.conways_game_of_life_widget.property_setter_error_signal, parent=self), parent=self)

        # Create ConfigManager
        self.game_config_manager = ConwaysGameOfLifeConfigManager(self.ui.conways_game_of_life_widget, parent=self)

        # Create ImageSaver
        self.image_saver = ImageSaver(parent=self)

        # Create color dialog handlers
        self.color_dialog_handler_1 = ColorDialogHandler(self.ui.border_color_button,
                                                         self.ui.border_color_label,
                                                         parent=self)
        self.color_dialog_handler_2 = ColorDialogHandler(self.ui.cell_alive_color_button,
                                                         self.ui.cell_alive_color_label,
                                                         parent=self)
        self.color_dialog_handler_3 = ColorDialogHandler(self.ui.cell_dead_color_button,
                                                         self.ui.cell_dead_color_label,
                                                         parent=self)

    def _connect_signals_to_slots(self):
        self.ui.action_about.triggered.connect(self.handle_action_about_triggered)
        self.ui.start_button.clicked.connect(self.handle_start_button_clicked)
        self.ui.stop_button.clicked.connect(self.handle_stop_button_clicked)
        self.ui.clear_board_button.clicked.connect(self.handle_clear_board_button_clicked)
        self.ui.apply_button.clicked.connect(self.handle_apply_button_clicked)
        self.ui.action_export_to_image.triggered.connect(self.handle_action_export_to_image_triggered)
        self.ui.action_save_config.triggered.connect(self.handle_action_save_config_triggered)
        self.ui.action_load_config.triggered.connect(self.handle_action_load_config_triggered)
        self.ui.action_view_dock_widget.triggered.connect(self.handle_action_view_dock_widget_triggered)
        self.ui.reset_to_default_button.clicked.connect(self.handle_reset_to_default_button_clicked)
        self.ui.dockWidget.visibilityChanged.connect(
            lambda is_visible: self.ui.action_view_dock_widget.setChecked(is_visible))
