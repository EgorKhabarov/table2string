from dataclasses import dataclass
from typing import Optional, Dict, Tuple


BORDER_EXAMPLE_SYMBOLS: Dict[str, Tuple[str, ...]] = {
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

    def get_border_name(self, border: str) -> Optional[str]:
        if border == self.horizontal:
            return "horizontal"
        elif border == self.vertical:
            return "vertical"
        elif border == self.central:
            return "central"
        elif border == self.top_left:
            return "top_left"
        elif border == self.top_right:
            return "top_right"
        elif border == self.bottom_left:
            return "bottom_left"
        elif border == self.bottom_right:
            return "bottom_right"
        elif border == self.vertical_left:
            return "vertical_left"
        elif border == self.vertical_right:
            return "vertical_right"
        elif border == self.top_horizontal:
            return "top_horizontal"
        elif border == self.bottom_horizontal:
            return "bottom_horizontal"
        elif border == self.vertical_left_plus:
            return "vertical_left_plus"
        elif border == self.horizontal_plus:
            return "horizontal_plus"
        elif border == self.central_plus:
            return "central_plus"
        elif border == self.vertical_right_plus:
            return "vertical_right_plus"
        elif border == self.top_horizontal_plus:
            return "top_horizontal_plus"
        elif border == self.bottom_horizontal_plus:
            return "bottom_horizontal_plus"

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
        return f"Themes.{self.name}"


class Themes:
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
