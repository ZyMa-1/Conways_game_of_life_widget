from typing import TypedDict


class PatternSchema(TypedDict):
    rows: int
    cols: int
    state: list[list[str]]
    pattern_name: str
