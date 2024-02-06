from json import JSONDecoder, JSONEncoder

from PySide6.QtGui import QColor


class ConfigDecoder(JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=ConfigDecoder.from_dict)

    @staticmethod
    def from_dict(d):
        if d.get("__class__") == "QColor":
            rgba = d['rgba']
            return QColor(*rgba)
        return d


class ConfigEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QColor):
            return {
                '__class__': "QColor",
                'rgba': o.getRgb()
            }
        return super().default(o)
