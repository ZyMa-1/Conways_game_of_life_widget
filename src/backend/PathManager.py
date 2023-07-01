"""
Author: ZyMa-1
"""

import pathlib


class PathManager:
    """Class for storing paths."""
    PROJECT_ROOT = None
    CONFIGS_DIR = None
    EXPORTS_DIR = None
    PATTERN_GALLERY_DIR = None
    SETTINGS_INI = None

    @classmethod
    def set_project_root(cls, path: pathlib.Path):
        cls.PROJECT_ROOT = path
        cls.CONFIGS_DIR = cls.PROJECT_ROOT / "configs"
        cls.EXPORTS_DIR = cls.PROJECT_ROOT / "exports"
        cls.SETTINGS_INI = cls.PROJECT_ROOT / "settings.ini"
        cls.PATTERN_GALLERY_DIR = cls.PROJECT_ROOT / "pattern_gallery"
