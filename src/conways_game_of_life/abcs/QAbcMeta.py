from abc import ABCMeta

from PySide6.QtCore import QObject


class QAbcMeta(type(QObject), ABCMeta):
    pass
