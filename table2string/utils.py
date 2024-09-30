import os
import re
import unicodedata
from functools import lru_cache
from typing import Union, List, Tuple, Optional, Dict

from table2string.themes import Theme, Themes
from table2string.aligns import HorizontalAlignment, VerticalAlignment


ANSI_REGEX = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
translate_border_dict: Dict[str, Dict[Tuple[str, str], str]] = {
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
    border_result: Optional[str] = translate_border_dict[side].get(
        (border_from_name, border_to_name)
    )

    if border_result:
        return getattr(theme.border, border_result)
    return border_from


def get_text_width_in_console(text: str) -> int:
    """
    Calculates the length of the text in the console
    Some special characters and emoji

    :param text: Text
    :return: Calculates the length of the text in the console
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
    row_widths: Tuple[int, ...],
    max_width: int = 120,
    min_row_widths: Optional[Tuple[int, ...]] = None,
    proportion_coefficient: float = 0.5,
) -> Tuple[int, ...]:
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
    if min_row_widths and sum(min_row_widths) > max_width:
        raise ValueError(f"{sum(min_row_widths)} <= {max_width}")

    if not (0.0 <= proportion_coefficient <= 2.0):
        raise ValueError(f"0.0 <= {proportion_coefficient} <= 2.0")

    if min_row_widths is None:
        min_row_widths = (1,) * len(row_widths)

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

    return tuple(distributed)


def transform_align(
    column_count: int,
    align: Optional[
        Union[
            Tuple[Union[HorizontalAlignment, VerticalAlignment, str], ...],
            Union[HorizontalAlignment, VerticalAlignment, str],
        ]
    ] = None,
    default: str = "*",
) -> Tuple[str, ...]:
    """
    Convert align to a suitable view

    :param column_count: Number of column
    :param align: Alignments
    :param default: Default value to fill
    :return: Transformed alignment
    """
    if align is None:
        align = default

    if isinstance(align, str):
        return (align, *(align,) * (column_count - 1))[:column_count]
    elif isinstance(align, (HorizontalAlignment, VerticalAlignment)):
        return (
            align.value,
            *(align.value,) * (column_count - 1),
        )[:column_count]
    else:
        return (
            *[
                (
                    a.value
                    if isinstance(a, (HorizontalAlignment, VerticalAlignment))
                    else a
                )
                for a in align
            ],
            *(default,) * (column_count - len(align)),
        )[:column_count]


def transform_width(
    width: Union[int, Tuple[int, ...], None],
    column_count: int,
    row_widths: Tuple[int, ...],
    min_row_widths: Optional[Tuple[int, ...]] = None,
    proportion_coefficient: float = 0.5,
) -> Tuple[int, ...]:
    """
    Convert width to a suitable view

    :param width: Required width or widths
    :param column_count: Number of columns
    :param row_widths: Column width
    :param min_row_widths: List of minimum widths for columns
    :param proportion_coefficient: Reduction coefficient for too large numbers
    :return: Transformed widths
    """
    if width is None:
        return row_widths

    if isinstance(width, (tuple, list)):
        width_l = list(width[:column_count])

        if len(width_l) == column_count:
            return tuple(width_l)

        if len(width_l) < column_count:
            width_l.extend((width_l[-1] for _ in range(column_count - len(width_l))))
            return tuple(width_l)

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


def split_text(
    text: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    line_break_symbol: str = "\\",
    cell_break_symbol: str = "…",
) -> Tuple[List[str], List[str], bool, Dict[str, Tuple[str, ...]]]:
    """
    Splits text to the desired width and height

    :param text: Text
    :param width: Width
    :param height: Height
    :param line_break_symbol: "\\" or "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :return: Split text by width and height
    """
    lines = text.split("\n")

    if width is None:
        width = len(max(lines))

    result_lines: List[str] = []
    result_symbol: List[str] = []

    for line in lines:
        if get_text_width_in_console(line) == 0:
            result_lines.append("")
            result_symbol.append(" ")
        else:
            while line:
                if get_text_width_in_console(line) <= width:
                    result_lines.append(line)
                    result_symbol.append(" ")
                    line = ""
                else:
                    w = 0
                    assert width >= 1, width
                    while get_text_width_in_console(line[:w]) <= width - 1:
                        w += 1
                    result_lines.append(line[:w])
                    result_symbol.append(line_break_symbol)
                    line = line[w:]

    if height and len(result_lines) > height:
        result_lines = result_lines[:height]
        result_symbol = result_symbol[:height]
        result_symbol[-1] = cell_break_symbol

    return result_lines, result_symbol, False, {}


def split_text_for_sub_table(
    string_sub_table: str, max_height: Optional[int]
) -> Tuple[List[str], List[str], bool, Dict[str, Tuple[str, ...]]]:
    sub_table_lines = string_sub_table.splitlines()

    if max_height:
        sub_table_lines = sub_table_lines[: max_height + 2]

    blank_line = ""
    return (
        [line[1:-1] for line in sub_table_lines[1:-1]],
        [blank_line for _ in range(len(sub_table_lines))],
        True,
        {
            "border_top": tuple(sub_table_lines[0][2:-2]),
            "border_bottom": tuple(sub_table_lines[-1][2:-2]),
            "border_left": tuple(line[0] for line in sub_table_lines[1:-1]) or (" ",),
            "border_right": tuple(line[-1] for line in sub_table_lines[1:-1]) or (" ",),
        },
    )


def fill_line(
    columns_lines: Tuple[List[str], ...],
    columns_symbols: Tuple[List[str], ...],
    subtable_columns: Tuple[bool, ...],
    border_data_list: Tuple[Dict[str, Tuple[str, ...]], ...],
    widths: Tuple[int, ...],
    h_align: Tuple[str, ...],
    v_align: Tuple[str, ...],
    theme: Theme = Themes.ascii_thin,
) -> str:
    """
    Fills the line

    :param columns_lines: Tuple of a list of lines
    :param columns_symbols: Line break or line ending characters
    :param subtable_columns: A list indicating whether the column should be formatted as subtable
    :param border_data_list: Tuple of dictionaries for joining boundaries
    :param widths: List of widths
    :param h_align: Tuple of horizontal alignments
    :param v_align: Tuple of vertical alignments
    :param theme: Theme
    :return: Filled line
    """
    h_align_left, h_align_right = [], []

    for a in h_align:
        al, ar = [*a * 2] if len(a) == 1 else [*a]
        h_align_left.append(al)
        h_align_right.append(ar)

    # Make each element the same width according to the maximum element
    for n, raw_lines in enumerate(columns_lines):
        if (
            h_align_left[n] == "^"
            and h_align_right[n] in ("<", ">")
            and len(raw_lines) > 1
        ):
            max_width = len(max(raw_lines, key=len))
            raw_lines[:] = [
                f"{r:{h_align_right[n]}{max_width}}" for _n, r in enumerate(raw_lines)
            ]
            h_align_right[n] = "^"

        if h_align_left[n] == "*" or h_align_right[n] == "*":
            try:
                float("\n".join(raw_lines))
                h_align_left[n] = ">"
                h_align_right[n] = ">"
            except ValueError:
                h_align_left[n] = "<"
                h_align_right[n] = "<"

        if not subtable_columns[n]:
            raw_lines[:] = apply_v_align(raw_lines, v_align[n])

    result_lines: List[str] = []
    symbols = list(zip(*columns_symbols))
    vertical = theme.border.vertical
    tags = [False for _ in subtable_columns]
    lines: Tuple[str, ...]

    for ci, lines in enumerate(zip(*columns_lines)):  # ci - column index
        # Selects alignment individually for each column and each row
        current_h_align: List[str] = []
        for ri, line in enumerate(lines):
            if tags[ri]:
                current_h_align.append(h_align_right[ri])
            else:
                current_h_align.append(h_align_left[ri])
            if not line.isspace():
                tags[ri] = True

        template_list: List[str] = []
        row_length = len(lines)
        for ri, line in enumerate(lines):  # ri - row index
            if subtable_columns[ri]:
                border_data: Dict[str, Tuple[str, ...]] = border_data_list[ri]
                if ri == 0:
                    template_list.append(
                        translate_theme_border(
                            "border_left",
                            theme,
                            vertical,
                            border_data["border_left"][0],
                        )
                    )
                elif ri == row_length - 1:
                    template_list[-1] = translate_theme_border(
                        "border_right",
                        theme,
                        template_list[-1] or vertical,
                        border_data["border_right"][-1],
                    )

                try:
                    border_left_ri = border_data["border_left"][ci]
                    border_right_ri = border_data["border_right"][ci]
                except IndexError:
                    border_left_ri = " "
                    border_right_ri = " "

                if template_list:
                    template_list[-1] = (
                        translate_theme_border(
                            "border_left",
                            theme,
                            template_list[-1] or vertical,
                            border_left_ri,
                        )
                        or template_list[-1]
                    )

                template_list.append(f"{{:<{widths[ri] + 2}}}")

                border_right = translate_theme_border(
                    "border_right", theme, vertical, border_right_ri
                )
                template_list.append(border_right)
            else:
                if ri == 0:
                    template_list.append(vertical)

                width = widths[ri] - (get_text_width_in_console(line) - len(line))
                template_list.append(
                    f" {{:{current_h_align[ri]}{width}}}{symbols[ci][ri]}"
                )
                template_list.append(vertical)

        template: str = "".join(template_list)
        result_lines.append(template.format(*lines))

    return "\n".join(result_lines)


def apply_v_align(cell_rows: List[str], v_align: str) -> List[str]:
    """
    Apply v_align

    :param cell_rows: List of strings in a cell
    :param v_align: Vertical alignment
    :return: Applied vertical alignments
    """
    rows_count = len(cell_rows)

    if v_align == "_":
        while cell_rows[-1].isspace():
            cell_rows.insert(0, cell_rows.pop())

    elif v_align == "-" and rows_count > 1:
        while cell_rows and cell_rows[0].isspace():
            cell_rows.pop(0)
        while cell_rows and cell_rows[-1].isspace():
            cell_rows.pop()

        not_empty_rows_count = len(cell_rows)
        difference = rows_count - not_empty_rows_count
        top = difference // 2
        bottom = difference - top

        for _ in range(top):
            cell_rows.insert(0, " ")
        for _ in range(bottom):
            cell_rows.append(" ")

    return [s if s else " " for s in cell_rows]


def apply_border_data(
    string_border: str,
    side: str,
    theme: Theme,
    border_data_list: Tuple[Dict[str, Tuple[str, ...]], ...],
    max_widths: Tuple[int, ...],
) -> str:
    """
    Connects table and subtable boundaries

    :param string_border: String border
    :param side: "border_left" or "border_right" or "border_top" or "border_bottom"
    :param theme: Theme
    :param border_data_list: Tuple of dictionaries to join boundaries
    :param max_widths: List of widths for each column
    """
    string_border_list = list(string_border)
    index = 2

    for current_border_data, width in zip(border_data_list, max_widths):
        if current_border_data:
            for border_r in current_border_data[side]:
                border_l = string_border_list[index]
                if border_l == " ":
                    border_l = theme.border.horizontal
                if side == "border_top":
                    string_border_list[index] = (
                        translate_theme_border(side, theme, border_l, border_r)
                        or border_l
                    )
                elif side == "border_bottom":
                    string_border_list[index] = (
                        translate_theme_border(side, theme, border_l, border_r)
                        or border_l
                    )
                index += 1
        else:
            index += width
        index += 3
    return "".join(string_border_list)


def terminal_size(default: Tuple[int, int] = (120, 30)) -> Tuple[int, int]:
    """
    :param default: Will be returned if it is not possible to get the console size
    :return: columns, lines
    """
    try:
        size = os.get_terminal_size()
    except OSError:
        return default

    return size.columns, size.lines


def generate_borders(theme: Theme, max_widths: Tuple[int, ...]) -> Tuple[str, ...]:
    """
    EXAMPLE

    theme                = Themes.thin_double
    up_separator         = "┌───────────┐"
    under_name_separator = "├───┬───┬───┤"
    up_noname_separator  = "┌───┬───┬───┐"
    line_separator       = "├───┼───┼───┤"
    line_separator_plus  = "╞═══╪═══╪═══╡"
    down_separator       = "└───┴───┴───┘"

    :param theme: Theme
    :param max_widths: List of column widths
    :return: (
        up_separator,
        under_name_separator,
        up_noname_separator,
        line_separator,
        line_separator_plus,
        down_separator,
    )
    """
    horizontally = [(theme.border.horizontal * (i + 2)) for i in max_widths]
    up_separator = "".join(
        (
            theme.border.top_left,
            "".join(horizontally),
            theme.border.horizontal * (len(max_widths) - 1),
            theme.border.top_right,
        )
    )
    under_name_separator = "".join(
        (
            theme.border.vertical_left,
            theme.border.top_horizontal.join(horizontally),
            theme.border.vertical_right,
        )
    )
    up_noname_separator = "".join(
        (
            theme.border.top_left,
            theme.border.top_horizontal.join(horizontally),
            theme.border.top_right,
        )
    )
    line_separator = "".join(
        (
            theme.border.vertical_left,
            theme.border.central.join(horizontally),
            theme.border.vertical_right,
        )
    )
    line_separator_plus = "".join(
        (
            theme.border.vertical_left_plus,
            theme.border.central_plus.join(
                (theme.border.horizontal_plus * (i + 2)) for i in max_widths
            ),
            theme.border.vertical_right_plus,
        )
    )
    down_separator = "".join(
        (
            theme.border.bottom_left,
            theme.border.bottom_horizontal.join(horizontally),
            theme.border.bottom_right,
        )
    )
    return (
        up_separator,
        under_name_separator,
        up_noname_separator,
        line_separator,
        line_separator_plus,
        down_separator,
    )
