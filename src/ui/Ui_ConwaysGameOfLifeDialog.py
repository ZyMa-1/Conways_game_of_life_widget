# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ConwaysGameOfLifeDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QSizePolicy, QVBoxLayout, QWidget)

from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife

class Ui_ConwaysGameOfLifeDialog(object):
    def setupUi(self, ConwaysGameOfLifeDialog):
        if not ConwaysGameOfLifeDialog.objectName():
            ConwaysGameOfLifeDialog.setObjectName(u"ConwaysGameOfLifeDialog")
        ConwaysGameOfLifeDialog.resize(342, 372)
        self.verticalLayout_2 = QVBoxLayout(ConwaysGameOfLifeDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.conways_game_of_life_widget = ConwaysGameOfLife(ConwaysGameOfLifeDialog)
        self.conways_game_of_life_widget.setObjectName(u"conways_game_of_life_widget")

        self.verticalLayout.addWidget(self.conways_game_of_life_widget)

        self.button_box = QDialogButtonBox(ConwaysGameOfLifeDialog)
        self.button_box.setObjectName(u"button_box")
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.button_box)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(ConwaysGameOfLifeDialog)
    # setupUi

    def retranslateUi(self, ConwaysGameOfLifeDialog):
        ConwaysGameOfLifeDialog.setWindowTitle(QCoreApplication.translate("ConwaysGameOfLifeDialog", u"ConwaysGameOfLifeDialog", None))
    # retranslateUi

