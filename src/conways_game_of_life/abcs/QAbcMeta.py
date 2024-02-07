from abc import ABCMeta

from PySide6.QtCore import QObject


class QAbcMeta(type(QObject), ABCMeta):
    """
    Metaclass for classes inherited from Qt-classes and Abc classes.
    Type of QObject, QWidget, QPushButton is essentially the same in PySide6:
    <class 'Shiboken.ObjectType'>
    """
    pass
