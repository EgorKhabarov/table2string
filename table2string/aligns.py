from enum import Enum


ALLOWED_H_ALIGNS = [
    "<",
    "^",
    ">",
    "<<",
    "<^",
    "<>",
    "^<",
    "^^",
    "^>",
    "><",
    ">^",
    ">>",
    "*",
    "**",
]
ALLOWED_V_ALIGNS = [
    "^",
    "-",
    "_",
]


class HorizontalAlignment(Enum):
    LEFT = "<"
    CENTER = "^"
    RIGHT = ">"
    LEFT_LEFT = "<<"
    LEFT_CENTER = "<^"
    LEFT_RIGHT = "<>"
    CENTER_LEFT = "^<"
    CENTER_CENTER = "^^"
    CENTER_RIGHT = "^>"
    RIGHT_LEFT = "><"
    RIGHT_CENTER = ">^"
    RIGHT_RIGHT = ">>"
    AUTO = "*"
    AUTO_AUTO = "**"


class VerticalAlignment(Enum):
    TOP = "^"
    MIDDLE = "-"
    BOTTOM = "_"
