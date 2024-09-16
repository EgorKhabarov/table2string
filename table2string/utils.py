import re
import unicodedata
from dataclasses import dataclass
from cachetools import cached, LRUCache
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
border_translate_cache = LRUCache(maxsize=100)


@cached(border_translate_cache)
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

    if border_result := translate_border_dict[side].get(
        (border_from_name, border_to_name)
    ):
        return getattr(theme.border, border_result)
    return border_from


def get_text_width_in_console(text: str) -> int:
    """
    Calculates the number of positions that a line will occupy in the console.
    """
    text = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)
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
    k: float = 0.5,
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
    The `k` argument is the coefficient for reducing large numbers.

    :param row_widths: List of widths for each column
    :param max_width: Max table width (Required sum for `row_widths`)
    :param min_row_widths: List of minimum widths for each column
    :param k: Reduction coefficient for too large numbers
    """
    if min_row_widths:
        assert sum(min_row_widths) <= max_width, f"{sum(min_row_widths)} <= {max_width}"
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
            - round(distributed[i] * k)
            + round(sum(distributed) * k / len(distributed)),
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
    row_widths: List[int],
    min_row_widths: Optional[List[int]] = None,
) -> List[int]:
    """
    Convert width to a suitable view

    :param width:
    :param column_count:
    :param row_widths:
    :param min_row_widths:
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
    max_widths = proportional_change(row_widths, sum_column_width, min_row_widths)
    return max_widths


def line_spliter(
    text: str,
    width: Union[int, None] = None,
    height: Union[int, None] = None,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
) -> List[List[str]]:
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
    subtable_columns: List[bool],
    metadata_list: Tuple[Dict[str, str] | None, ...],
    widths: List[int],
    align: Tuple[str, ...],
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

    lines = []
    symbol = list(zip(*symbols))
    vertical = border.vertical

    for ri, row in enumerate(zip(*rows)):  # ri - row index
        row = list(row)

        if ri == 0:
            current_align = align_left
        else:
            current_align = align_right

        def get_width(ci: int):
            return widths[ci] - (get_text_width_in_console(row[ci]) - len(row[ci]))

        def get_template() -> str:
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
                    template_list.append(
                        f" {{:{current_align[ci]}{get_width(ci)}}}{symbol[ri][ci]}"
                    )

                    template_list.append(vertical)

            return "".join(template_list)

        template = get_template()
        lines.append(template.format(*row))

    return "\n".join(lines)


def apply_metadata(
    string: str,
    side: str,
    theme: Theme,
    metadata_list: tuple[dict | None, ...],
    max_widths: list[int],
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
