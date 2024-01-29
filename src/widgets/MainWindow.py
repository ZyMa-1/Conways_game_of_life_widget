from typing import List, Tuple, Dict

from PySide6.QtCore import Slot, QObject, QThreadPool, Qt
from PySide6.QtGui import QActionGroup, QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QLabel, QColorDialog, QPushButton, QButtonGroup

from src.backend.MainWindowUtils import MainWindowUtils
from src.backend.SignalCollector import SignalCollector
from src.backend.UtilsFactory import UtilsFactory
from src.conways_game_of_life.ConfigManager.ConwaysGameOfLifeConfigManager import ConwaysGameOfLifeConfigManager
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife
from src.conways_game_of_life.InstructionsDialog import InstructionsDialog
from src.conways_game_of_life.PropertiesManager.ConwaysGameOfLifePropertiesManager import \
    ConwaysGameOfLifePropertiesManager
from src.conways_game_of_life.PatternsDataLoader import PatternsDataLoader
from src.ui.Ui_MainWindow import Ui_MainWindow
from src.widgets.AboutDialog import AboutDialog
from src.widgets import utils


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

        # Create ConfigManager
        self.config_manager = ConwaysGameOfLifeConfigManager(
            self.ui.conways_game_of_life_widget,
            parent=self)

        # Create PropertiesManager
        self.properties_manager = ConwaysGameOfLifePropertiesManager(
            self.ui.conways_game_of_life_widget,
            parent=self)

        # Create MainWindowUtils
        self.main_window_utils = MainWindowUtils(self)

        # Link widget and game properties
        self.properties_manager.connect_widget_and_property(self.ui.is_game_running_label,
                                                            "is_game_running",
                                                            property_has_signal=True,
                                                            property_read_only=True)
        self.properties_manager.connect_widget_and_property(self.ui.turn_number_label,
                                                            "turn_number",
                                                            property_has_signal=True,
                                                            property_read_only=True)
        self.properties_manager.connect_widget_and_property(self.ui.alive_cells_label,
                                                            "alive_cells",
                                                            property_has_signal=True,
                                                            property_read_only=True)
        self.properties_manager.connect_widget_and_property(self.ui.dead_cells_label,
                                                            "dead_cells",
                                                            property_has_signal=True,
                                                            property_read_only=True)
        self.properties_manager.connect_widget_and_property(self.ui.rows_spin_box,
                                                            "rows")
        self.properties_manager.connect_widget_and_property(self.ui.cols_spin_box,
                                                            "cols")
        self.properties_manager.connect_widget_and_property(self.ui.turn_duration_spin_box,
                                                            "turn_duration")
        self.properties_manager.connect_widget_and_property(self.ui.border_thickness_spin_box,
                                                            "border_thickness")
        self.properties_manager.connect_widget_and_property(self.ui.border_color_label,
                                                            "border_color")
        self.properties_manager.connect_widget_and_property(self.ui.cell_alive_color_label,
                                                            "cell_alive_color")
        self.properties_manager.connect_widget_and_property(self.ui.cell_dead_color_label,
                                                            "cell_dead_color")

        # Get settings from UtilsFactory
        self.settings = UtilsFactory.get_settings()

        # Create property setter signal collector
        self.property_setter_signal_collector = SignalCollector(
            self.ui.conways_game_of_life_widget.property_setter_error_signal, parent=self)

        # Create thread pool and start patterns loader thread
        self.thread_pool = QThreadPool.globalInstance()
        self.pattern_data_loader = PatternsDataLoader()
        self.pattern_data_loader.signals.data_generated.connect(self.handle_patterns_data_loaded)
        self.thread_pool.start(self.pattern_data_loader)

        # Init UI (more like create things I cannot create in Qt-designer)
        self.init_ui()

        self.connect_signals_to_slots()

    # Outer Handlers
    @Slot(list)
    def handle_patterns_data_loaded(self, patterns_data: List[Tuple[Dict, QPixmap]]):
        self.ui.patterns_combo_box.setEnabled(True)
        self.ui.insert_pattern_button.setEnabled(True)
        self.ui.patterns_combo_box.clear()
        for pattern_data in patterns_data:
            self.ui.patterns_combo_box.addItem(QIcon(pattern_data[1]), pattern_data[0]["pattern_name"],
                                               userData=pattern_data[0])

    # Inner handlers
    @Slot()
    def handle_start_button_clicked(self):
        self.ui.conways_game_of_life_widget.start_game()

    @Slot()
    def handle_stop_button_clicked(self):
        self.ui.conways_game_of_life_widget.stop_game()

    @Slot()
    def handle_clear_board_button_clicked(self):
        self.ui.conways_game_of_life_widget.clear_state()

    @Slot()
    def handle_apply_button_clicked(self):
        self.properties_manager.assign_widget_values_to_properties()
        self.show_property_signal_collector_errors()

    @Slot()
    def handle_reset_to_default_button_clicked(self):
        self.ui.conways_game_of_life_widget.reset_to_default()

    @Slot()
    def handle_action_about_triggered(self):
        dialog = AboutDialog(self)
        dialog.setModal(True)
        dialog.show()

    @Slot()
    def handle_action_export_to_image_triggered(self):
        filename = self.main_window_utils.save_widget_to_png(self.ui.conways_game_of_life_widget)
        if filename:
            msg = f"File saved as {filename}"
            message_box = self.main_window_utils.create_info_msg_box(msg)
            message_box.exec()

    @Slot()
    def handle_action_save_config_triggered(self):
        filename = self.config_manager.save_config()
        if filename:
            msg = f"Config saved as {filename}"
            message_box = self.main_window_utils.create_info_msg_box(msg)
            message_box.exec()

    @Slot()
    def handle_action_load_config_triggered(self):
        filename = self.config_manager.load_config()
        if filename:
            msg = f"Config loaded from {filename}"
            message_box = self.main_window_utils.create_info_msg_box(msg)
            message_box.exec()
            self.show_property_signal_collector_errors()

    @Slot()
    def handle_language_changed(self):
        sender = self.sender()
        is_checked = sender.isChecked()
        if not is_checked:
            return

        if "ru" in sender.objectName().lower():
            self.settings.setValue("Language", "ru")
            msg = "Language changed to 'ru'. Restart the app to see the changes."
            message_box = self.main_window_utils.create_info_msg_box(msg)
            message_box.exec()
        elif "en" in sender.objectName().lower():
            self.settings.setValue("Language", "en")
            msg = "Language changed to 'en'. Restart the app to see the changes."
            message_box = self.main_window_utils.create_info_msg_box(msg)
            message_box.exec()

    @Slot(bool)
    def handle_default_mode_tool_button_toggled(self, is_checked: bool):
        if not is_checked:
            return

        self.ui.conways_game_of_life_widget.set_edit_mode(ConwaysGameOfLife.EditMode.DEFAULT)

    @Slot(bool)
    def handle_paint_mode_tool_button_toggled(self, is_checked: bool):
        if not is_checked:
            return

        self.ui.conways_game_of_life_widget.set_edit_mode(ConwaysGameOfLife.EditMode.PAINT)

    @Slot(bool)
    def handle_erase_mode_tool_button_toggled(self, is_checked: bool):
        if not is_checked:
            return

        self.ui.conways_game_of_life_widget.set_edit_mode(ConwaysGameOfLife.EditMode.ERASE)

    @Slot()
    def handle_insert_pattern_button_clicked(self):
        selected_index = self.ui.patterns_combo_box.currentIndex()
        if selected_index == -1:
            return

        pattern_data = self.ui.patterns_combo_box.itemData(selected_index)
        self.ui.conways_game_of_life_widget.insert_pattern(pattern_data)

    @Slot()
    def handle_help_button_clicked(self):
        instructions_dialog = InstructionsDialog(self)
        instructions_dialog.show()

    @Slot()
    def handle_sync_button_clicked(self):
        self.properties_manager.assign_properties_values_to_widgets()

    @Slot(bool)
    def handle_square_size_constraint_check_box_state_changed(self, state):
        val = (state == Qt.CheckState.Checked.value)
        self.ui.conways_game_of_life_widget.set_square_size_constraint(val)

    @Slot(bool)
    def handle_perfect_size_constraint_check_box_state_changed(self, state):
        val = (state == Qt.CheckState.Checked.value)
        self.ui.conways_game_of_life_widget.set_perfect_size_constraint(val)

    # Yeah
    def show_property_signal_collector_errors(self):
        signal_data = self.property_setter_signal_collector.collect_signal_data()
        if signal_data:
            message = "\n".join(str(d) for d in signal_data)
            warning_box = self.main_window_utils.create_warning_msg_box(message)
            warning_box.exec()

    # Init methods
    def init_ui(self):
        # Create action groups
        _lang_action_group = QActionGroup(self)
        _lang_action_group.setExclusive(True)
        _lang_action_group.addAction(self.ui.action_english_US)
        _lang_action_group.addAction(self.ui.action_russian_RU)

        _tools_action_group = QButtonGroup(self)
        _tools_action_group.setExclusive(True)
        _tools_action_group.addButton(self.ui.default_mode_tool_button)
        _tools_action_group.addButton(self.ui.paint_mode_tool_button)
        _tools_action_group.addButton(self.ui.erase_mode_tool_button)

        # Change language check box
        lang = self.settings.value("Language", "en", type=str)
        if lang == "ru":
            self.ui.action_russian_RU.setChecked(True)
        elif lang == "en":
            self.ui.action_english_US.setChecked(True)

        # Create color dialog handlers
        _color_dialog_handlers = [ColorDialogHandler(button=self.ui.border_color_button,
                                                     label=self.ui.border_color_label,
                                                     parent=self),
                                  ColorDialogHandler(button=self.ui.cell_alive_color_button,
                                                     label=self.ui.cell_alive_color_label,
                                                     parent=self),
                                  ColorDialogHandler(button=self.ui.cell_dead_color_button,
                                                     label=self.ui.cell_dead_color_label,
                                                     parent=self)]

    def connect_signals_to_slots(self):
        # Actions
        self.ui.action_about.triggered.connect(self.handle_action_about_triggered)
        self.ui.action_export_to_image.triggered.connect(self.handle_action_export_to_image_triggered)
        self.ui.action_save_config.triggered.connect(self.handle_action_save_config_triggered)
        self.ui.action_load_config.triggered.connect(self.handle_action_load_config_triggered)
        self.ui.action_english_US.changed.connect(self.handle_language_changed)
        self.ui.action_russian_RU.changed.connect(self.handle_language_changed)

        # Dock widgets
        utils.connect_action_to_dock_widget(self.ui.action_view_settings, self.ui.settings_dock_widget)
        utils.connect_action_to_dock_widget(self.ui.action_view_game_statistics, self.ui.game_statistics_dock_widget)
        utils.connect_action_to_dock_widget(self.ui.action_view_pattern_gallery, self.ui.pattern_gallery_dock_widget)
        utils.connect_action_to_dock_widget(self.ui.action_view_edit_tools, self.ui.edit_tools_dock_widget)
        utils.connect_action_to_dock_widget(self.ui.action_view_game_size_constraints,
                                            self.ui.game_size_constraints_dock_widget)

        # Buttons/Toggles
        self.ui.start_button.clicked.connect(self.handle_start_button_clicked)
        self.ui.stop_button.clicked.connect(self.handle_stop_button_clicked)
        self.ui.clear_board_button.clicked.connect(self.handle_clear_board_button_clicked)
        self.ui.apply_button.clicked.connect(self.handle_apply_button_clicked)
        self.ui.reset_to_default_button.clicked.connect(self.handle_reset_to_default_button_clicked)
        self.ui.insert_pattern_button.clicked.connect(self.handle_insert_pattern_button_clicked)
        self.ui.default_mode_tool_button.toggled.connect(self.handle_default_mode_tool_button_toggled)
        self.ui.paint_mode_tool_button.toggled.connect(self.handle_paint_mode_tool_button_toggled)
        self.ui.erase_mode_tool_button.toggled.connect(self.handle_erase_mode_tool_button_toggled)
        self.ui.help_button.clicked.connect(self.handle_help_button_clicked)
        self.ui.sync_button.clicked.connect(self.handle_sync_button_clicked)
        self.ui.square_size_constraint_check_box.stateChanged.connect(
            self.handle_square_size_constraint_check_box_state_changed)
        self.ui.perfect_size_constraint_check_box.stateChanged.connect(
            self.handle_perfect_size_constraint_check_box_state_changed)
