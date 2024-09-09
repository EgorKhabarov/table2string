import inspect

import unicodedata
from dataclasses import dataclass
from cachetools import cached, LRUCache
from typing import Union, List, Tuple, Sequence, Optional

ALLOWED_ALIGNS = [
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


@dataclass
class Border:
    name: str = "ascii_thin"
    horizontal: str = "-"
    vertical: str = "|"
    top_left: str = "+"
    top_right: str = "+"
    bottom_left: str = "+"
    bottom_right: str = "+"
    vertical_left: str = "+"
    vertical_right: str = "+"
    top_horizontal: str = "+"
    bottom_horizontal: str = "+"
    central: str = "+"
    vertical_left_plus: str = "+"
    horizontal_plus: str = "-"
    central_plus: str = "+"
    vertical_right_plus: str = "+"
    top_horizontal_plus: str = "+"
    bottom_horizontal_plus: str = "+"

    def get_border_name(self, border: str) -> str:
        match border:
            case self.horizontal:
                return "horizontal"
            case self.vertical:
                return "vertical"
            case self.central:
                return "central"
            case self.top_left:
                return "top_left"
            case self.top_right:
                return "top_right"
            case self.bottom_left:
                return "bottom_left"
            case self.bottom_right:
                return "bottom_right"
            case self.vertical_left:
                return "vertical_left"
            case self.vertical_right:
                return "vertical_right"
            case self.top_horizontal:
                return "top_horizontal"
            case self.bottom_horizontal:
                return "bottom_horizontal"
            case self.vertical_left_plus:
                return "vertical_left_plus"
            case self.horizontal_plus:
                return "horizontal_plus"
            case self.central_plus:
                return "central_plus"
            case self.vertical_right_plus:
                return "vertical_right_plus"
            case self.top_horizontal_plus:
                return "top_horizontal_plus"
            case self.bottom_horizontal_plus:
                return "bottom_horizontal_plus"


class Theme:
    def __init__(self, border: Border = Border(), custom_sub_table_theme: Optional["Theme"] = None):
        self.border = border
        self.custom_sub_table_theme = custom_sub_table_theme or self

    def __repr__(self):
        return f"Themes.{self.border.name}"


class Themes:
    ascii_thin: Theme = Theme()
    ascii_thin_double: Theme = Theme(
        border=Border(
            name="ascii_thin_double",
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
    )
    ascii_double: Theme = Theme(
        border=Border(
            name="ascii_double",
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
        border=Border(
            name="ascii_double_thin",
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
    )
    ascii_booktabs: Theme = Theme(
        border=Border(
            name="ascii_booktabs",
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
        border=Border(
            name="thin",
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
        border=Border(
            name="thin_thick",
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
        border=Border(
            name="thin_double",
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
        border=Border(
            name="rounded",
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
        border=Border(
            name="rounded_thick",
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
        border=Border(
            name="rounded_double",
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
        border=Border(
            name="thick",
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
        border=Border(
            name="thick_thin",
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
            vertical_left_plus="┠",
            horizontal_plus="━",
            central_plus="╂",
            vertical_right_plus="┨",
            top_horizontal_plus="┳",
            bottom_horizontal_plus="┻",
        ),
        custom_sub_table_theme=thick,
    )
    double: Theme = Theme(
        border=Border(
            name="double",
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
        border=Border(
            name="double_thin",
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
            top_horizontal_plus="╦",
            bottom_horizontal_plus="╩",
        ),
    )
    booktabs: Theme = Theme(
        border=Border(
            name="booktabs",
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
        custom_sub_table_theme=thin,
    )
    markdown: Theme = Theme(
        border=Border(
            name="markdown",
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
    )


class MutableString:
    def __init__(self, seq=""):
        self.data = list(seq)

    def __getitem__(self, index):
        return self.data[index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            self.data[index] = list(value)
        else:
            self.data[index] = value

    def __str__(self):
        return "".join(self.data)

    def __repr__(self):
        return f"MutableString({str(self)!r})"


translate_border_dict = {
    "border_left": {
        ("vertical", "horizontal"): "vertical_left",
        ("vertical", "horizontal_plus"): "vertical_left_plus",
        ("vertical_right", "horizontal"): "central",
        ("vertical_right", "horizontal_plus"): "central_plus",
    },
    "border_right": {
        ("vertical", "horizontal"): "vertical_right",
        ("vertical", "horizontal_plus"): "vertical_right_plus",
        ("vertical_left", "horizontal"): "central",
        ("vertical_left", "horizontal_plus"): "central_plus",
    },
    "border_top": {
        ("horizontal", ""): "horizontal",
        ("horizontal", "vertical"): "top_horizontal",
        ("top_horizontal", ""): "",
        ("top_horizontal", "vertical"): "top_horizontal",
        ("bottom_horizontal", ""): "bottom_horizontal",
        ("bottom_horizontal", "vertical"): "central",
        ("horizontal", "top_horizontal"): "top_horizontal",
        ("horizontal_plus", ""): "horizontal_plus",
        ("horizontal_plus", "top_horizontal"): "top_horizontal_plus",
    },
    "border_bottom": {
        ("horizontal", "vertical"): "bottom_horizontal",
        ("top_horizontal", "vertical"): "central",
        ("bottom_horizontal", "vertical"): "bottom_horizontal",
        ("horizontal", "bottom_horizontal"): "bottom_horizontal",
    },
}
border_translate_cache = LRUCache(maxsize=100)


@cached(border_translate_cache)
def translate_theme_border(side: str, theme: Theme, border_from: str, border_to: str) -> str:
    border_from_name = theme.border.get_border_name(border_from)
    border_to_name = theme.border.get_border_name(border_to)

    if border_result := translate_border_dict[side].get((border_from_name, border_to_name)):
        return getattr(theme.border, border_result)
    return border_from


def get_text_width_in_console(text: str) -> int:
    """
    Calculates the number of positions that a line will occupy in the console.
    """
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ("W", "F"):
            width += 2  # Wide characters
        else:
            width += 1  # Narrow characters
    return width


def decrease_numbers(
    row_lengths: List[int],
    max_width: int = 120,
    min_width: int = 1,
) -> List[int]:
    current_sum = sum(row_lengths)
    difference = max_width - current_sum

    if difference == 0 and all(n >= min_width for n in row_lengths):
        return row_lengths

    proportions = [n / current_sum for n in row_lengths]
    distributed = [n + round(difference * p) for n, p in zip(row_lengths, proportions)]

    total = sum(distributed)
    final_difference = max_width - total

    if final_difference > 0:
        for i in range(final_difference):
            distributed[i % len(distributed)] += 1
    elif final_difference < 0:
        for i in range(-final_difference):
            if distributed[i % len(distributed)] > min_width:
                distributed[i % len(distributed)] -= 1

    # Ensure all values are at least min_value
    for i in range(len(distributed)):
        if distributed[i] < min_width:
            distributed[i] = min_width

    # Adjust again if min_value correction breaks the total sum
    total = sum(distributed)
    final_difference = max_width - total

    if final_difference > 0:
        for i in range(final_difference):
            distributed[i % len(distributed)] += 1
    elif final_difference < 0:
        for i in range(-final_difference):
            if distributed[i % len(distributed)] > min_width:
                distributed[i % len(distributed)] -= 1

    return distributed


def transform_align(
    column_count: int, align: Union[Tuple[str, ...], str] = "*"
) -> Tuple[str, ...]:
    """
    Convert align to a suitable view

    :param column_count:
    :param align:
    :return:
    """
    wrong_align = [
        a
        for a in ((align,) if isinstance(align, str) else align)
        if a not in ALLOWED_ALIGNS
    ]
    if wrong_align:
        raise ValueError(f"{wrong_align[0]} not in ALLOWED_ALIGNS")

    if isinstance(align, str):
        align = (align, *(align,) * (column_count - 1))
    else:
        align = (*align, *("*",) * (column_count - len(align)))

    return align[:column_count]


def transform_width(
    width: Union[int, Tuple[int, ...], None],
    column_count: int,
    row_lengths: List[int],
) -> Union[List[int]]:
    """

    :param width:
    :param column_count:
    :param row_lengths:
    :return:
    """
    if width is None:
        return row_lengths

    if isinstance(width, (tuple, list)):
        width_l = list(width[:column_count])

        if len(width_l) == column_count:
            return width_l

        if len(width_l) < column_count:
            width_l.extend((width_l[-1] for _ in range(column_count - len(width_l))))
            return width_l

        width_t = tuple((*width_l, *(width_l[-1],) * (column_count - len(width_l))))
        width_i = sum(width_t) + (3 * len(width_t)) + 1
    else:
        width_i = width

    if width_i < column_count * 4 + 1:
        width_i = sum(1 if rl > 1 else 0 for rl in row_lengths) + (3 * column_count) + 1

    # Calculate the width of each column
    sum_column_width = (width_i - column_count * 3 - 1) or 1
    max_widths = decrease_numbers(row_lengths, sum_column_width)
    return max_widths


def line_spliter(
    text: str,
    width: Union[int, None] = None,
    height: Union[int, None] = None,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    theme: Theme = Themes.ascii_thin,  # noqa
) -> List[List[str]]:
    """

    :param text:
    :param width:
    :param height:
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param theme:
    :return:
    """
    lines = text.split("\n")

    if width is None:
        width = len(max(lines))

    result_lines = []
    result_breaks = []

    for line in lines:
        if get_text_width_in_console(line) == 0:
            result_lines.append(" ")
            result_breaks.append(" ")
        else:
            while line:
                if get_text_width_in_console(line) <= width:
                    result_lines.append(line)
                    result_breaks.append(" ")
                    line = ""
                else:
                    w = 0
                    assert width >= 1, width
                    while get_text_width_in_console(line[:w]) <= width - 1:
                        w += 1
                    result_lines.append(line[:w])
                    result_breaks.append(line_break_symbol)
                    line = line[w:]

    if height and len(result_lines) > height:
        result_lines = result_lines[:height]
        result_breaks = result_breaks[:height]
        result_breaks[-1] = cell_break_symbol

    return [result_lines, result_breaks, False, None]


def fill_line(
    rows: List[List[str]],
    symbols: List[List[str]],
    lines_without_border: list[bool],
    metadata_list: tuple[dict[str, str] | None, ...],
    widths: List[int],
    align: Tuple[str, ...],
    theme: Theme = Themes.ascii_thin,
    without_border: bool = False,
) -> str:
    """

    :param rows:
    :param symbols:
    :param lines_without_border:
    :param metadata_list:
    :param widths:
    :param align:
    :param theme:
    :param without_border:
    :return:
    """
    border = theme.border

    align_left, align_right = [], []
    for a in align:
        al, ar = [*a * 2] if len(a) == 1 else [*a]
        align_left.append(al)
        align_right.append(ar)

    # Make each element the same width according to the maximum element
    for n, row in enumerate(rows):
        if align_left[n] == "^" and align_right[n] in ("<", ">") and len(row) > 1:
            max_width = len(max(row, key=len))
            row[:] = [f"{r:{align_right[n]}{max_width}}" for _n, r in enumerate(row)]
            align_right[n] = "^"

        if align_left[n] == "*" or align_right[n] == "*":
            try:
                float("\n".join(row))
                align_left[n] = ">"
                align_right[n] = ">"
            except ValueError:
                align_left[n] = "<"
                align_right[n] = "<"

    lines = []
    symbol = list(zip(*symbols))
    vertical = border.vertical
    vertical_without_border = "" if without_border else border.vertical

    for ri, row in enumerate(zip(*rows)):  # ri - row index
        row = list(row)

        if ri == 0:
            current_align = align_left
        else:
            current_align = align_right

        def get_width(ci: int):
            return widths[ci] - (
                get_text_width_in_console(row[ci]) - len(row[ci])
            )

        def get_template() -> str:
            template_list = []
            row_length = len(row)
            for ci in range(row_length):  # ci - column index
                if lines_without_border[ci]:
                    metadata = metadata_list[ci]
                    if not without_border:
                        if ci == 0:
                            template_list.append(translate_theme_border("border_left", theme, vertical, metadata["border_left"][0]))
                        elif ci == row_length - 1:
                            template_list[-1] = translate_theme_border("border_right", theme, template_list[-1] or vertical, metadata["border_right"][-1])

                    try:
                        metadata_border_left_ri = metadata["border_left"][ri]
                        metadata_border_right_ri = metadata["border_right"][ri]
                    except IndexError:
                        metadata_border_left_ri = " "
                        metadata_border_right_ri = " "
                    if template_list:
                        template_list[-1] = translate_theme_border("border_left", theme, template_list[-1] or vertical, metadata_border_left_ri) or template_list[-1]

                    # print(f"{widths[ci]=} {metadata_border_left_ri=} {metadata_border_right_ri=}")
                    template_list.append(f"{metadata_border_left_ri}{{:<{widths[ci]}}}{metadata_border_right_ri}")

                    border_right = translate_theme_border("border_right", theme, vertical, metadata_border_right_ri)
                    template_list.append(border_right)
                    if without_border and ci == row_length - 1:
                        del template_list[-1]
                else:
                    if not without_border:
                        if ci == 0:
                            template_list.append(vertical_without_border)
                    template_list.append(f" {{:{current_align[ci]}{get_width(ci)}}}{symbol[ri][ci]}")

                    template_list.append(vertical)
                    if without_border and ci == row_length - 1:
                        del template_list[-1]

            return "".join(template_list)

        template = get_template()
        lines.append(template.format(*row))

    return "\n".join(lines)


def check_cell(cell) -> bool:
    if not hasattr(cell, "stringify"):
        return False

    if not callable(cell.stringify):
        return False

    if not {
        "align",
        "max_width",
        "max_height",
        "line_break_symbol",
        "cell_break_symbol",
        "theme",
        "without_border",
        "ignore_width_errors",
    }.issubset(
        {param.name for param in inspect.signature(cell.stringify).parameters.values()}
    ):
        return False

    return True


def get_row_lengths(table: Sequence[Sequence]) -> List[int]:
    return [
        max(
            (lambda row_lengths: sum(row_lengths) + 3 * len(row_lengths))(get_row_lengths(cell.table))
            if check_cell(cell)
            else (
                max(
                    get_text_width_in_console(line)
                    for line in str_cell.splitlines() or [""]
                )
                if (str_cell := str(cell))
                else 1
            )
            for cell in column
        )
        for ci, column in enumerate(zip(*table))
    ]


def apply_metadata(string: str, style: str, theme: Theme, metadata_list: tuple[dict | None, ...], max_widths: list[int], without_border: bool) -> str:
    string = MutableString(string)
    index = 2
    if without_border:
        index -= 1

    for current_metadata, width in zip(metadata_list, max_widths):
        if current_metadata:
            for border_r in current_metadata[style]:
                border_l = string[index]
                if border_l == " ":
                    border_l = theme.border.horizontal
                if style == "border_top":
                    string[index] = translate_theme_border(style, theme, border_l, border_r) or border_l
                elif style == "border_bottom":
                    string[index] = translate_theme_border(style, theme, border_l, border_r) or border_l
                index += 1
        else:
            index += width
        index += 3
    return str(string)
