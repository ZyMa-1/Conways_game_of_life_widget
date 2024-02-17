from PySide6.QtCore import Slot, QThreadPool, Qt
from PySide6.QtGui import QActionGroup, QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QButtonGroup

from backend import MainWindowUtils, SignalCollector, UtilsFactory
from conways_game_of_life.ConfigManager import GameConfigManager
from conways_game_of_life.core import GameScene, GameEngine
from conways_game_of_life.InstructionsDialog import InstructionsDialog
from conways_game_of_life.PropertiesManager import GamePropertiesManager
from conways_game_of_life.PatternsDataLoader import PatternsDataLoader
from conways_game_of_life.core.enums import CellEditMode
from conways_game_of_life.core.static_types import PatternSchema
from ui.Ui_MainWindow import Ui_MainWindow
from widgets.AboutDialog import AboutDialog
from widgets.helpers import DockWidgetActionBinder


class MainWindow(QMainWindow):
    """
    Main window of an application.
    """

    def __init__(self):
        super().__init__()

        # Setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set up the game from components
        self._game_engine = GameEngine(parent=self)
        self._game_scene = GameScene(self._game_engine, parent=self)
        self._game_view = self.ui.game_view
        self._game_view.setScene(self._game_scene)

        # Create ConfigManager
        self.config_manager = GameConfigManager(
            game_objects=(self._game_engine, self._game_scene),
            parent_widget=self)

        # Create PropertiesManager
        self.properties_manager = GamePropertiesManager(parent=self)

        # Create MainWindowUtils
        self.main_window_utils = MainWindowUtils(self)

        # Link widgets and game properties
        _connect_prop = self.properties_manager.connect_widget_and_obj_property
        _connect_prop(self.ui.is_game_running_label,
                      self._game_scene,
                      "is_game_running",
                      property_has_signal=True,
                      property_read_only=True)
        _connect_prop(self.ui.turn_duration_spin_box,
                      self._game_scene,
                      "turn_duration")
        _connect_prop(self.ui.border_thickness_double_spin_box,
                      self._game_scene,
                      "border_thickness")
        _connect_prop(self.ui.border_color_label,
                      self._game_scene,
                      "border_color")
        _connect_prop(self.ui.cell_alive_color_label,
                      self._game_scene,
                      "cell_alive_color")
        _connect_prop(self.ui.cell_dead_color_label,
                      self._game_scene,
                      "cell_dead_color")
        _connect_prop(self.ui.turn_number_label,
                      self._game_engine,
                      "turn_number",
                      property_has_signal=True,
                      property_read_only=True)
        _connect_prop(self.ui.alive_cells_label,
                      self._game_engine,
                      "alive_cells",
                      property_has_signal=True,
                      property_read_only=True)
        _connect_prop(self.ui.dead_cells_label,
                      self._game_engine,
                      "dead_cells",
                      property_has_signal=True,
                      property_read_only=True)
        _connect_prop(self.ui.rows_spin_box,
                      self._game_engine,
                      "rows")
        _connect_prop(self.ui.cols_spin_box,
                      self._game_engine,
                      "cols")

        # Get settings from UtilsFactory
        self.settings = UtilsFactory.get_settings()

        # Create property setter signal collector
        self.property_setter_signal_collector = SignalCollector(
            signals=(self._game_scene.property_setter_error_signal,
                     self._game_engine.property_setter_error_signal),
            parent=self)

        # Create thread pool and start patterns loader thread
        self.thread_pool = QThreadPool.globalInstance()
        self.patterns_data_loader = PatternsDataLoader()
        self.patterns_data_loader.signals.data_generated.connect(self.handle_patterns_data_generated)
        self.thread_pool.start(self.patterns_data_loader)

        # Init UI (more like create things Qt-designer cannot handle)
        self.init_ui()

        # Connect signals to slots
        self.connect_signals_to_slots()
        # extra signal stuff
        self._game_engine.turn_made.connect(self.handle_turn_made)
        self._game_view.painted.connect(self.handle_game_painted)

    # Outer Signal Handlers
    @Slot(list)
    def handle_patterns_data_generated(self, patterns_data: list[tuple[PatternSchema, QPixmap]]):
        self.ui.patterns_combo_box.setEnabled(True)
        self.ui.insert_pattern_button.setEnabled(True)
        self.ui.patterns_combo_box.clear()
        for pattern_data in patterns_data:
            self.ui.patterns_combo_box.addItem(QIcon(pattern_data[1]), pattern_data[0]["pattern_name"],
                                               userData=pattern_data[0])

    @Slot()
    def handle_turn_made(self):
        self.ui.avg_turn_performance_label.setText(
            f"{round(self._game_engine.get_avg_turn_performance() * 1000, 2)} ms")

    @Slot()
    def handle_game_painted(self):
        self.ui.avg_paint_performance_label.setText(
            f"{round(self._game_view.get_avg_paint_performance() * 1000, 2)} ms")

    # Inner Signal Handlers
    @Slot()
    def handle_start_button_clicked(self):
        self._game_scene.start_game()

    @Slot()
    def handle_stop_button_clicked(self):
        self._game_scene.stop_game()

    @Slot()
    def handle_clear_board_button_clicked(self):
        self._game_scene.clear_state()

    @Slot()
    def handle_apply_button_clicked(self):
        self.properties_manager.assign_widget_values_to_properties()
        self.show_property_signal_collector_errors()

    @Slot()
    def handle_reset_to_default_button_clicked(self):
        self._game_scene.reset_to_default()

    @Slot()
    def handle_action_about_triggered(self):
        dialog = AboutDialog(self)
        dialog.setModal(True)
        dialog.show()

    @Slot()
    def handle_action_export_to_image_triggered(self):
        filename = self.main_window_utils.save_widget_to_png(self._game_view)
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

        lang = "en"
        if "ru" in sender.objectName().lower():
            lang = "ru"
        elif "en" in sender.objectName().lower():
            lang = "en"

        self.settings.setValue("Language", "ru")
        msg = f"Language changed to '{lang}'. Restart the app to see the changes."
        message_box = self.main_window_utils.create_info_msg_box(msg)
        message_box.exec()

    @Slot(bool)
    def handle_default_mode_tool_button_toggled(self, is_checked: bool):
        if not is_checked:
            return

        self._game_scene.set_cell_edit_mode(CellEditMode.DEFAULT)

    @Slot(bool)
    def handle_paint_mode_tool_button_toggled(self, is_checked: bool):
        if not is_checked:
            return

        self._game_scene.set_cell_edit_mode(CellEditMode.PAINT)

    @Slot(bool)
    def handle_erase_mode_tool_button_toggled(self, is_checked: bool):
        if not is_checked:
            return

        self._game_scene.set_cell_edit_mode(CellEditMode.ERASE)

    @Slot()
    def handle_insert_pattern_button_clicked(self):
        selected_index = self.ui.patterns_combo_box.currentIndex()
        if selected_index == -1:
            return

        pattern_data = self.ui.patterns_combo_box.itemData(selected_index)
        self._game_scene.insert_pattern(pattern_data)

    @Slot()
    def handle_help_button_clicked(self):
        instructions_dialog = InstructionsDialog(self)
        instructions_dialog.show()

    @Slot()
    def handle_sync_button_clicked(self):
        self.properties_manager.assign_properties_values_to_widgets()

    @Slot(bool)
    def handle_keep_aspect_ratio_constraint_check_box_state_changed(self, state):
        val = (state == Qt.CheckState.Checked.value)
        self._game_view.set_keep_aspect_ratio_constraint(val)

    # Errors collector
    def show_property_signal_collector_errors(self):
        signal_data = self.property_setter_signal_collector.collect_signal_data()
        if signal_data:
            message = "\n".join(str(d) for d in signal_data)
            warning_box = self.main_window_utils.create_warning_msg_box(message)
            warning_box.exec()

    # Init methods
    def init_ui(self):
        # Create groups
        _lang_action_group = QActionGroup(self)
        _lang_action_group.setExclusive(True)
        _lang_action_group.addAction(self.ui.action_english_US)
        _lang_action_group.addAction(self.ui.action_russian_RU)

        _tools_action_group = QButtonGroup(self)
        _tools_action_group.setExclusive(True)
        _tools_action_group.addButton(self.ui.default_mode_tool_button)
        _tools_action_group.addButton(self.ui.paint_mode_tool_button)
        _tools_action_group.addButton(self.ui.erase_mode_tool_button)

        # Dock widget visibility - Checkable actions
        _binder1 = DockWidgetActionBinder(self,
                                          self.ui.action_view_settings,
                                          self.ui.settings_dock_widget)
        _binder2 = DockWidgetActionBinder(self,
                                          self.ui.action_view_game_statistics,
                                          self.ui.game_statistics_dock_widget)
        _binder3 = DockWidgetActionBinder(self,
                                          self.ui.action_view_pattern_gallery,
                                          self.ui.pattern_gallery_dock_widget)
        _binder4 = DockWidgetActionBinder(self,
                                          self.ui.action_view_edit_tools,
                                          self.ui.edit_tools_dock_widget)
        _binder5 = DockWidgetActionBinder(self,
                                          self.ui.action_view_game_size_constraints,
                                          self.ui.game_size_constraints_dock_widget)

        # Change language check box
        lang = self.settings.value("Language", "en", type=str)
        if lang == "ru":
            self.ui.action_russian_RU.setChecked(True)
        elif lang == "en":
            self.ui.action_english_US.setChecked(True)

    def connect_signals_to_slots(self):
        # Actions
        self.ui.action_about.triggered.connect(self.handle_action_about_triggered)
        self.ui.action_export_to_image.triggered.connect(self.handle_action_export_to_image_triggered)
        self.ui.action_save_config.triggered.connect(self.handle_action_save_config_triggered)
        self.ui.action_load_config.triggered.connect(self.handle_action_load_config_triggered)
        self.ui.action_english_US.changed.connect(self.handle_language_changed)
        self.ui.action_russian_RU.changed.connect(self.handle_language_changed)

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
        self.ui.keep_aspect_ratio_constraint_check_box.stateChanged.connect(
            self.handle_keep_aspect_ratio_constraint_check_box_state_changed)

        # ChooseColor buttons and LabelColors
        self.ui.border_color_button.connect_label(self.ui.border_color_label)
        self.ui.cell_alive_color_button.connect_label(self.ui.cell_alive_color_label)
        self.ui.cell_dead_color_button.connect_label(self.ui.cell_dead_color_label)
