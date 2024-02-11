from abc import ABCMeta

from PySide6.QtCore import QObject


class QAbcMeta(type(QObject), ABCMeta):
    """
    Metaclass for classes that inherit from Qt and ABC classes.

    Type of QObject, QWidget, QPushButton, QGraphicsScene is essentially the same in PySide6:
    <class 'Shiboken.ObjectType'>
    """
    pass
