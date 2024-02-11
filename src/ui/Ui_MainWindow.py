# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QDockWidget, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QToolButton, QVBoxLayout, QWidget)

from conways_game_of_life.PropertiesManager.promoted_widgets.LabelColor import LabelColor
from conways_game_of_life.PropertiesManager.promoted_widgets.LabelGameRunning import LabelGameRunning
from conways_game_of_life.PropertiesManager.promoted_widgets.LabelInt import LabelInt
from conways_game_of_life.core.graphics_view.GameView import GameView
from src.conways_game_of_life.PropertiesManager.promoted_widgets.SpinBoxInt import SpinBoxInt
from src.widgets.promoted.ChooseColorPushButton import ChooseColorPushButton
import src.resources.rc_resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(690, 467)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_export_to_image = QAction(MainWindow)
        self.action_export_to_image.setObjectName(u"action_export_to_image")
        self.action_save_config = QAction(MainWindow)
        self.action_save_config.setObjectName(u"action_save_config")
        self.action_load_config = QAction(MainWindow)
        self.action_load_config.setObjectName(u"action_load_config")
        self.action_view_settings = QAction(MainWindow)
        self.action_view_settings.setObjectName(u"action_view_settings")
        self.action_view_settings.setCheckable(True)
        self.action_view_settings.setChecked(True)
        self.action_english_US = QAction(MainWindow)
        self.action_english_US.setObjectName(u"action_english_US")
        self.action_english_US.setCheckable(True)
        self.action_english_US.setChecked(True)
        self.action_russian_RU = QAction(MainWindow)
        self.action_russian_RU.setObjectName(u"action_russian_RU")
        self.action_russian_RU.setCheckable(True)
        self.action_russian_RU.setMenuRole(QAction.TextHeuristicRole)
        self.action_view_edit_tools = QAction(MainWindow)
        self.action_view_edit_tools.setObjectName(u"action_view_edit_tools")
        self.action_view_edit_tools.setCheckable(True)
        self.action_view_edit_tools.setChecked(True)
        self.action_view_pattern_gallery = QAction(MainWindow)
        self.action_view_pattern_gallery.setObjectName(u"action_view_pattern_gallery")
        self.action_view_pattern_gallery.setCheckable(True)
        self.action_view_pattern_gallery.setChecked(True)
        self.action_view_game_statistics = QAction(MainWindow)
        self.action_view_game_statistics.setObjectName(u"action_view_game_statistics")
        self.action_view_game_statistics.setCheckable(True)
        self.action_view_game_statistics.setChecked(True)
        self.action_view_game_size_constraints = QAction(MainWindow)
        self.action_view_game_size_constraints.setObjectName(u"action_view_game_size_constraints")
        self.action_view_game_size_constraints.setCheckable(True)
        self.action_view_game_size_constraints.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(9, -1, 9, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.layout_top = QHBoxLayout()
        self.layout_top.setObjectName(u"layout_top")
        self.layout_top.setSizeConstraint(QLayout.SetMinimumSize)
        self.layout_top.setContentsMargins(-1, 0, -1, -1)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        self.layout_top.addWidget(self.label, 0, Qt.AlignBottom)

        self.turn_number_label = LabelInt(self.centralwidget)
        self.turn_number_label.setObjectName(u"turn_number_label")
        self.turn_number_label.setFont(font)

        self.layout_top.addWidget(self.turn_number_label, 0, Qt.AlignBottom)

        self.is_game_running_label = LabelGameRunning(self.centralwidget)
        self.is_game_running_label.setObjectName(u"is_game_running_label")
        sizePolicy1.setHeightForWidth(self.is_game_running_label.sizePolicy().hasHeightForWidth())
        self.is_game_running_label.setSizePolicy(sizePolicy1)
        self.is_game_running_label.setMinimumSize(QSize(10, 0))
        self.is_game_running_label.setFont(font)

        self.layout_top.addWidget(self.is_game_running_label, 0, Qt.AlignBottom)


        self.verticalLayout.addLayout(self.layout_top)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.help_button = QPushButton(self.centralwidget)
        self.help_button.setObjectName(u"help_button")
        self.help_button.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.help_button)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.game_view = GameView(self.centralwidget)
        self.game_view.setObjectName(u"game_view")
        self.game_view.setMinimumSize(QSize(264, 264))

        self.verticalLayout.addWidget(self.game_view)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setObjectName(u"layout_buttons")
        self.layout_buttons.setSizeConstraint(QLayout.SetMinimumSize)
        self.layout_buttons.setContentsMargins(-1, 0, -1, -1)
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")
        self.start_button.setFocusPolicy(Qt.NoFocus)

        self.layout_buttons.addWidget(self.start_button)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setFocusPolicy(Qt.NoFocus)

        self.layout_buttons.addWidget(self.stop_button)

        self.clear_board_button = QPushButton(self.centralwidget)
        self.clear_board_button.setObjectName(u"clear_board_button")
        self.clear_board_button.setFocusPolicy(Qt.NoFocus)

        self.layout_buttons.addWidget(self.clear_board_button)


        self.verticalLayout.addLayout(self.layout_buttons)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.reset_to_default_button = QPushButton(self.centralwidget)
        self.reset_to_default_button.setObjectName(u"reset_to_default_button")
        self.reset_to_default_button.setMinimumSize(QSize(0, 30))
        self.reset_to_default_button.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.reset_to_default_button)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 690, 22))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuExport = QMenu(self.menubar)
        self.menuExport.setObjectName(u"menuExport")
        self.menuSave = QMenu(self.menubar)
        self.menuSave.setObjectName(u"menuSave")
        self.menuLoad = QMenu(self.menubar)
        self.menuLoad.setObjectName(u"menuLoad")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuLanguage = QMenu(self.menubar)
        self.menuLanguage.setObjectName(u"menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.settings_dock_widget = QDockWidget(MainWindow)
        self.settings_dock_widget.setObjectName(u"settings_dock_widget")
        self.settings_dock_widget.setStyleSheet(u"")
        self.settings_dock_widget.setFloating(False)
        self.settings_dock_widget.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.settings_dock_widget.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_settings = QGridLayout()
        self.layout_settings.setObjectName(u"layout_settings")
        self.layout_settings.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.layout_settings.setContentsMargins(-1, 0, -1, -1)
        self.label_6 = QLabel(self.dockWidgetContents_2)
        self.label_6.setObjectName(u"label_6")

        self.layout_settings.addWidget(self.label_6, 6, 0, 1, 1)

        self.label_7 = QLabel(self.dockWidgetContents_2)
        self.label_7.setObjectName(u"label_7")

        self.layout_settings.addWidget(self.label_7, 8, 0, 1, 1)

        self.border_color_label = LabelColor(self.dockWidgetContents_2)
        self.border_color_label.setObjectName(u"border_color_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(2)
        sizePolicy2.setVerticalStretch(2)
        sizePolicy2.setHeightForWidth(self.border_color_label.sizePolicy().hasHeightForWidth())
        self.border_color_label.setSizePolicy(sizePolicy2)
        self.border_color_label.setMinimumSize(QSize(20, 20))
        self.border_color_label.setMaximumSize(QSize(16777215, 16777215))
        self.border_color_label.setSizeIncrement(QSize(0, 0))
        self.border_color_label.setBaseSize(QSize(0, 0))

        self.layout_settings.addWidget(self.border_color_label, 7, 2, 1, 1)

        self.cell_dead_color_button = ChooseColorPushButton(self.dockWidgetContents_2)
        self.cell_dead_color_button.setObjectName(u"cell_dead_color_button")
        self.cell_dead_color_button.setMinimumSize(QSize(0, 0))
        self.cell_dead_color_button.setFocusPolicy(Qt.NoFocus)

        self.layout_settings.addWidget(self.cell_dead_color_button, 9, 1, 1, 1)

        self.label_9 = QLabel(self.dockWidgetContents_2)
        self.label_9.setObjectName(u"label_9")

        self.layout_settings.addWidget(self.label_9, 7, 0, 1, 1)

        self.label_8 = QLabel(self.dockWidgetContents_2)
        self.label_8.setObjectName(u"label_8")

        self.layout_settings.addWidget(self.label_8, 9, 0, 1, 1)

        self.cell_alive_color_button = ChooseColorPushButton(self.dockWidgetContents_2)
        self.cell_alive_color_button.setObjectName(u"cell_alive_color_button")
        self.cell_alive_color_button.setMinimumSize(QSize(0, 0))
        self.cell_alive_color_button.setFocusPolicy(Qt.NoFocus)

        self.layout_settings.addWidget(self.cell_alive_color_button, 8, 1, 1, 1)

        self.label_2 = QLabel(self.dockWidgetContents_2)
        self.label_2.setObjectName(u"label_2")

        self.layout_settings.addWidget(self.label_2, 5, 0, 1, 1)

        self.cell_dead_color_label = LabelColor(self.dockWidgetContents_2)
        self.cell_dead_color_label.setObjectName(u"cell_dead_color_label")
        sizePolicy2.setHeightForWidth(self.cell_dead_color_label.sizePolicy().hasHeightForWidth())
        self.cell_dead_color_label.setSizePolicy(sizePolicy2)
        self.cell_dead_color_label.setMinimumSize(QSize(20, 20))

        self.layout_settings.addWidget(self.cell_dead_color_label, 9, 2, 1, 1)

        self.rows_spin_box = SpinBoxInt(self.dockWidgetContents_2)
        self.rows_spin_box.setObjectName(u"rows_spin_box")
        self.rows_spin_box.setFocusPolicy(Qt.ClickFocus)
        self.rows_spin_box.setMinimum(-100)
        self.rows_spin_box.setMaximum(200)

        self.layout_settings.addWidget(self.rows_spin_box, 3, 1, 1, 2)

        self.apply_button = QPushButton(self.dockWidgetContents_2)
        self.apply_button.setObjectName(u"apply_button")
        self.apply_button.setMinimumSize(QSize(0, 40))
        self.apply_button.setMaximumSize(QSize(16777214, 16777215))
        self.apply_button.setFocusPolicy(Qt.NoFocus)
        self.apply_button.setFlat(False)

        self.layout_settings.addWidget(self.apply_button, 10, 1, 1, 2)

        self.cols_spin_box = SpinBoxInt(self.dockWidgetContents_2)
        self.cols_spin_box.setObjectName(u"cols_spin_box")
        self.cols_spin_box.setFocusPolicy(Qt.ClickFocus)
        self.cols_spin_box.setMinimum(-100)
        self.cols_spin_box.setMaximum(200)

        self.layout_settings.addWidget(self.cols_spin_box, 4, 1, 1, 2)

        self.label_3 = QLabel(self.dockWidgetContents_2)
        self.label_3.setObjectName(u"label_3")

        self.layout_settings.addWidget(self.label_3, 3, 0, 1, 1)

        self.turn_duration_spin_box = SpinBoxInt(self.dockWidgetContents_2)
        self.turn_duration_spin_box.setObjectName(u"turn_duration_spin_box")
        self.turn_duration_spin_box.setFocusPolicy(Qt.ClickFocus)
        self.turn_duration_spin_box.setMinimum(-10000)
        self.turn_duration_spin_box.setMaximum(10000)

        self.layout_settings.addWidget(self.turn_duration_spin_box, 5, 1, 1, 2)

        self.label_4 = QLabel(self.dockWidgetContents_2)
        self.label_4.setObjectName(u"label_4")

        self.layout_settings.addWidget(self.label_4, 4, 0, 1, 1)

        self.border_thickness_spin_box = SpinBoxInt(self.dockWidgetContents_2)
        self.border_thickness_spin_box.setObjectName(u"border_thickness_spin_box")
        self.border_thickness_spin_box.setFocusPolicy(Qt.ClickFocus)
        self.border_thickness_spin_box.setMinimum(-100)

        self.layout_settings.addWidget(self.border_thickness_spin_box, 6, 1, 1, 2)

        self.border_color_button = ChooseColorPushButton(self.dockWidgetContents_2)
        self.border_color_button.setObjectName(u"border_color_button")
        self.border_color_button.setMinimumSize(QSize(0, 0))
        self.border_color_button.setFocusPolicy(Qt.NoFocus)

        self.layout_settings.addWidget(self.border_color_button, 7, 1, 1, 1)

        self.cell_alive_color_label = LabelColor(self.dockWidgetContents_2)
        self.cell_alive_color_label.setObjectName(u"cell_alive_color_label")
        sizePolicy2.setHeightForWidth(self.cell_alive_color_label.sizePolicy().hasHeightForWidth())
        self.cell_alive_color_label.setSizePolicy(sizePolicy2)
        self.cell_alive_color_label.setMinimumSize(QSize(20, 20))

        self.layout_settings.addWidget(self.cell_alive_color_label, 8, 2, 1, 1)

        self.sync_button = QPushButton(self.dockWidgetContents_2)
        self.sync_button.setObjectName(u"sync_button")
        self.sync_button.setMinimumSize(QSize(0, 40))

        self.layout_settings.addWidget(self.sync_button, 11, 1, 1, 2)


        self.verticalLayout_2.addLayout(self.layout_settings)

        self.settings_dock_widget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.settings_dock_widget)
        self.edit_tools_dock_widget = QDockWidget(MainWindow)
        self.edit_tools_dock_widget.setObjectName(u"edit_tools_dock_widget")
        self.edit_tools_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.default_mode_tool_button = QToolButton(self.dockWidgetContents_3)
        self.default_mode_tool_button.setObjectName(u"default_mode_tool_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.default_mode_tool_button.sizePolicy().hasHeightForWidth())
        self.default_mode_tool_button.setSizePolicy(sizePolicy3)
        self.default_mode_tool_button.setMinimumSize(QSize(0, 30))
        self.default_mode_tool_button.setCheckable(True)
        self.default_mode_tool_button.setChecked(True)
        self.default_mode_tool_button.setAutoExclusive(True)
        self.default_mode_tool_button.setAutoRaise(False)

        self.verticalLayout_3.addWidget(self.default_mode_tool_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.paint_mode_tool_button = QToolButton(self.dockWidgetContents_3)
        self.tool_button_group = QButtonGroup(MainWindow)
        self.tool_button_group.setObjectName(u"tool_button_group")
        self.tool_button_group.addButton(self.paint_mode_tool_button)
        self.paint_mode_tool_button.setObjectName(u"paint_mode_tool_button")
        sizePolicy3.setHeightForWidth(self.paint_mode_tool_button.sizePolicy().hasHeightForWidth())
        self.paint_mode_tool_button.setSizePolicy(sizePolicy3)
        self.paint_mode_tool_button.setMinimumSize(QSize(0, 30))
        self.paint_mode_tool_button.setCheckable(True)
        self.paint_mode_tool_button.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.paint_mode_tool_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.erase_mode_tool_button = QToolButton(self.dockWidgetContents_3)
        self.tool_button_group.addButton(self.erase_mode_tool_button)
        self.erase_mode_tool_button.setObjectName(u"erase_mode_tool_button")
        sizePolicy3.setHeightForWidth(self.erase_mode_tool_button.sizePolicy().hasHeightForWidth())
        self.erase_mode_tool_button.setSizePolicy(sizePolicy3)
        self.erase_mode_tool_button.setMinimumSize(QSize(0, 30))
        self.erase_mode_tool_button.setCheckable(True)
        self.erase_mode_tool_button.setAutoExclusive(True)

        self.verticalLayout_3.addWidget(self.erase_mode_tool_button, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.edit_tools_dock_widget.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.edit_tools_dock_widget)
        self.pattern_gallery_dock_widget = QDockWidget(MainWindow)
        self.pattern_gallery_dock_widget.setObjectName(u"pattern_gallery_dock_widget")
        self.pattern_gallery_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.verticalLayout_5 = QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.patterns_combo_box = QComboBox(self.dockWidgetContents_4)
        self.patterns_combo_box.setObjectName(u"patterns_combo_box")
        self.patterns_combo_box.setEnabled(False)
        self.patterns_combo_box.setMinimumSize(QSize(0, 34))
        self.patterns_combo_box.setFocusPolicy(Qt.NoFocus)
        self.patterns_combo_box.setIconSize(QSize(32, 32))

        self.verticalLayout_5.addWidget(self.patterns_combo_box)

        self.insert_pattern_button = QPushButton(self.dockWidgetContents_4)
        self.insert_pattern_button.setObjectName(u"insert_pattern_button")
        self.insert_pattern_button.setEnabled(False)
        self.insert_pattern_button.setFocusPolicy(Qt.NoFocus)

        self.verticalLayout_5.addWidget(self.insert_pattern_button)

        self.pattern_gallery_dock_widget.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.pattern_gallery_dock_widget)
        self.game_statistics_dock_widget = QDockWidget(MainWindow)
        self.game_statistics_dock_widget.setObjectName(u"game_statistics_dock_widget")
        self.game_statistics_dock_widget.setMinimumSize(QSize(170, 126))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_8 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_10 = QLabel(self.dockWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_11 = QLabel(self.dockWidgetContents)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.avg_turn_performance_label = QLabel(self.dockWidgetContents)
        self.avg_turn_performance_label.setObjectName(u"avg_turn_performance_label")

        self.gridLayout.addWidget(self.avg_turn_performance_label, 2, 1, 1, 1)

        self.label_5 = QLabel(self.dockWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.dead_cells_label = LabelInt(self.dockWidgetContents)
        self.dead_cells_label.setObjectName(u"dead_cells_label")

        self.gridLayout.addWidget(self.dead_cells_label, 1, 1, 1, 1)

        self.alive_cells_label = LabelInt(self.dockWidgetContents)
        self.alive_cells_label.setObjectName(u"alive_cells_label")

        self.gridLayout.addWidget(self.alive_cells_label, 0, 1, 1, 1)

        self.label_12 = QLabel(self.dockWidgetContents)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 3, 0, 1, 1)

        self.avg_paint_performance_label = QLabel(self.dockWidgetContents)
        self.avg_paint_performance_label.setObjectName(u"avg_paint_performance_label")

        self.gridLayout.addWidget(self.avg_paint_performance_label, 3, 1, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout)

        self.game_statistics_dock_widget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.game_statistics_dock_widget)
        self.game_size_constraints_dock_widget = QDockWidget(MainWindow)
        self.game_size_constraints_dock_widget.setObjectName(u"game_size_constraints_dock_widget")
        self.dockWidgetContents_5 = QWidget()
        self.dockWidgetContents_5.setObjectName(u"dockWidgetContents_5")
        self.verticalLayout_6 = QVBoxLayout(self.dockWidgetContents_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.square_size_constraint_check_box = QCheckBox(self.dockWidgetContents_5)
        self.square_size_constraint_check_box.setObjectName(u"square_size_constraint_check_box")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.square_size_constraint_check_box.sizePolicy().hasHeightForWidth())
        self.square_size_constraint_check_box.setSizePolicy(sizePolicy4)

        self.verticalLayout_6.addWidget(self.square_size_constraint_check_box)

        self.perfect_size_constraint_check_box = QCheckBox(self.dockWidgetContents_5)
        self.perfect_size_constraint_check_box.setObjectName(u"perfect_size_constraint_check_box")

        self.verticalLayout_6.addWidget(self.perfect_size_constraint_check_box)

        self.game_size_constraints_dock_widget.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.game_size_constraints_dock_widget)
        QWidget.setTabOrder(self.rows_spin_box, self.cols_spin_box)
        QWidget.setTabOrder(self.cols_spin_box, self.border_thickness_spin_box)
        QWidget.setTabOrder(self.border_thickness_spin_box, self.cell_alive_color_button)
        QWidget.setTabOrder(self.cell_alive_color_button, self.border_color_button)
        QWidget.setTabOrder(self.border_color_button, self.cell_dead_color_button)
        QWidget.setTabOrder(self.cell_dead_color_button, self.turn_duration_spin_box)

        self.menubar.addAction(self.menuSave.menuAction())
        self.menubar.addAction(self.menuLoad.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuExport.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuExport.addAction(self.action_export_to_image)
        self.menuSave.addAction(self.action_save_config)
        self.menuLoad.addAction(self.action_load_config)
        self.menuView.addAction(self.action_view_settings)
        self.menuView.addAction(self.action_view_edit_tools)
        self.menuView.addAction(self.action_view_pattern_gallery)
        self.menuView.addAction(self.action_view_game_statistics)
        self.menuView.addAction(self.action_view_game_size_constraints)
        self.menuLanguage.addAction(self.action_english_US)
        self.menuLanguage.addAction(self.action_russian_RU)

        self.retranslateUi(MainWindow)

        self.apply_button.setDefault(False)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
#if QT_CONFIG(statustip)
        self.action_about.setStatusTip(QCoreApplication.translate("MainWindow", u"About application", None))
#endif // QT_CONFIG(statustip)
        self.action_export_to_image.setText(QCoreApplication.translate("MainWindow", u"Export to image", None))
#if QT_CONFIG(statustip)
        self.action_export_to_image.setStatusTip(QCoreApplication.translate("MainWindow", u"Export game widget to image", None))
#endif // QT_CONFIG(statustip)
        self.action_save_config.setText(QCoreApplication.translate("MainWindow", u"Save config", None))
#if QT_CONFIG(statustip)
        self.action_save_config.setStatusTip(QCoreApplication.translate("MainWindow", u"Save config", None))
#endif // QT_CONFIG(statustip)
        self.action_load_config.setText(QCoreApplication.translate("MainWindow", u"Load config", None))
#if QT_CONFIG(statustip)
        self.action_load_config.setStatusTip(QCoreApplication.translate("MainWindow", u"Load config", None))
#endif // QT_CONFIG(statustip)
        self.action_view_settings.setText(QCoreApplication.translate("MainWindow", u"Game of life settings", None))
#if QT_CONFIG(statustip)
        self.action_view_settings.setStatusTip(QCoreApplication.translate("MainWindow", u"Change Dock widget visibility", None))
#endif // QT_CONFIG(statustip)
        self.action_english_US.setText(QCoreApplication.translate("MainWindow", u"English (US)", None))
#if QT_CONFIG(statustip)
        self.action_english_US.setStatusTip(QCoreApplication.translate("MainWindow", u"English", None))
#endif // QT_CONFIG(statustip)
        self.action_russian_RU.setText(QCoreApplication.translate("MainWindow", u"Russian (RU)", None))
#if QT_CONFIG(statustip)
        self.action_russian_RU.setStatusTip(QCoreApplication.translate("MainWindow", u"Russian", None))
#endif // QT_CONFIG(statustip)
        self.action_view_edit_tools.setText(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.action_view_pattern_gallery.setText(QCoreApplication.translate("MainWindow", u"Pattern gallery", None))
        self.action_view_game_statistics.setText(QCoreApplication.translate("MainWindow", u"Game Statistics", None))
        self.action_view_game_size_constraints.setText(QCoreApplication.translate("MainWindow", u"Game size constraints", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Turn number:", None))
#if QT_CONFIG(statustip)
        self.turn_number_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Turn number label", None))
#endif // QT_CONFIG(statustip)
        self.turn_number_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(statustip)
        self.is_game_running_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Is game running label", None))
#endif // QT_CONFIG(statustip)
        self.is_game_running_label.setText(QCoreApplication.translate("MainWindow", u":)", None))
        self.help_button.setText(QCoreApplication.translate("MainWindow", u"Help (?)", None))
#if QT_CONFIG(statustip)
        self.start_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Start game button", None))
#endif // QT_CONFIG(statustip)
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
#if QT_CONFIG(statustip)
        self.stop_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Stop game button", None))
#endif // QT_CONFIG(statustip)
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(statustip)
        self.clear_board_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Clear board button", None))
#endif // QT_CONFIG(statustip)
        self.clear_board_button.setText(QCoreApplication.translate("MainWindow", u"Clear board", None))
#if QT_CONFIG(statustip)
        self.reset_to_default_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Reset to default button", None))
#endif // QT_CONFIG(statustip)
        self.reset_to_default_button.setText(QCoreApplication.translate("MainWindow", u"Reset to default", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuSave.setTitle(QCoreApplication.translate("MainWindow", u"Save", None))
        self.menuLoad.setTitle(QCoreApplication.translate("MainWindow", u"Load", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
#if QT_CONFIG(statustip)
        self.settings_dock_widget.setStatusTip(QCoreApplication.translate("MainWindow", u"Settings dock widget", None))
#endif // QT_CONFIG(statustip)
        self.settings_dock_widget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Game of life settings", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Border thickness:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Cell alive color:", None))
#if QT_CONFIG(statustip)
        self.border_color_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Label displaying color", None))
#endif // QT_CONFIG(statustip)
        self.border_color_label.setText("")
#if QT_CONFIG(statustip)
        self.cell_dead_color_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Cell dead color button", None))
#endif // QT_CONFIG(statustip)
        self.cell_dead_color_button.setText(QCoreApplication.translate("MainWindow", u"Choose color...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Border color:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Cell dead color:", None))
#if QT_CONFIG(statustip)
        self.cell_alive_color_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Cell alive color button", None))
#endif // QT_CONFIG(statustip)
        self.cell_alive_color_button.setText(QCoreApplication.translate("MainWindow", u"Choose color...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Turn duration:", None))
#if QT_CONFIG(statustip)
        self.cell_dead_color_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Label displaying color", None))
#endif // QT_CONFIG(statustip)
        self.cell_dead_color_label.setText("")
#if QT_CONFIG(statustip)
        self.rows_spin_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Row count spin box", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(statustip)
        self.apply_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Apply button", None))
#endif // QT_CONFIG(statustip)
        self.apply_button.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
#if QT_CONFIG(statustip)
        self.cols_spin_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Column count spin box", None))
#endif // QT_CONFIG(statustip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Row count:", None))
#if QT_CONFIG(statustip)
        self.turn_duration_spin_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Turn duration spin box", None))
#endif // QT_CONFIG(statustip)
        self.turn_duration_spin_box.setSuffix(QCoreApplication.translate("MainWindow", u" ms", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Column count:", None))
#if QT_CONFIG(statustip)
        self.border_thickness_spin_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Border thickness spin box", None))
#endif // QT_CONFIG(statustip)
        self.border_thickness_spin_box.setSuffix(QCoreApplication.translate("MainWindow", u" px", None))
#if QT_CONFIG(statustip)
        self.border_color_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Border color button", None))
#endif // QT_CONFIG(statustip)
        self.border_color_button.setText(QCoreApplication.translate("MainWindow", u"Choose color...", None))
#if QT_CONFIG(statustip)
        self.cell_alive_color_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Label displaying color", None))
#endif // QT_CONFIG(statustip)
        self.cell_alive_color_label.setText("")
#if QT_CONFIG(statustip)
        self.sync_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Sync button", None))
#endif // QT_CONFIG(statustip)
        self.sync_button.setText(QCoreApplication.translate("MainWindow", u"Sync", None))
#if QT_CONFIG(statustip)
        self.edit_tools_dock_widget.setStatusTip(QCoreApplication.translate("MainWindow", u"Edit tools dock widget", None))
#endif // QT_CONFIG(statustip)
        self.edit_tools_dock_widget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Edit tools", None))
#if QT_CONFIG(statustip)
        self.default_mode_tool_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Default mode - change cell states one by one", None))
#endif // QT_CONFIG(statustip)
        self.default_mode_tool_button.setText(QCoreApplication.translate("MainWindow", u"\"Default\" mode", None))
#if QT_CONFIG(statustip)
        self.paint_mode_tool_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Paint mode - Create multiple alive cells by dragging your mouse over the widget", None))
#endif // QT_CONFIG(statustip)
        self.paint_mode_tool_button.setText(QCoreApplication.translate("MainWindow", u"\"Paint\" mode", None))
#if QT_CONFIG(statustip)
        self.erase_mode_tool_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Erase mode - Delete multiple alive cells by dragging your mouse over the widget", None))
#endif // QT_CONFIG(statustip)
        self.erase_mode_tool_button.setText(QCoreApplication.translate("MainWindow", u"\"Erase\" mode", None))
#if QT_CONFIG(statustip)
        self.pattern_gallery_dock_widget.setStatusTip(QCoreApplication.translate("MainWindow", u"Pattern gallery dock widget", None))
#endif // QT_CONFIG(statustip)
        self.pattern_gallery_dock_widget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pattern gallery", None))
#if QT_CONFIG(statustip)
        self.patterns_combo_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Patterns combo box", None))
#endif // QT_CONFIG(statustip)
        self.patterns_combo_box.setCurrentText("")
        self.patterns_combo_box.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Choose pattern", None))
#if QT_CONFIG(statustip)
        self.insert_pattern_button.setStatusTip(QCoreApplication.translate("MainWindow", u"Insert pattern to a current active cell", None))
#endif // QT_CONFIG(statustip)
        self.insert_pattern_button.setText(QCoreApplication.translate("MainWindow", u"Insert pattern\n"
"to current \n"
"position", None))
#if QT_CONFIG(statustip)
        self.game_statistics_dock_widget.setStatusTip(QCoreApplication.translate("MainWindow", u"Game statistics dock widget", None))
#endif // QT_CONFIG(statustip)
        self.game_statistics_dock_widget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Game Statistics", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Dead cells:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Avg turn time:", None))
#if QT_CONFIG(statustip)
        self.avg_turn_performance_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Avg turn performance label", None))
#endif // QT_CONFIG(statustip)
        self.avg_turn_performance_label.setText(QCoreApplication.translate("MainWindow", u"0 ms", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Alive cells:", None))
#if QT_CONFIG(statustip)
        self.dead_cells_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Dead cells label", None))
#endif // QT_CONFIG(statustip)
        self.dead_cells_label.setText(QCoreApplication.translate("MainWindow", u"a lot", None))
#if QT_CONFIG(statustip)
        self.alive_cells_label.setStatusTip(QCoreApplication.translate("MainWindow", u"Alive cells label", None))
#endif // QT_CONFIG(statustip)
        self.alive_cells_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Avg paint time:", None))
        self.avg_paint_performance_label.setText(QCoreApplication.translate("MainWindow", u"0 ms", None))
#if QT_CONFIG(statustip)
        self.game_size_constraints_dock_widget.setStatusTip(QCoreApplication.translate("MainWindow", u"Game size constraints dock widget", None))
#endif // QT_CONFIG(statustip)
        self.game_size_constraints_dock_widget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Game size constraints", None))
#if QT_CONFIG(statustip)
        self.square_size_constraint_check_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Square size constraint check box", None))
#endif // QT_CONFIG(statustip)
        self.square_size_constraint_check_box.setText(QCoreApplication.translate("MainWindow", u"Square size constraint", None))
#if QT_CONFIG(statustip)
        self.perfect_size_constraint_check_box.setStatusTip(QCoreApplication.translate("MainWindow", u"Perfect size constraint check box", None))
#endif // QT_CONFIG(statustip)
        self.perfect_size_constraint_check_box.setText(QCoreApplication.translate("MainWindow", u"Perfect size constraint", None))
    # retranslateUi

