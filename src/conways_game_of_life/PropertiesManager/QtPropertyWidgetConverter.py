from types import MappingProxyType

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QSpinBox


class QtPropertyWidgetConverter:
    @staticmethod
    def _convert_label_to_color(label: QLabel) -> QColor:
        return label.palette().color(label.backgroundRole())

    @staticmethod
    def _convert_spin_box_to_int(spin_box: QSpinBox) -> int:
        return int(spin_box.value())

    @classmethod
    def convert_widget_value(cls, *, property_name: str, widget):
        if property_name not in cls.WIDGETS:
            return None

        return cls.WIDGETS[property_name](widget)

    WIDGETS = MappingProxyType({
        "cols": _convert_spin_box_to_int,
        "rows": _convert_spin_box_to_int,
        "turn_duration": _convert_spin_box_to_int,
        "border_thickness": _convert_spin_box_to_int,
        "border_color": _convert_label_to_color,
        "cell_dead_color": _convert_label_to_color,
        "cell_alive_color": _convert_label_to_color
    })
