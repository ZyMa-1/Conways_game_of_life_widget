from enum import IntEnum


class CellEditMode(IntEnum):
    """
    Enum representing different edit modes user can perform on the cell.
    """
    DEFAULT = 0
    PAINT = 1
    ERASE = 2


class SceneCellType(IntEnum):
    """
    Enum representing various cell types within the Scene.
    """
    ALIVE = 0
    DEAD = 1
    ACTIVE = 2
