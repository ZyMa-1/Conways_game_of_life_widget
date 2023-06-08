"""
Author: ZyMa-1
"""

import os
import pathlib


class PathManager:
    try:
        PROJECT_ROOT = pathlib.Path(os.getenv('PROJECT_ROOT'))
    except TypeError:
        PROJECT_ROOT = None

    @classmethod
    def get_project_root(cls):
        if cls.PROJECT_ROOT is None:
            raise FileNotFoundError
        return cls.PROJECT_ROOT
