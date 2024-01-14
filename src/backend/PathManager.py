import os
import pathlib


class PathManager:
    PROJECT_ROOT: pathlib.Path
    CONFIGS_DIR: pathlib.Path
    EXPORTS_DIR: pathlib.Path
    PATTERN_GALLERY_DIR: pathlib.Path
    SETTINGS_INI: pathlib.Path

    @classmethod
    def set_project_root(cls, path: pathlib.Path):
        cls.PROJECT_ROOT = path
        cls.CONFIGS_DIR = cls.PROJECT_ROOT / "configs"
        cls.EXPORTS_DIR = cls.PROJECT_ROOT / "exports"
        cls.SETTINGS_INI = cls.PROJECT_ROOT / "settings.ini"
        cls.PATTERN_GALLERY_DIR = cls.PROJECT_ROOT / "pattern_gallery"

    @classmethod
    def create_files(cls):
        if not os.path.exists(cls.SETTINGS_INI):
            with open(cls.SETTINGS_INI, 'w') as f:
                f.write('[General]\nLanguage=en')
        with open(cls.PATTERN_GALLERY_DIR / "square.json", 'w') as f:
            f.write(
                """{
                "rows": 5,
                "cols": 5,
                "state": [["*","*","*","*","*"],
                ["*",".",".",".","*"],
                ["*",".",".",".","*"],
                ["*",".",".",".","*"],
                ["*","*","*","*","*"]],
                "pattern_name": "Square"
                }""")
