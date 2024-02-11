from PySide6.QtCore import QLineF
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsLineItem


class BorderItem(QGraphicsLineItem):
    """
    A QGraphicsLineItem for displaying it as an overlay representing the borders of the game.

    Receives information from the Scene via setters.
    """

    def __init__(self, line: QLineF, *, color: QColor, thickness: int):
        super().__init__(line)
        self.setZValue(1)

        self.set_color(color)
        self.set_thickness(thickness)

    def set_color(self, value: QColor):
        self.pen().setColor(value)

    def set_thickness(self, value: int):
        self.pen().setWidth(value)

    # def paint(self, painter, option, widget=None):
    #     pen = self.pen()
    #     pen.setColor(self._color)
    #     pen.setWidth(self._thickness)
    #     super().paint(painter, option, widget)
