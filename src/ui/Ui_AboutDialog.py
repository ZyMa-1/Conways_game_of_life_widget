# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AboutDialog.ui'
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
    QGridLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 187)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.app_name_label = QLabel(Dialog)
        self.app_name_label.setObjectName(u"app_name_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.app_name_label.sizePolicy().hasHeightForWidth())
        self.app_name_label.setSizePolicy(sizePolicy)
        self.app_name_label.setMinimumSize(QSize(300, 0))
        font = QFont()
        font.setPointSize(14)
        self.app_name_label.setFont(font)
        self.app_name_label.setStyleSheet(u"margin-top: 0.5em;")
        self.app_name_label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.verticalLayout_2.addWidget(self.app_name_label, 0, Qt.AlignTop)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.author_name_label = QLabel(Dialog)
        self.author_name_label.setObjectName(u"author_name_label")
        self.author_name_label.setStyleSheet(u"")
        self.author_name_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.author_name_label, 0, 1, 1, 1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setStyleSheet(u"")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.docs_link_label = QLabel(Dialog)
        self.docs_link_label.setObjectName(u"docs_link_label")

        self.gridLayout.addWidget(self.docs_link_label, 2, 1, 1, 1)

        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.app_version_label = QLabel(Dialog)
        self.app_version_label.setObjectName(u"app_version_label")

        self.gridLayout.addWidget(self.app_version_label, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"About", None))
        self.app_name_label.setText(QCoreApplication.translate("Dialog", u"{app_name}", None))
        self.author_name_label.setText(QCoreApplication.translate("Dialog", u"{author_name}", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Documentation: ", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Author:", None))
        self.docs_link_label.setText(QCoreApplication.translate("Dialog", u"{docs_link}", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"App version:", None))
        self.app_version_label.setText(QCoreApplication.translate("Dialog", u"{app_version}", None))
    # retranslateUi

