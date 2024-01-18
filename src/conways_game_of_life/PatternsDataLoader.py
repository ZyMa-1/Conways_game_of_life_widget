import json
import os
import pathlib
from json import JSONDecodeError

from PySide6.QtCore import QRunnable, QObject, Signal, Slot, Qt, QRect, QPoint
from PySide6.QtGui import QPainter, QPixmap
from jsonschema import validators
from jsonschema.exceptions import ValidationError

from src.backend.PathManager import PathManager
from src.conways_game_of_life.ConwaysGameOfLife import ConwaysGameOfLife

pattern_json_schema = {
    "type": "object",
    "properties": {
        "rows": {"type": "integer"},
        "cols": {"type": "integer"},
        "state": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "pattern_name": {"type": "string"}
    },
    "required": ["rows", "cols", "state", "pattern_name"]
}


class PatternsDataLoader(QRunnable):
    def __init__(self):
        super().__init__()

        self.json_file_paths = []
        self.result_data = []
        # QRunnable cannot have signals, so doing that
        self.signals = _PatternDataLoaderSignals()

    def run(self):
        self.load_file_paths()
        for file_path in self.json_file_paths:
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
            except JSONDecodeError:
                continue
            if not self.validate_json_data(data):
                continue
            parsed_data = self.parse_data(data)
            if not self.validate_data_on_widget(parsed_data):
                continue

            self.result_data.append((parsed_data, self.generate_pixmap(parsed_data)))

        self.signals.finished.emit()
        self.signals.data_generated.emit(self.result_data)

    @staticmethod
    def validate_data_on_widget(parsed_data: dict) -> bool:
        is_valid = True

        @Slot(str, str)
        def _error_catch_slot(*args: str):
            nonlocal is_valid
            is_valid = False

        game_widget = ConwaysGameOfLife()
        game_widget.property_setter_error_signal.connect(_error_catch_slot)
        game_widget.setProperty('rows', parsed_data["rows"])
        game_widget.setProperty('cols', parsed_data["cols"])
        game_widget.setProperty('state', parsed_data["state"])
        game_widget.property_setter_error_signal.disconnect(_error_catch_slot)
        del game_widget

        return is_valid

    @staticmethod
    def generate_pixmap(parsed_data: dict) -> QPixmap:
        game_widget = ConwaysGameOfLife()
        game_widget._active_cell = (-1, -1)
        game_widget.setProperty('rows', parsed_data["rows"])
        game_widget.setProperty('cols', parsed_data["cols"])
        game_widget.setProperty('state', parsed_data["state"])

        pixmap = QPixmap(game_widget.size())

        with QPainter(pixmap) as painter:
            game_widget.render(painter, QPoint(0, 0), QRect(QPoint(0, 0), game_widget.size()))

            result_width = 32
            aspect_ratio = pixmap.width() / pixmap.height()
            result_height = int(result_width / aspect_ratio)
            resized_pixmap = pixmap.scaled(result_width, result_height, Qt.AspectRatioMode.KeepAspectRatio)

            del game_widget
            return resized_pixmap

    @staticmethod
    def parse_data(data: dict) -> dict:
        """Type casting can be handled entirely by json schema"""
        # return {"rows": int(data["rows"]),
        #         "cols": int(data["cols"]),
        #         "state": data["state"],
        #         "pattern_name": str(data["pattern_name"])}
        return data

    @staticmethod
    def validate_json_data(data: dict) -> bool:
        try:
            validators.validate(data, pattern_json_schema)
            return True
        except ValidationError:
            return False

    def load_file_paths(self):
        json_file_paths = []
        with os.scandir(PathManager.PATTERN_GALLERY_DIR) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(".json"):
                    json_file_paths.append(pathlib.Path(entry.path))

        self.json_file_paths.extend(json_file_paths)


class _PatternDataLoaderSignals(QObject):
    finished = Signal()
    data_generated = Signal(list)  # List of (dict, QPixmap)
