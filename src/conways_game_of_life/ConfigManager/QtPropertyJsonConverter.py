from PySide6.QtGui import QColor


class QtPropertyJsonConverter:
    @staticmethod
    def to_property_type(value):
        if (isinstance(value, list) or isinstance(value, tuple)) and len(value) == 3:
            value = QColor(value[0], value[1], value[2])

        return value

    @staticmethod
    def to_json_type(value):
        if isinstance(value, QColor):
            value = (value.red(), value.green(), value.blue())

        return value
