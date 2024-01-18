# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InstructionsDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_InstructionsDialog(object):
    def setupUi(self, InstructionsDialog):
        if not InstructionsDialog.objectName():
            InstructionsDialog.setObjectName(u"InstructionsDialog")
        InstructionsDialog.resize(284, 206)
        InstructionsDialog.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(210, 210, 210);\n"
"}\n"
"QLabel {\n"
"	margin-top: 0.4em;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(212, 212, 212);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(188, 188, 188);\n"
"}\n"
"")
        InstructionsDialog.setModal(True)
        self.verticalLayout_2 = QVBoxLayout(InstructionsDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 10, -1, -1)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(InstructionsDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label.setMargin(0)

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(InstructionsDialog)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(9)
        self.label_2.setFont(font1)
        self.label_2.setMargin(0)

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(InstructionsDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setMargin(0)

        self.verticalLayout.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.close_button = QPushButton(InstructionsDialog)
        self.close_button.setObjectName(u"close_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.close_button.sizePolicy().hasHeightForWidth())
        self.close_button.setSizePolicy(sizePolicy)
        self.close_button.setMaximumSize(QSize(30, 16777215))
        self.close_button.setFont(font1)

        self.gridLayout.addWidget(self.close_button, 0, 1, 1, 1, Qt.AlignTop)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.retranslateUi(InstructionsDialog)
    # setupUi

    def retranslateUi(self, InstructionsDialog):
        InstructionsDialog.setWindowTitle(QCoreApplication.translate("InstructionsDialog", u"InstructionsDialog", None))
        self.label.setText(QCoreApplication.translate("InstructionsDialog", u"Instructions", None))
        self.label_2.setText(QCoreApplication.translate("InstructionsDialog", u"\u2022 To change the cell state to the opposite,\n"
" press 'Enter' key or click the cell with \n"
"the left mouse button.", None))
        self.label_3.setText(QCoreApplication.translate("InstructionsDialog", u"\u2022 Use arrow keys on the keyboard\n"
"to change the current active cell position", None))
        self.close_button.setText(QCoreApplication.translate("InstructionsDialog", u"X", None))
    # retranslateUi

