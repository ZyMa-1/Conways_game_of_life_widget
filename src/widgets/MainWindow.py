"""
Author: ZyMa-1
"""

from PySide6.QtCore import Slot, QObject, QSettings
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import QMainWindow, QLabel, QColorDialog, QPushButton

from src.backend.ImageSaver import ImageSaver
from src.backend.MessageBoxFactory import MessageBoxFactory
from src.backend.SettingsManager import SettingsManager
from src.backend.SignalCollector import SignalCollector
from src.backend.WarningMessageBoxGenerator import WarningMessageBoxGenerator
from src.conways_game_of_life.ConfigManager.ConwaysGameOfLifeConfigManager import ConwaysGameOfLifeConfigManager
from src.conways_game_of_life.PropertiesManager.ConwaysGameOfLifePropertiesManager import \
    ConwaysGameOfLifePropertiesManager
from src.ui.Ui_MainWindow import Ui_MainWindow
from src.widgets.AboutDialog import AboutDialog


class ColorDialogHandler(QObject):
    def __init__(self, *, button: QPushButton, label: QLabel, parent=None):
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

        # Create expected attributes
        self.color_dialog_handler_1: ColorDialogHandler | None = None
        self.color_dialog_handler_2: ColorDialogHandler | None = None
        self.color_dialog_handler_3: ColorDialogHandler | None = None
        self.lang_action_group: QActionGroup | None = None
        self.config_manager: ConwaysGameOfLifeConfigManager | None = None
        self.properties_manager: ConwaysGameOfLifePropertiesManager | None = None
        self.settings: QSettings | None = None
        self.image_saver: ImageSaver | None = None
        self.warning_generator: WarningMessageBoxGenerator | None = None

        # Init UI
        self.create_all_annoying_stuff()
        self.init_ui()

        self.connect_signals_to_slots()

    def init_ui(self):
        # Create action group
        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)
        self.lang_action_group.addAction(self.ui.action_english_US)
        self.lang_action_group.addAction(self.ui.action_russian_RU)

        # Change language check box
        lang = self.settings.value("Language", "en", type=str)
        if lang == "ru":
            self.ui.action_russian_RU.setChecked(True)
        elif lang == "en":
            self.ui.action_english_US.setChecked(True)
        self.ui.conways_game_of_life_widget.setFocus()

        # Create color dialog handlers

        self.color_dialog_handler_1 = ColorDialogHandler(button=self.ui.border_color_button,
                                                         label=self.ui.border_color_label,
                                                         parent=self)
        self.color_dialog_handler_2 = ColorDialogHandler(button=self.ui.cell_alive_color_button,
                                                         label=self.ui.cell_alive_color_label,
                                                         parent=self)
        self.color_dialog_handler_3 = ColorDialogHandler(button=self.ui.cell_dead_color_button,
                                                         label=self.ui.cell_dead_color_label,
                                                         parent=self)

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
        self.properties_manager.assign_all_widget_values_to_properties()

        warning = self.warning_generator.generate_warning_message_box(parent=self)
        if warning is not None:
            warning.exec()

    @Slot()
    def handle_reset_to_default_button_clicked(self):
        self.ui.conways_game_of_life_widget.reset_to_default()
        self.ui.conways_game_of_life_widget.setFocus()

    @Slot()
    def handle_action_about_triggered(self):
        dialog = AboutDialog(self)
        dialog.setModal(True)
        dialog.show()

    @Slot()
    def handle_action_export_to_image_triggered(self):
        filename = self.image_saver.save_widget_to_image(self.ui.conways_game_of_life_widget,
                                                         file_type="png",
                                                         parent=self)
        if filename is not None:
            message_box = MessageBoxFactory.create_file_save_info_box(parent=self,
                                                                      filename=filename)
            message_box.exec()

    @Slot()
    def handle_action_save_config_triggered(self):
        filename = self.config_manager.save_config(parent=self)
        if filename is not None:
            message_box = MessageBoxFactory.create_config_save_info_box(parent=self,
                                                                        filename=filename)
            message_box.exec()

    @Slot()
    def handle_action_load_config_triggered(self):
        filename = self.config_manager.load_config(parent=self)
        if filename is not None:
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
    def handle_language_changed(self):
        sender = self.sender()
        is_checked = sender.isChecked()
        if not is_checked:
            return

        if "ru" in sender.objectName().lower():
            self.settings.setValue("Language", "ru")
            message_box = MessageBoxFactory.create_language_changed_info_box(parent=self,
                                                                             lang="ru")
            message_box.exec()
        elif "en" in sender.objectName().lower():
            self.settings.setValue("Language", "en")
            message_box = MessageBoxFactory.create_language_changed_info_box(parent=self,
                                                                             lang="en")
            message_box.exec()

    # Init functions

    def create_all_annoying_stuff(self):
        # Create ConfigManager
        self.config_manager = ConwaysGameOfLifeConfigManager(
            self.ui.conways_game_of_life_widget,
            parent=self)

        # Create PropertiesManager
        self.properties_manager = ConwaysGameOfLifePropertiesManager(
            self.ui.conways_game_of_life_widget,
            parent=self)

        # Create handlers for widgets using property manager
        self.properties_manager.add_handler_by_property_name(widget=self.ui.is_game_running_label,
                                                             property_name="is_game_running",
                                                             is_both_way=False)
        self.properties_manager.add_handler_by_property_name(widget=self.ui.turn_number_label,
                                                             property_name="turn_number",
                                                             is_both_way=False)
        self.properties_manager.add_handler_by_property_name(widget=self.ui.rows_spin_box,
                                                             property_name="rows")
        self.properties_manager.add_handler_by_property_name(widget=self.ui.cols_spin_box,
                                                             property_name="cols")
        self.properties_manager.add_handler_by_property_name(widget=self.ui.turn_duration_spin_box,
                                                             property_name="turn_duration")
        self.properties_manager.add_handler_by_property_name(widget=self.ui.border_thickness_spin_box,
                                                             property_name="border_thickness")
        self.properties_manager.add_handler_by_property_name(widget=self.ui.border_color_label,
                                                             property_name="border_color")
        self.properties_manager.add_handler_by_property_name(widget=self.ui.cell_alive_color_label,
                                                             property_name="cell_alive_color")
        self.properties_manager.add_handler_by_property_name(widget=self.ui.cell_dead_color_label,
                                                             property_name="cell_dead_color")

        # Create settings
        self.settings = SettingsManager().settings_instance()

        # Create ImageSaver
        self.image_saver = ImageSaver(parent=self)

        # Create Warning dialog generator with 'SignalCollector' of 'property_setter_error_signal'
        self.warning_generator = WarningMessageBoxGenerator(
            SignalCollector(self.ui.conways_game_of_life_widget.property_setter_error_signal, parent=self),
            parent=self)

    def connect_signals_to_slots(self):
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
        self.ui.action_english_US.changed.connect(self.handle_language_changed)
        self.ui.action_russian_RU.changed.connect(self.handle_language_changed)
