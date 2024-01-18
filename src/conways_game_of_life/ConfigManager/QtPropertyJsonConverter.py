from PySide6.QtGui import QColor


def deserialize_property(obj):
    if isinstance(obj, dict) and '__qcolor__' in obj:
        rgba = obj['rgba']
        return QColor(*rgba)
    return obj


def serialize_property(obj):
    if isinstance(obj, QColor):
        return {
            '__qcolor__': True,
            'rgba': (obj.red(), obj.green(), obj.blue(), obj.alpha())
        }
    return obj
