import pathlib


class PathManager:
    """
    Class for managing the paths of the project.
    """
    PROJECT_ROOT: pathlib.Path
    CONFIGS_DIR: pathlib.Path
    EXPORTS_DIR: pathlib.Path
    PATTERN_GALLERY_DIR: pathlib.Path
    ASSETS_DIR: pathlib.Path
    SETTINGS_INI: pathlib.Path

    @classmethod
    def set_project_root(cls, path: pathlib.Path):
        cls.PROJECT_ROOT = path
        cls.CONFIGS_DIR = cls.PROJECT_ROOT / "configs"
        cls.EXPORTS_DIR = cls.PROJECT_ROOT / "exports"
        cls.ASSETS_DIR = cls.PROJECT_ROOT / "assets"
        cls.SETTINGS_INI = cls.PROJECT_ROOT / "settings.ini"
        cls.PATTERN_GALLERY_DIR = cls.PROJECT_ROOT / "pattern_gallery"
