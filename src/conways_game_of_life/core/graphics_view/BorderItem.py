from PySide6.QtCore import QLineF
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsLineItem


class BorderItem(QGraphicsLineItem):
    """
    A QGraphicsLineItem for displaying it as an overlay representing the borders of the game.

    Receives information from the Scene via setters.
    """

    def __init__(self, line: QLineF, *, color: QColor, thickness_percentage: float, scene_width: float):
        super().__init__(line)
        self.setZValue(1)
        self.setAcceptDrops(False)  # Disables automatic mouse events handling

        self.set_color(color)
        self.set_thickness_percentage(thickness_percentage, scene_width=scene_width)

    def set_color(self, value: QColor):
        pen = self.pen()
        pen.setColor(value)
        self.setPen(pen)

    def set_thickness_percentage(self, value: float, *, scene_width: float):
        pen = self.pen()
        true_value = scene_width / 100 * value
        pen.setWidthF(true_value)
        self.setPen(pen)
