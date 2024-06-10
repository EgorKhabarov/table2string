import unicodedata
from dataclasses import dataclass
from typing import Union, List, Tuple, Sequence

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


class Theme:
    def __init__(self, border: Border = Border()):
        self.border = border


class Themes:
    ascii_thin: Theme = Theme(
        Border(
            "ascii_thin",
            "-",
            "|",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "-",
            "+",
            "+",
        ),
    )
    ascii_thin_double: Theme = Theme(
        Border(
            "ascii_thin_double",
            "-",
            "|",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "=",
            "+",
            "+",
        ),
    )
    ascii_double: Theme = Theme(
        Border(
            "ascii_double",
            "=",
            "‖",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "=",
            "+",
            "+",
        ),
    )
    ascii_double_thin: Theme = Theme(
        Border(
            "ascii_double_thin",
            "=",
            "‖",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "+",
            "-",
            "+",
            "+",
        ),
    )
    ascii_booktabs: Theme = Theme(
        Border(
            "ascii_booktabs",
            "-",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            "-",
            "-",
            "-",
            " ",
            "=",
            "=",
            " ",
        ),
    )
    thin: Theme = Theme(
        Border(
            "thin",
            "─",
            "│",
            "┌",
            "┐",
            "└",
            "┘",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "├",
            "─",
            "┼",
            "┤",
        ),
    )
    thin_thick: Theme = Theme(
        Border(
            "thin_thick",
            "─",
            "│",
            "┌",
            "┐",
            "└",
            "┘",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "┝",
            "━",
            "┿",
            "┥",
        ),
    )
    thin_double: Theme = Theme(
        Border(
            "thin_double",
            "─",
            "│",
            "┌",
            "┐",
            "└",
            "┘",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "╞",
            "═",
            "╪",
            "╡",
        ),
    )
    rounded: Theme = Theme(
        Border(
            "rounded",
            "─",
            "│",
            "╭",
            "╮",
            "╰",
            "╯",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "├",
            "─",
            "┼",
            "┤",
        ),
    )
    rounded_thick: Theme = Theme(
        Border(
            "rounded_thick",
            "─",
            "│",
            "╭",
            "╮",
            "╰",
            "╯",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "┝",
            "━",
            "┿",
            "┥",
        ),
    )
    rounded_double: Theme = Theme(
        Border(
            "rounded_double",
            "─",
            "│",
            "╭",
            "╮",
            "╰",
            "╯",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "╞",
            "═",
            "╪",
            "╡",
        ),
    )
    thick: Theme = Theme(
        Border(
            "thick",
            "━",
            "┃",
            "┏",
            "┓",
            "┗",
            "┛",
            "┣",
            "┫",
            "┳",
            "┻",
            "╋",
            "┣",
            "━",
            "╋",
            "┫",
        ),
    )
    thick_thin: Theme = Theme(
        Border(
            "thick_thin",
            "─",
            "│",
            "┌",
            "┐",
            "└",
            "┘",
            "├",
            "┤",
            "┬",
            "┴",
            "┼",
            "┠",
            "━",
            "╂",
            "┨",
        ),
    )
    double: Theme = Theme(
        Border(
            "double",
            "═",
            "║",
            "╔",
            "╗",
            "╚",
            "╝",
            "╠",
            "╣",
            "╦",
            "╩",
            "╬",
            "╠",
            "═",
            "╬",
            "╣",
        ),
    )
    double_thin: Theme = Theme(
        Border(
            "double_thin",
            "═",
            "║",
            "╔",
            "╗",
            "╚",
            "╝",
            "╠",
            "╣",
            "╦",
            "╩",
            "╬",
            "╟",
            "─",
            "╫",
            "╢",
        ),
    )
    booktabs: Theme = Theme(
        Border(
            "booktabs",
            "─",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            "─",
            "─",
            "─",
            " ",
            "━",
            "━",
            " ",
        ),
    )
    markdown: Theme = Theme(
        Border(
            "markdown",
            " ",
            "|",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            " ",
            "|",
            "-",
            "|",
            "|",
        ),
    )


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
    column_count: int,
    align: Union[Tuple[str, ...], str] = "*",
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

    return [result_lines, result_breaks]


def fill_line(
    rows: List[List[str]],
    symbols: List[List[str]],
    widths: List[int],
    align: Tuple[str, ...],
    theme: Theme = Themes.ascii_thin,
) -> str:
    """

    :param rows:
    :param symbols:
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

    for rn, row in enumerate(zip(*rows)):
        if rn == 0:
            current_align = align_left
        else:
            current_align = align_right

        def get_width(index: int):
            return widths[index] - (
                get_text_width_in_console(row[index]) - len(row[index])
            )

        template = border.vertical + "".join(
            f" {{:{current_align[cn]}{get_width(cn)}}}{symbol[rn][cn]}"
            + border.vertical
            for cn in range(len(row))
        )
        lines.append(template.format(*row))

    return "\n".join(lines)


def get_row_lengths(table: Sequence[Sequence]) -> List[int]:
    return [
        max(
            (
                max(
                    get_text_width_in_console(line)
                    for line in str(cell).splitlines() or [""]
                )
                if cell
                else 1
            )
            for cell in column
        )
        for column in zip(*table)
    ]
