import json
import os
import pathlib
from contextlib import contextmanager
from json import JSONDecodeError
from typing import ContextManager

from PySide6.QtCore import QRunnable, QObject, Signal, Slot, Qt, QRectF
from PySide6.QtGui import QPainter, QPixmap
from jsonschema import validators
from jsonschema.exceptions import ValidationError

from backend import PathManager
from conways_game_of_life.core import GameView, GameEngine, GameScene
from conways_game_of_life.core.static_types import PatternSchema

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


@contextmanager
def _temp_game_context() -> ContextManager[tuple[GameEngine, GameScene, GameView]]:
    game_engine = GameEngine()
    game_scene = GameScene(game_engine)
    game_view = GameView()
    game_view.setScene(game_scene)
    try:
        yield game_engine, game_scene, game_view
    finally:
        del game_view
        del game_scene
        del game_engine


class PatternsDataLoader(QRunnable):
    """
    QRunnable that processes the JSON pattern data according to defined schema.

    Responsible for retrieving JSON files in a directory,
    validating, and rendering them on the game widget to generate QPixmap for each pattern.
    Emits the 'finished' and 'data_generated' Signals when it has done the job.
    """

    def __init__(self):
        super().__init__()

        self.json_file_paths: list[pathlib.Path] = []
        self.result_data: list[tuple[PatternSchema, QPixmap]] = []
        # QRunnable cannot have signals, so doing that
        self.signals = _PatternDataLoaderSignals()

    def run(self):
        self.load_file_paths()
        for file_path in self.json_file_paths:
            try:
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    validators.validate(data, pattern_json_schema)
                    parsed_data: PatternSchema = data  # Type casting handled by json schema
                    if self.validate_data_on_widget(parsed_data):
                        self.result_data.append((parsed_data, self.generate_pixmap(parsed_data)))
            except (JSONDecodeError, ValidationError):
                continue

        self.signals.finished.emit()
        self.signals.data_generated.emit(self.result_data)

    @staticmethod
    def validate_data_on_widget(parsed_data: PatternSchema) -> bool:
        is_valid = True

        @Slot(str, str)
        def _error_catch_slot(*args: str):
            nonlocal is_valid
            is_valid = False

        with _temp_game_context() as game_components:
            engine, scene, view = game_components
            engine.property_setter_error_signal.connect(_error_catch_slot)
            engine.setProperty('rows', parsed_data["rows"])
            engine.setProperty('cols', parsed_data["cols"])
            engine.setProperty('state', parsed_data["state"])
            engine.property_setter_error_signal.disconnect(_error_catch_slot)
        return is_valid

    @staticmethod
    def generate_pixmap(parsed_data: PatternSchema) -> QPixmap:
        """
        Renders Scene on the QPixMap.
        Return QPixMap with target width 32 and the same aspect ratio as the Scene.
        """
        with _temp_game_context() as game_components:
            engine, scene, view = game_components
            engine.setProperty('rows', parsed_data["rows"])
            engine.setProperty('cols', parsed_data["cols"])
            engine.setProperty('state', parsed_data["state"])
            scene.setProperty('border_thickness', 0)

            target_width = 32
            original_rect = scene.sceneRect()
            original_width = original_rect.width()
            original_height = original_rect.height()
            aspect_ratio = original_width / original_height
            target_height = int(target_width / aspect_ratio)

            pixmap = QPixmap(target_width, target_height)
            pixmap.fill(Qt.transparent)

            with QPainter(pixmap) as painter:
                scene.render(painter, QRectF(pixmap.rect()))
            return pixmap

    def load_file_paths(self):
        json_file_paths = []
        with os.scandir(PathManager.PATTERN_GALLERY_DIR) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith(".json"):
                    json_file_paths.append(pathlib.Path(entry.path))

        self.json_file_paths = json_file_paths


class _PatternDataLoaderSignals(QObject):
    finished = Signal()
    data_generated = Signal(list)  # List of (dict, QPixmap)
