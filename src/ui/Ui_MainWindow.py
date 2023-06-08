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
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpinBox,
    QStatusBar, QVBoxLayout, QWidget)

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(574, 481)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_export_to_image = QAction(MainWindow)
        self.action_export_to_image.setObjectName(u"action_export_to_image")
        self.actionExport_config_to_json = QAction(MainWindow)
        self.actionExport_config_to_json.setObjectName(u"actionExport_config_to_json")
        self.action_export_to_mp4 = QAction(MainWindow)
        self.action_export_to_mp4.setObjectName(u"action_export_to_mp4")
        self.action_save_config = QAction(MainWindow)
        self.action_save_config.setObjectName(u"action_save_config")
        self.action_load_config = QAction(MainWindow)
        self.action_load_config.setObjectName(u"action_load_config")
        self.action_view_dock_widget = QAction(MainWindow)
        self.action_view_dock_widget.setObjectName(u"action_view_dock_widget")
        self.action_view_dock_widget.setCheckable(True)
        self.action_view_dock_widget.setChecked(True)
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

        self.turn_number_label = QLabel(self.centralwidget)
        self.turn_number_label.setObjectName(u"turn_number_label")
        self.turn_number_label.setFont(font)

        self.layout_top.addWidget(self.turn_number_label, 0, Qt.AlignBottom)

        self.is_game_running_label = QLabel(self.centralwidget)
        self.is_game_running_label.setObjectName(u"is_game_running_label")
        sizePolicy1.setHeightForWidth(self.is_game_running_label.sizePolicy().hasHeightForWidth())
        self.is_game_running_label.setSizePolicy(sizePolicy1)
        self.is_game_running_label.setMinimumSize(QSize(10, 0))
        self.is_game_running_label.setFont(font)

        self.layout_top.addWidget(self.is_game_running_label, 0, Qt.AlignBottom)


        self.verticalLayout.addLayout(self.layout_top)

        self.conways_game_of_life_widget = ConwaysGameOfLife(self.centralwidget)
        self.conways_game_of_life_widget.setObjectName(u"conways_game_of_life_widget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.conways_game_of_life_widget.sizePolicy().hasHeightForWidth())
        self.conways_game_of_life_widget.setSizePolicy(sizePolicy2)
        self.conways_game_of_life_widget.setMinimumSize(QSize(0, 0))
        self.conways_game_of_life_widget.setMaximumSize(QSize(16777215, 16777215))
        self.conways_game_of_life_widget.setSizeIncrement(QSize(0, 0))
        self.conways_game_of_life_widget.setFocusPolicy(Qt.StrongFocus)
        self.conways_game_of_life_widget.setProperty("cols", 10)
        self.conways_game_of_life_widget.setProperty("rows", 10)
        self.conways_game_of_life_widget.setProperty("turn_duration", 1500)
        self.conways_game_of_life_widget.setProperty("border_thickness", 2)
        self.conways_game_of_life_widget.setProperty("cell_dead_color", QColor(255, 255, 255))

        self.verticalLayout.addWidget(self.conways_game_of_life_widget)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.setObjectName(u"layout_buttons")
        self.layout_buttons.setSizeConstraint(QLayout.SetMinimumSize)
        self.layout_buttons.setContentsMargins(-1, 0, -1, -1)
        self.start_button = QPushButton(self.centralwidget)
        self.start_button.setObjectName(u"start_button")

        self.layout_buttons.addWidget(self.start_button)

        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")

        self.layout_buttons.addWidget(self.stop_button)

        self.clear_board_button = QPushButton(self.centralwidget)
        self.clear_board_button.setObjectName(u"clear_board_button")

        self.layout_buttons.addWidget(self.clear_board_button)


        self.verticalLayout.addLayout(self.layout_buttons)

        self.reset_to_default_button = QPushButton(self.centralwidget)
        self.reset_to_default_button.setObjectName(u"reset_to_default_button")
        self.reset_to_default_button.setMinimumSize(QSize(0, 30))

        self.verticalLayout.addWidget(self.reset_to_default_button)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 574, 22))
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
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setStyleSheet(u"")
        self.dockWidget.setFloating(False)
        self.dockWidget.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout_2 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.layout_settings = QGridLayout()
        self.layout_settings.setObjectName(u"layout_settings")
        self.layout_settings.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.layout_settings.setContentsMargins(-1, 0, -1, -1)
        self.label_4 = QLabel(self.dockWidgetContents_2)
        self.label_4.setObjectName(u"label_4")

        self.layout_settings.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_6 = QLabel(self.dockWidgetContents_2)
        self.label_6.setObjectName(u"label_6")

        self.layout_settings.addWidget(self.label_6, 6, 0, 1, 1)

        self.label_2 = QLabel(self.dockWidgetContents_2)
        self.label_2.setObjectName(u"label_2")

        self.layout_settings.addWidget(self.label_2, 5, 0, 1, 1)

        self.apply_button = QPushButton(self.dockWidgetContents_2)
        self.apply_button.setObjectName(u"apply_button")
        self.apply_button.setMinimumSize(QSize(0, 40))
        self.apply_button.setMaximumSize(QSize(16777214, 16777215))
        self.apply_button.setFocusPolicy(Qt.ClickFocus)
        self.apply_button.setFlat(False)

        self.layout_settings.addWidget(self.apply_button, 10, 1, 1, 2)

        self.turn_duration_spin_box = QSpinBox(self.dockWidgetContents_2)
        self.turn_duration_spin_box.setObjectName(u"turn_duration_spin_box")
        self.turn_duration_spin_box.setMinimum(-10000)
        self.turn_duration_spin_box.setMaximum(10000)

        self.layout_settings.addWidget(self.turn_duration_spin_box, 5, 1, 1, 2)

        self.rows_spin_box = QSpinBox(self.dockWidgetContents_2)
        self.rows_spin_box.setObjectName(u"rows_spin_box")
        self.rows_spin_box.setFocusPolicy(Qt.WheelFocus)
        self.rows_spin_box.setMinimum(-100)
        self.rows_spin_box.setMaximum(100)

        self.layout_settings.addWidget(self.rows_spin_box, 3, 1, 1, 2)

        self.cell_alive_color_button = QPushButton(self.dockWidgetContents_2)
        self.cell_alive_color_button.setObjectName(u"cell_alive_color_button")
        self.cell_alive_color_button.setMinimumSize(QSize(0, 0))

        self.layout_settings.addWidget(self.cell_alive_color_button, 8, 1, 1, 1)

        self.label_9 = QLabel(self.dockWidgetContents_2)
        self.label_9.setObjectName(u"label_9")

        self.layout_settings.addWidget(self.label_9, 7, 0, 1, 1)

        self.border_color_button = QPushButton(self.dockWidgetContents_2)
        self.border_color_button.setObjectName(u"border_color_button")
        self.border_color_button.setMinimumSize(QSize(0, 0))

        self.layout_settings.addWidget(self.border_color_button, 7, 1, 1, 1)

        self.cell_dead_color_label = QLabel(self.dockWidgetContents_2)
        self.cell_dead_color_label.setObjectName(u"cell_dead_color_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(2)
        sizePolicy3.setHeightForWidth(self.cell_dead_color_label.sizePolicy().hasHeightForWidth())
        self.cell_dead_color_label.setSizePolicy(sizePolicy3)
        self.cell_dead_color_label.setMinimumSize(QSize(20, 20))

        self.layout_settings.addWidget(self.cell_dead_color_label, 9, 2, 1, 1)

        self.border_color_label = QLabel(self.dockWidgetContents_2)
        self.border_color_label.setObjectName(u"border_color_label")
        sizePolicy3.setHeightForWidth(self.border_color_label.sizePolicy().hasHeightForWidth())
        self.border_color_label.setSizePolicy(sizePolicy3)
        self.border_color_label.setMinimumSize(QSize(20, 20))
        self.border_color_label.setMaximumSize(QSize(16777215, 16777215))
        self.border_color_label.setSizeIncrement(QSize(0, 0))
        self.border_color_label.setBaseSize(QSize(0, 0))

        self.layout_settings.addWidget(self.border_color_label, 7, 2, 1, 1)

        self.label_7 = QLabel(self.dockWidgetContents_2)
        self.label_7.setObjectName(u"label_7")

        self.layout_settings.addWidget(self.label_7, 8, 0, 1, 1)

        self.cell_dead_color_button = QPushButton(self.dockWidgetContents_2)
        self.cell_dead_color_button.setObjectName(u"cell_dead_color_button")
        self.cell_dead_color_button.setMinimumSize(QSize(0, 0))

        self.layout_settings.addWidget(self.cell_dead_color_button, 9, 1, 1, 1)

        self.label_3 = QLabel(self.dockWidgetContents_2)
        self.label_3.setObjectName(u"label_3")

        self.layout_settings.addWidget(self.label_3, 3, 0, 1, 1)

        self.label_8 = QLabel(self.dockWidgetContents_2)
        self.label_8.setObjectName(u"label_8")

        self.layout_settings.addWidget(self.label_8, 9, 0, 1, 1)

        self.cols_spin_box = QSpinBox(self.dockWidgetContents_2)
        self.cols_spin_box.setObjectName(u"cols_spin_box")
        self.cols_spin_box.setMinimum(-100)
        self.cols_spin_box.setMaximum(100)

        self.layout_settings.addWidget(self.cols_spin_box, 4, 1, 1, 2)

        self.cell_alive_color_label = QLabel(self.dockWidgetContents_2)
        self.cell_alive_color_label.setObjectName(u"cell_alive_color_label")
        sizePolicy3.setHeightForWidth(self.cell_alive_color_label.sizePolicy().hasHeightForWidth())
        self.cell_alive_color_label.setSizePolicy(sizePolicy3)
        self.cell_alive_color_label.setMinimumSize(QSize(20, 20))

        self.layout_settings.addWidget(self.cell_alive_color_label, 8, 2, 1, 1)

        self.border_thickness_spin_box = QSpinBox(self.dockWidgetContents_2)
        self.border_thickness_spin_box.setObjectName(u"border_thickness_spin_box")
        self.border_thickness_spin_box.setMinimum(-100)

        self.layout_settings.addWidget(self.border_thickness_spin_box, 6, 1, 1, 2)


        self.verticalLayout_2.addLayout(self.layout_settings)

        self.dockWidget.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget)
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
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.action_about)
        self.menuExport.addAction(self.action_export_to_image)
        self.menuSave.addAction(self.action_save_config)
        self.menuLoad.addAction(self.action_load_config)
        self.menuView.addAction(self.action_view_dock_widget)

        self.retranslateUi(MainWindow)

        self.apply_button.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_export_to_image.setText(QCoreApplication.translate("MainWindow", u"Export to image", None))
        self.actionExport_config_to_json.setText(QCoreApplication.translate("MainWindow", u"Export config to json", None))
        self.action_export_to_mp4.setText(QCoreApplication.translate("MainWindow", u"Export to mp4", None))
        self.action_save_config.setText(QCoreApplication.translate("MainWindow", u"Save config", None))
        self.action_load_config.setText(QCoreApplication.translate("MainWindow", u"Load config", None))
        self.action_view_dock_widget.setText(QCoreApplication.translate("MainWindow", u"Game of life settings", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Turn number:", None))
        self.turn_number_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.is_game_running_label.setText(QCoreApplication.translate("MainWindow", u":)", None))
#if QT_CONFIG(statustip)
        self.conways_game_of_life_widget.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.conways_game_of_life_widget.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.clear_board_button.setText(QCoreApplication.translate("MainWindow", u"Clear board", None))
        self.reset_to_default_button.setText(QCoreApplication.translate("MainWindow", u"Reset to default", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.menuExport.setTitle(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuSave.setTitle(QCoreApplication.translate("MainWindow", u"Save", None))
        self.menuLoad.setTitle(QCoreApplication.translate("MainWindow", u"Load", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", u"Game of life settings", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Column count:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Border thickness:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Turn duration:", None))
        self.apply_button.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.turn_duration_spin_box.setSuffix(QCoreApplication.translate("MainWindow", u" ms", None))
        self.cell_alive_color_button.setText(QCoreApplication.translate("MainWindow", u"Choose color...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Border color:", None))
        self.border_color_button.setText(QCoreApplication.translate("MainWindow", u"Choose color...", None))
        self.cell_dead_color_label.setText("")
        self.border_color_label.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Cell alive color:", None))
        self.cell_dead_color_button.setText(QCoreApplication.translate("MainWindow", u"Choose color...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Row count:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Cell dead color:", None))
        self.cell_alive_color_label.setText("")
        self.border_thickness_spin_box.setSuffix(QCoreApplication.translate("MainWindow", u" px", None))
    # retranslateUi

