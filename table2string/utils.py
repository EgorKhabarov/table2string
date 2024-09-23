import os
import re
import unicodedata
from functools import lru_cache
from dataclasses import dataclass
from typing import Union, List, Tuple, Optional, Dict


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
ALLOWED_V_ALIGNS = [
    "^",
    "-",
    "_",
]
ANSI_REGEX = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
translate_border_dict = {
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
        border: Border = Border(),
        custom_sub_table_theme: Optional["Theme"] = None,
    ):
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
        custom_sub_table_theme=ascii_thin,
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
        custom_sub_table_theme=ascii_double,
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
            top_horizontal_plus="╥",
            bottom_horizontal_plus="╨",
        ),
        custom_sub_table_theme=double,
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
        custom_sub_table_theme=ascii_thin,
    )


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
    border_from_name = theme.border.get_border_name(border_from)
    border_to_name = theme.border.get_border_name(border_to)
    border_result = translate_border_dict[side].get((border_from_name, border_to_name))

    if border_result:
        return getattr(theme.border, border_result)
    return border_from


def get_text_width_in_console(text: str) -> int:
    """
    Calculates the number of positions that a line will occupy in the console.
    """
    text = ANSI_REGEX.sub("", text)
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ("W", "F"):
            width += 2  # Wide characters
        else:
            width += 1  # Narrow characters
    return width


def proportional_change(
    row_widths: List[int],
    max_width: int = 120,
    min_row_widths: Optional[List[int]] = None,
    proportion_coefficient: float = 0.5,
) -> List[int]:
    """
    The function changes the values in `row_widths` proportionally,
    so that the sum of the numbers remains equal to `max_width`
    and each value in must be greater than or equal to the corresponding number in `min_row_widths`.
    The proportionality condition can be violated only to meet the conditions in `min_row_widths`
    or to avoid the appearance of fractional numbers.
    When passing arguments to the function, it is guaranteed that `max_width`
    will be large enough to change the values in `row_widths`
    without violating the conditions of the sum and minimum values.
    It is also guaranteed that all values in the list of `row_widths`
    and `min_row_widths` will be greater than 0.
    The length of `row_widths` and `min_row_widths` are the same
    if `min_row_widths` is not None. If `min_row_widths` is None,
    then it can be treated as a list whose length is `row_widths`, and all values are 1.
    Fractal numbers and numbers less than one are not allowed.
    The `proportion_coefficient` argument is the coefficient for reducing large numbers.

    :param row_widths: List of widths for each column
    :param max_width: Max table width (Required sum for `row_widths`)
    :param min_row_widths: List of minimum widths for each column
    :param proportion_coefficient: Reduction coefficient for too large numbers
    """
    if min_row_widths:
        assert sum(min_row_widths) <= max_width, f"{sum(min_row_widths)} <= {max_width}"
    assert (
        0.0 <= proportion_coefficient <= 2.0
    ), f"0.0 <= {proportion_coefficient} <= 2.0"
    if min_row_widths is None:
        min_row_widths = [1] * len(row_widths)

    current_sum = sum(row_widths)
    difference = max_width - current_sum

    if difference == 0 and all(n >= m for n, m in zip(row_widths, min_row_widths)):
        return row_widths

    proportions = [n / current_sum for n in row_widths]
    distributed = [
        max(m, n + round(difference * p))
        for n, p, m in zip(row_widths, proportions, min_row_widths)
    ]

    total = sum(distributed)
    final_difference = max_width - total

    # We adjust if the final amount is more or less than the target
    if final_difference > 0:
        for i in range(final_difference):
            idx = i % len(distributed)
            distributed[idx] += 1
    elif final_difference < 0:
        for i in range(-final_difference):
            idx = i % len(distributed)
            if distributed[idx] > min_row_widths[idx]:
                distributed[idx] -= 1

    # Reduction of large values by a coefficient
    for i in range(len(distributed)):
        distributed[i] = max(
            min_row_widths[i],
            distributed[i]
            - round(distributed[i] * proportion_coefficient)
            + round(sum(distributed) * proportion_coefficient / len(distributed)),
        )

    # Checking and final adjustment of the amount
    total = sum(distributed)
    final_difference = max_width - total

    while final_difference != 0:
        if final_difference > 0:
            for i in range(len(distributed)):
                if distributed[i] < max_width - (len(distributed) - 1):
                    distributed[i] += 1
                    final_difference -= 1
                    if final_difference == 0:
                        break
        elif final_difference < 0:
            for i in range(len(distributed)):
                if distributed[i] > min_row_widths[i]:
                    distributed[i] -= 1
                    final_difference += 1
                    if final_difference == 0:
                        break

    return distributed


def transform_align(
    column_count: int,
    align: Optional[Union[Tuple[str, ...], str]] = None,
    is_v_align: bool = False,
) -> Tuple[str, ...]:
    """
    Convert align to a suitable view

    :param column_count:
    :param align:
    :param is_v_align:
    :return:
    """
    allowed_list = ALLOWED_V_ALIGNS if is_v_align else ALLOWED_ALIGNS
    string_allowed_list_name = "ALLOWED_V_ALIGNS" if is_v_align else "ALLOWED_ALIGNS"
    default = "^" if is_v_align else "*"
    if align is None:
        align = default

    wrong_align = [
        a
        for a in ((align,) if isinstance(align, str) else align)
        if a not in allowed_list
    ]
    if wrong_align:
        raise ValueError(f"{wrong_align[0]} not in {string_allowed_list_name}")

    if isinstance(align, str):
        align = (align, *(align,) * (column_count - 1))
    else:
        align = (*align, *(default,) * (column_count - len(align)))

    return align[:column_count]


def transform_width(
    width: Union[int, Tuple[int, ...], None],
    column_count: int,
    row_widths: List[int],
    min_row_widths: Optional[List[int]] = None,
    proportion_coefficient: float = 0.5,
) -> List[int]:
    """
    Convert width to a suitable view

    :param width:
    :param column_count:
    :param row_widths:
    :param min_row_widths:
    :param proportion_coefficient:
    :return:
    """
    if width is None:
        return row_widths

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
        width_i = sum(1 if rl > 1 else 0 for rl in row_widths) + (3 * column_count) + 1

    # Calculate the width of each column
    sum_column_width = (width_i - column_count * 3 - 1) or 1
    max_widths = proportional_change(
        row_widths, sum_column_width, min_row_widths, proportion_coefficient
    )
    return max_widths


def line_spliter(
    text: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
) -> List[Union[List[str], List[bool], bool, None]]:
    """
    Splits text to the desired width and height

    :param text:
    :param width:
    :param height:
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :return:
    """
    lines = text.split("\n")

    if width is None:
        width = len(max(lines))

    result_lines = []
    result_breaks = []

    for line in lines:
        if get_text_width_in_console(line) == 0:
            result_lines.append("")
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
    rows: List[Union[List[str], List[bool], bool, None]],
    symbols: List[List[str]],
    subtable_columns: List[bool],
    metadata_list: Tuple[Optional[Dict[str, str]], ...],
    widths: List[int],
    align: Tuple[str, ...],
    v_align: Tuple[str, ...],
    theme: Theme = Themes.ascii_thin,
) -> str:
    """
    Fills the line

    :param rows:
    :param symbols: Line break or line ending characters
    :param subtable_columns: A list indicating whether the column should be formatted as subtable
    :param metadata_list: Tuple of dictionaries to join boundaries
    :param widths:
    :param align:
    :param v_align:
    :param theme:
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

    for ci, column in enumerate(rows):
        if not subtable_columns[ci]:
            rows[ci][:] = apply_v_align(column, v_align[ci])

    lines = []
    symbol = list(zip(*symbols))
    vertical = border.vertical
    tags = [False for _ in subtable_columns]

    for ri, row in enumerate(zip(*rows)):  # ri - row index
        current_align = []
        for ci, column in enumerate(row):
            if tags[ci]:
                current_align.append(align_right[ci])
            else:
                current_align.append(align_left[ci])
            if not column.isspace():
                tags[ci] = True

        template_list = []
        row_length = len(row)
        for ci in range(row_length):  # ci - column index
            if subtable_columns[ci]:
                metadata = metadata_list[ci]
                if ci == 0:
                    template_list.append(
                        translate_theme_border(
                            "border_left",
                            theme,
                            vertical,
                            metadata["border_left"][0],
                        )
                    )
                elif ci == row_length - 1:
                    template_list[-1] = translate_theme_border(
                        "border_right",
                        theme,
                        template_list[-1] or vertical,
                        metadata["border_right"][-1],
                    )

                try:
                    metadata_border_left_ri = metadata["border_left"][ri]
                    metadata_border_right_ri = metadata["border_right"][ri]
                except IndexError:
                    metadata_border_left_ri = " "
                    metadata_border_right_ri = " "
                if template_list:
                    template_list[-1] = (
                        translate_theme_border(
                            "border_left",
                            theme,
                            template_list[-1] or vertical,
                            metadata_border_left_ri,
                        )
                        or template_list[-1]
                    )

                template_list.append(f"{{:<{widths[ci]+2}}}")

                border_right = translate_theme_border(
                    "border_right", theme, vertical, metadata_border_right_ri
                )
                template_list.append(border_right)
            else:
                if ci == 0:
                    template_list.append(vertical)
                width = widths[ci] - (get_text_width_in_console(row[ci]) - len(row[ci]))
                template_list.append(
                    f" {{:{current_align[ci]}{width}}}{symbol[ri][ci]}"
                )

                template_list.append(vertical)

        template = "".join(template_list)
        lines.append(template.format(*row))

    return "\n".join(lines)


def apply_v_align(column: List[str], v_align: str) -> List[str]:
    """
    Apply v_align

    :param column:
    :param v_align:
    """
    if v_align == "_":
        while column[-1].isspace():
            column.insert(0, column.pop())
    elif v_align == "-":
        rows_count = len(column)
        while column[0].isspace():
            column.pop(0)
        while column[-1].isspace():
            column.pop()

        not_empty_rows_count = len(column)
        difference = rows_count - not_empty_rows_count
        top = difference // 2
        bottom = difference - top
        for _ in range(top):
            column.insert(0, " ")
        for _ in range(bottom):
            column.append(" ")

    return [s if s else " " for s in column]


def apply_metadata(
    string: str,
    side: str,
    theme: Theme,
    metadata_list: Tuple[Optional[dict], ...],
    max_widths: List[int],
) -> str:
    """
    Connects table and subtable boundaries

    :param string:
    :param side: "border_left" or "border_right" or "border_top" or "border_bottom"
    :param theme:
    :param metadata_list: Tuple of dictionaries to join boundaries
    :param max_widths:
    """
    string_list = list(string)
    index = 2

    for current_metadata, width in zip(metadata_list, max_widths):
        if current_metadata:
            for border_r in current_metadata[side]:
                border_l = string_list[index]
                if border_l == " ":
                    border_l = theme.border.horizontal
                if side == "border_top":
                    string_list[index] = (
                        translate_theme_border(side, theme, border_l, border_r)
                        or border_l
                    )
                elif side == "border_bottom":
                    string_list[index] = (
                        translate_theme_border(side, theme, border_l, border_r)
                        or border_l
                    )
                index += 1
        else:
            index += width
        index += 3
    return "".join(string_list)


def terminal_size() -> tuple[int, int]:
    try:
        size = os.get_terminal_size()
    except OSError:
        return 120, 30

    return size.columns, size.lines
