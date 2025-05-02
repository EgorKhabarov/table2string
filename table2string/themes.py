from typing import Optional
from functools import lru_cache
from dataclasses import dataclass


BORDER_EXAMPLE_SYMBOLS: dict[str, tuple[str, ...]] = {
    "horizontal": (
        "─",
        "━",
        "┄",
        "┅",
        "┈",
        "┉",
        "╌",
        "╍",
        "═",
        "╴",
        "╶",
        "╸",
        "╺",
        "╼",
        "╾",
    ),
    "vertical": (
        "│",
        "┃",
        "┆",
        "┇",
        "┊",
        "┋",
        "╎",
        "╏",
        "║",
        "╵",
        "╷",
        "╹",
        "╻",
        "╽",
        "╿",
        "‖",
    ),
    "top_left": ("┌", "┍", "┎", "┏", "╒", "╓", "╔", "╭"),
    "top_right": ("┐", "┑", "┒", "┓", "╕", "╖", "╗", "╮"),
    "bottom_left": ("└", "┕", "┖", "┗", "╘", "╙", "╚", "╰"),
    "bottom_right": ("┘", "┙", "┚", "┛", "╛", "╜", "╝", "╯"),
    "vertical_left": ("├", "┝", "┞", "┟", "┠", "┡", "┢", "┣", "╞", "╟", "╠"),
    "vertical_right": ("┤", "┥", "┦", "┧", "┨", "┩", "┪", "┫", "╡", "╢", "╣"),
    "top_horizontal": ("┬", "┭", "┮", "┯", "┰", "┱", "┲", "┳", "╤", "╥", "╦"),
    "bottom_horizontal": ("┴", "┵", "┶", "┷", "┸", "┹", "┺", "┻", "╧", "╨", "╩"),
    "central": (
        "┼",
        "┽",
        "┾",
        "┿",
        "╀",
        "╁",
        "╂",
        "╃",
        "╄",
        "╅",
        "╆",
        "╇",
        "╈",
        "╉",
        "╊",
        "╋",
        "╪",
        "╫",
        "╬",
    ),
}
"""
┌───────┐ ┏━━━━━━━┓ ╔═══════╗ ╭───────╮ ┏━━━╾───┐ ┍━━━━━━━┑ ┎───────┒ ╒═══════╕ ╓───────╖
│       │ ┃       ┃ ║       ║ │       │ ┃       │ │       │ ┃       ┃ │       │ ║       ║
│       │ ┃       ┃ ║       ║ │       │ ╿       ╽ │       │ ┃       ┃ │       │ ║       ║
│       │ ┃       ┃ ║       ║ │       │ │       ┃ │       │ ┃       ┃ │       │ ║       ║
└───────┘ ┗━━━━━━━┛ ╚═══════╝ ╰───────╯ └───╼━━━┛ ┕━━━━━━━┙ ┖───────┚ ╘═══════╛ ╙───────╜
┌╌╌╌╌╌╌╌┐ ┏╍╍╍╍╍╍╍┓ ┌┄┄┄┄┄┄┄┐ ┏┅┅┅┅┅┅┅┓ ┌┈┈┈┈┈┈┈┐ ┏┉┉┉┉┉┉┉┓ ┌──╴ ╶──┐ ┏━━╸ ╺━━┓
╎       ╎ ╏       ╏ ┆       ┆ ┇       ┇ ┊       ┊ ┋       ┋ ╷       ╷ ╹       ╹
╎       ╎ ╏       ╏ ┆       ┆ ┇       ┇ ┊       ┊ ┋       ┋
╎       ╎ ╏       ╏ ┆       ┆ ┇       ┇ ┊       ┊ ┋       ┋ ╵       ╵ ╻       ╻
└╌╌╌╌╌╌╌┘ ┗╍╍╍╍╍╍╍┛ └┄┄┄┄┄┄┄┘ ┗┅┅┅┅┅┅┅┛ └┈┈┈┈┈┈┈┘ ┗┉┉┉┉┉┉┉┛ └──╴ ╶──┘ ┗━━╸ ╺━━┛
┌───┬───┐ ┏━━━┳━━━┓ ┌───┬───┐ ┌───┰───┐ ┏━━━┳━━━┓ ┏━━━┯━━━┓
│   │   │ ┃   ┃   ┃ │   │   │ │   ┃   │ ┃   ┃   ┃ ┃   │   ┃
├───┼───┤ ┣━━━╋━━━┫ ┝━━━┿━━━┥ ├───╂───┤ ┠───╂───┨ ┣━━━┿━━━┫
│   │   │ ┃   ┃   ┃ │   │   │ │   ┃   │ ┃   ┃   ┃ ┃   │   ┃
└───┴───┘ ┗━━━┻━━━┛ └───┴───┘ └───┸───┘ ┗━━━┻━━━┛ ┗━━━┷━━━┛
╔═══╦═══╗ ╔═══╦═══╗ ╔═══╤═══╗ ┌───┬───┐ ┌───╥───┐
║   ║   ║ ║   ║   ║ ║   │   ║ │   │   │ │   ║   │
╠═══╬═══╣ ╟───╫───╢ ╠═══╪═══╣ ╞═══╪═══╡ ├───╫───┤
║   ║   ║ ║   ║   ║ ║   │   ║ │   │   │ │   ║   │
╚═══╩═══╝ ╚═══╩═══╝ ╚═══╧═══╝ └───┴───┘ └───╨───┘
┏━━━┳━━━┓ ┏━━━┱───┐ ┌───┬───┐ ┌───┲━━━┓ ┏━━━┳━━━┓ ┏━━━┭───┐
┃   ┃   ┃ ┃   ┃   │ │   │   │ │   ┃   ┃ ┃   ┃   ┃ ┃   │   │
┡━━━╇━━━┩ ┣━━━╉───┤ ┢━━━╈━━━┪ ├───╊━━━┫ ┞───╀───┦ ┣━━━┽───┤
│   │   │ ┃   ┃   │ ┃   ┃   ┃ │   ┃   ┃ │   │   │ ┃   │   │
└───┴───┘ ┗━━━┹───┘ ┗━━━┻━━━┛ └───┺━━━┛ └───┴───┘ ┗━━━┵───┘
┌───┬───┐ ┌───┮━━━┓ ┌───┲━━━┓ ┏━━━┱───┐ ┌───┬───┐ ┌───┬───┐
│   │   │ │   │   ┃ │   ┃   ┃ ┃   ┃   │ │   │   │ │   │   │
┟───╁───┧ ├───┾━━━┫ ├───╄━━━┩ ┡━━━╃───┤ ┢━━━╅───┤ ├───╆━━━┪
┃   ┃   ┃ │   │   ┃ │   │   │ │   │   │ ┃   ┃   │ │   ┃   ┃
┗━━━┻━━━┛ └───┶━━━┛ └───┴───┘ └───┴───┘ ┗━━━┹───┘ └───┺━━━┛
note: not all of these borders can be used in table2string
"""


@dataclass
class Border:
    horizontal: str
    vertical: str
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    vertical_left: str
    vertical_right: str
    top_horizontal: str
    bottom_horizontal: str
    central: str
    vertical_left_plus: str
    horizontal_plus: str
    central_plus: str
    vertical_right_plus: str
    top_horizontal_plus: str
    bottom_horizontal_plus: str

    def get_border_name(self, border: str) -> str | None:
        if border == self.horizontal:
            return "horizontal"
        elif border == self.vertical:
            return "vertical"
        elif border == self.central:
            return "central"
        # elif border == self.top_left:
        #     return "top_left"
        # elif border == self.top_right:
        #     return "top_right"
        # elif border == self.bottom_left:
        #     return "bottom_left"
        # elif border == self.bottom_right:
        #     return "bottom_right"
        elif border == self.vertical_left:
            return "vertical_left"
        elif border == self.vertical_right:
            return "vertical_right"
        elif border == self.top_horizontal:
            return "top_horizontal"
        elif border == self.bottom_horizontal:
            return "bottom_horizontal"
        # elif border == self.vertical_left_plus:
        #     return "vertical_left_plus"
        elif border == self.horizontal_plus:
            return "horizontal_plus"
        # elif border == self.central_plus:
        #     return "central_plus"
        # elif border == self.vertical_right_plus:
        #     return "vertical_right_plus"
        # elif border == self.top_horizontal_plus:
        #     return "top_horizontal_plus"
        # elif border == self.bottom_horizontal_plus:
        #     return "bottom_horizontal_plus"

        return None


class Theme:
    def __init__(
        self,
        name: str,
        border: Border,
        custom_sub_table_theme: Optional["Theme"] = None,
    ):
        self.name = name
        self.border = border
        self.custom_sub_table_theme = custom_sub_table_theme or self

    def __repr__(self):
        if self.name in (
            "ascii_thin",
            "ascii_thin_double",
            "ascii_double",
            "ascii_double_thin",
            "thin",
            "thin_thick",
            "thin_double",
            "rounded_double",
            "rounded",
            "rounded_thick",
            "thick",
            "thick_thin",
            "double",
            "double_thin",
            "booktabs",
            "ascii_booktabs",
            "markdown",
        ):
            return f"Themes.{self.name}"
        else:
            return f"Theme({self.name!r}, {self.border!r}, {self.custom_sub_table_theme!r})"


class Themes:
    @classmethod
    def get(cls, theme: str, default_theme: Theme | None = None) -> Theme:
        if theme == "get":
            return default_theme or Themes.ascii_thin
        return getattr(cls, theme, default_theme or Themes.ascii_thin)

    ascii_thin: Theme = Theme(
        name="ascii_thin",
        border=Border(
            horizontal="-",
            vertical="|",
            top_left="+",
            top_right="+",
            bottom_left="+",
            bottom_right="+",
            vertical_left="+",
            vertical_right="+",
            top_horizontal="+",
            bottom_horizontal="+",
            central="+",
            vertical_left_plus="+",
            horizontal_plus="-",
            central_plus="+",
            vertical_right_plus="+",
            top_horizontal_plus="+",
            bottom_horizontal_plus="+",
        ),
    )
    ascii_thin_double: Theme = Theme(
        name="ascii_thin_double",
        border=Border(
            horizontal="-",
            vertical="|",
            top_left="+",
            top_right="+",
            bottom_left="+",
            bottom_right="+",
            vertical_left="+",
            vertical_right="+",
            top_horizontal="+",
            bottom_horizontal="+",
            central="+",
            vertical_left_plus="+",
            horizontal_plus="=",
            central_plus="+",
            vertical_right_plus="+",
            top_horizontal_plus="+",
            bottom_horizontal_plus="+",
        ),
        custom_sub_table_theme=ascii_thin,
    )
    ascii_double: Theme = Theme(
        name="ascii_double",
        border=Border(
            horizontal="=",
            vertical="‖",
            top_left="+",
            top_right="+",
            bottom_left="+",
            bottom_right="+",
            vertical_left="+",
            vertical_right="+",
            top_horizontal="+",
            bottom_horizontal="+",
            central="+",
            vertical_left_plus="+",
            horizontal_plus="=",
            central_plus="+",
            vertical_right_plus="+",
            top_horizontal_plus="+",
            bottom_horizontal_plus="+",
        ),
    )
    ascii_double_thin: Theme = Theme(
        name="ascii_double_thin",
        border=Border(
            horizontal="=",
            vertical="‖",
            top_left="+",
            top_right="+",
            bottom_left="+",
            bottom_right="+",
            vertical_left="+",
            vertical_right="+",
            top_horizontal="+",
            bottom_horizontal="+",
            central="+",
            vertical_left_plus="+",
            horizontal_plus="-",
            central_plus="+",
            vertical_right_plus="+",
            top_horizontal_plus="-",
            bottom_horizontal_plus="-",
        ),
        custom_sub_table_theme=ascii_double,
    )
    ascii_booktabs: Theme = Theme(
        name="ascii_booktabs",
        border=Border(
            horizontal="-",
            vertical=" ",
            top_left=" ",
            top_right=" ",
            bottom_left=" ",
            bottom_right=" ",
            vertical_left=" ",
            vertical_right=" ",
            top_horizontal="-",
            bottom_horizontal="-",
            central="-",
            vertical_left_plus=" ",
            horizontal_plus="=",
            central_plus="=",
            vertical_right_plus=" ",
            top_horizontal_plus=" ",
            bottom_horizontal_plus=" ",
        ),
    )
    thin: Theme = Theme(
        name="thin",
        border=Border(
            horizontal="─",
            vertical="│",
            top_left="┌",
            top_right="┐",
            bottom_left="└",
            bottom_right="┘",
            vertical_left="├",
            vertical_right="┤",
            top_horizontal="┬",
            bottom_horizontal="┴",
            central="┼",
            vertical_left_plus="├",
            horizontal_plus="─",
            central_plus="┼",
            vertical_right_plus="┤",
            top_horizontal_plus="┬",
            bottom_horizontal_plus="┴",
        ),
    )
    thin_thick: Theme = Theme(
        name="thin_thick",
        border=Border(
            horizontal="─",
            vertical="│",
            top_left="┌",
            top_right="┐",
            bottom_left="└",
            bottom_right="┘",
            vertical_left="├",
            vertical_right="┤",
            top_horizontal="┬",
            bottom_horizontal="┴",
            central="┼",
            vertical_left_plus="┝",
            horizontal_plus="━",
            central_plus="┿",
            vertical_right_plus="┥",
            top_horizontal_plus="┯",
            bottom_horizontal_plus="┷",
        ),
        custom_sub_table_theme=thin,
    )
    thin_double: Theme = Theme(
        name="thin_double",
        border=Border(
            horizontal="─",
            vertical="│",
            top_left="┌",
            top_right="┐",
            bottom_left="└",
            bottom_right="┘",
            vertical_left="├",
            vertical_right="┤",
            top_horizontal="┬",
            bottom_horizontal="┴",
            central="┼",
            vertical_left_plus="╞",
            horizontal_plus="═",
            central_plus="╪",
            vertical_right_plus="╡",
            top_horizontal_plus="╤",
            bottom_horizontal_plus="╧",
        ),
        custom_sub_table_theme=thin,
    )
    rounded: Theme = Theme(
        name="rounded",
        border=Border(
            horizontal="─",
            vertical="│",
            top_left="╭",
            top_right="╮",
            bottom_left="╰",
            bottom_right="╯",
            vertical_left="├",
            vertical_right="┤",
            top_horizontal="┬",
            bottom_horizontal="┴",
            central="┼",
            vertical_left_plus="├",
            horizontal_plus="─",
            central_plus="┼",
            vertical_right_plus="┤",
            top_horizontal_plus="┬",
            bottom_horizontal_plus="┴",
        ),
    )
    rounded_thick: Theme = Theme(
        name="rounded_thick",
        border=Border(
            horizontal="─",
            vertical="│",
            top_left="╭",
            top_right="╮",
            bottom_left="╰",
            bottom_right="╯",
            vertical_left="├",
            vertical_right="┤",
            top_horizontal="┬",
            bottom_horizontal="┴",
            central="┼",
            vertical_left_plus="┝",
            horizontal_plus="━",
            central_plus="┿",
            vertical_right_plus="┥",
            top_horizontal_plus="┯",
            bottom_horizontal_plus="┷",
        ),
        custom_sub_table_theme=thin,
    )
    rounded_double: Theme = Theme(
        name="rounded_double",
        border=Border(
            horizontal="─",
            vertical="│",
            top_left="╭",
            top_right="╮",
            bottom_left="╰",
            bottom_right="╯",
            vertical_left="├",
            vertical_right="┤",
            top_horizontal="┬",
            bottom_horizontal="┴",
            central="┼",
            vertical_left_plus="╞",
            horizontal_plus="═",
            central_plus="╪",
            vertical_right_plus="╡",
            top_horizontal_plus="╤",
            bottom_horizontal_plus="╧",
        ),
        custom_sub_table_theme=thin,
    )
    thick: Theme = Theme(
        name="thick",
        border=Border(
            horizontal="━",
            vertical="┃",
            top_left="┏",
            top_right="┓",
            bottom_left="┗",
            bottom_right="┛",
            vertical_left="┣",
            vertical_right="┫",
            top_horizontal="┳",
            bottom_horizontal="┻",
            central="╋",
            vertical_left_plus="┣",
            horizontal_plus="━",
            central_plus="╋",
            vertical_right_plus="┫",
            top_horizontal_plus="┳",
            bottom_horizontal_plus="┻",
        ),
    )
    thick_thin: Theme = Theme(
        name="thick_thin",
        border=Border(
            horizontal="━",
            vertical="┃",
            top_left="┏",
            top_right="┓",
            bottom_left="┗",
            bottom_right="┛",
            vertical_left="┣",
            vertical_right="┫",
            top_horizontal="┳",
            bottom_horizontal="┻",
            central="╋",
            vertical_left_plus="┠",
            horizontal_plus="─",
            central_plus="╂",
            vertical_right_plus="┨",
            top_horizontal_plus="┰",
            bottom_horizontal_plus="┸",
        ),
        custom_sub_table_theme=thick,
    )
    double: Theme = Theme(
        name="double",
        border=Border(
            horizontal="═",
            vertical="║",
            top_left="╔",
            top_right="╗",
            bottom_left="╚",
            bottom_right="╝",
            vertical_left="╠",
            vertical_right="╣",
            top_horizontal="╦",
            bottom_horizontal="╩",
            central="╬",
            vertical_left_plus="╠",
            horizontal_plus="═",
            central_plus="╬",
            vertical_right_plus="╣",
            top_horizontal_plus="╦",
            bottom_horizontal_plus="╩",
        ),
    )
    double_thin: Theme = Theme(
        name="double_thin",
        border=Border(
            horizontal="═",
            vertical="║",
            top_left="╔",
            top_right="╗",
            bottom_left="╚",
            bottom_right="╝",
            vertical_left="╠",
            vertical_right="╣",
            top_horizontal="╦",
            bottom_horizontal="╩",
            central="╬",
            vertical_left_plus="╟",
            horizontal_plus="─",
            central_plus="╫",
            vertical_right_plus="╢",
            top_horizontal_plus="╥",
            bottom_horizontal_plus="╨",
        ),
        custom_sub_table_theme=double,
    )
    booktabs: Theme = Theme(
        name="booktabs",
        border=Border(
            horizontal="─",
            vertical=" ",
            top_left=" ",
            top_right=" ",
            bottom_left=" ",
            bottom_right=" ",
            vertical_left=" ",
            vertical_right=" ",
            top_horizontal="─",
            bottom_horizontal="─",
            central="─",
            vertical_left_plus=" ",
            horizontal_plus="━",
            central_plus="━",
            vertical_right_plus=" ",
            top_horizontal_plus=" ",
            bottom_horizontal_plus=" ",
        ),
    )
    markdown: Theme = Theme(
        name="markdown",
        border=Border(
            horizontal=" ",
            vertical="|",
            top_left=" ",
            top_right=" ",
            bottom_left=" ",
            bottom_right=" ",
            vertical_left=" ",
            vertical_right=" ",
            top_horizontal=" ",
            bottom_horizontal=" ",
            central=" ",
            vertical_left_plus="|",
            horizontal_plus="-",
            central_plus="|",
            vertical_right_plus="|",
            top_horizontal_plus=" ",
            bottom_horizontal_plus=" ",
        ),
        custom_sub_table_theme=ascii_thin,
    )


translate_border_dict: dict[str, dict[tuple[str, str], str]] = {
    "border_left": {
        ("vertical", "vertical_left"): "vertical_left",
        ("vertical", "vertical_left_plus"): "vertical_left_plus",
        ("vertical_right", "vertical_left"): "central",
        ("vertical_right", "vertical_left_plus"): "central_plus",
        ("vertical", "central"): "vertical_left",
    },
    "border_right": {
        ("vertical", "vertical_right"): "vertical_right",
        ("vertical", "vertical_right_plus"): "vertical_right_plus",
        ("vertical_left", "vertical_right"): "central",
        ("vertical_left", "vertical_right_plus"): "central_plus",
        ("vertical", "central"): "vertical_right",
    },
    "border_top": {
        ("horizontal", "top_horizontal"): "top_horizontal",
        ("top_horizontal", "bottom_horizontal"): "central",
        ("bottom_horizontal", "top_horizontal"): "central",
        ("horizontal_plus", "top_horizontal"): "top_horizontal_plus",
        ("horizontal", "central"): "central",
        ("horizontal_plus", "central"): "central",
    },
    "border_bottom": {
        ("horizontal", "bottom_horizontal"): "bottom_horizontal",
        ("top_horizontal", "bottom_horizontal"): "central",
        ("bottom_horizontal", "top_horizontal"): "central",
        ("horizontal_plus", "bottom_horizontal"): "bottom_horizontal_plus",
        ("horizontal", "central"): "central",
        ("horizontal_plus", "central"): "central",
    },
}


@lru_cache(maxsize=100)
def translate_theme_border(
    side: str, theme: Theme, border_from: str, border_to: str
) -> str:
    """
    Used to connect table boundaries to a subtable

    :param side: "border_left" or "border_right" or "border_top" or "border_bottom"
    :param theme: Theme
    :param border_from: The border to be connected to border_to
    :param border_to: The border to be attached
    :return: Connected borders (if possible)
    """
    border_from_name: str = theme.border.get_border_name(border_from) or ""
    border_to_name: str = theme.border.get_border_name(border_to) or ""
    border_result: str | None = translate_border_dict[side].get(
        (border_from_name, border_to_name)
    )

    if border_result:
        return getattr(theme.border, border_result)
    return border_from
