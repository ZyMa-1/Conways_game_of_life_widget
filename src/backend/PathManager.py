"""
Author: ZyMa-1
"""

import os
import pathlib


class PathManager:
    PROJECT_ROOT = None
    CONFIGS_DIR = None
    EXPORTS_DIR = None
    SETTINGS_INI = None

    @classmethod
    def set_project_root(cls, path: pathlib.Path):
        cls.PROJECT_ROOT = path
        cls.CONFIGS_DIR = cls.PROJECT_ROOT / "configs"
        cls.EXPORTS_DIR = cls.PROJECT_ROOT / "exports"
        cls.SETTINGS_INI = cls.PROJECT_ROOT / "settings.ini"
