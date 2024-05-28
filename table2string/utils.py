import unicodedata
from typing import Union, List, Tuple


# fmt: off
ALLOWED_ALIGNS = [
    "<", "^", ">",
    "<<", "<^", "<>",
    "^<", "^^", "^>",
    "><", ">^", ">>",
    "*", "**"
]
# fmt: on


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
    min_value: int = 10,
) -> List[int]:
    """

    :param row_lengths:
    :param max_width:
    :param min_value:
    :return:
    """
    # Calculate the average value
    mean_value = sum(row_lengths) / len(row_lengths)
    new_numbers = []

    for num in row_lengths:
        # Determine how much more or less this number is than the average
        diff_from_mean = num - mean_value

        if diff_from_mean > 0:
            reduction_percent = 0.4
        else:
            reduction_percent = 0.01

        reduced_num = num - (mean_value * reduction_percent)

        new_num = max(int(reduced_num), min_value)
        new_numbers.append(new_num)

    # If the total sum of new numbers exceeds max_width, reduce the largest number by 1
    while sum(new_numbers) > max_width:
        new_numbers[new_numbers.index(max(new_numbers))] -= 1

    # Calculate the coefficient for proportional increase if the sum is less than max_sum
    if sum(new_numbers) < max_width:
        new_numbers = [int(num * (max_width / sum(new_numbers))) for num in new_numbers]

    # If the total sum of new numbers is less than max_width, increase the smallest number by 1
    while sum(new_numbers) < max_width and min(new_numbers) < min_value:
        new_numbers[new_numbers.index(min(new_numbers))] += 1

    return new_numbers


def transform_align(
    column_count: int,
    align: Union[Tuple[str, ...], str] = "*",
) -> Tuple[str]:
    """
    Convert align to a suitable view

    :param column_count:
    :param align:
    :return:
    """
    if isinstance(align, str):
        align = (align, *(align,) * (column_count - 1))
    else:
        align = (*align, *("*",) * (column_count - len(align)))

    return align[:column_count]


def transform_width(
    width: Union[int, Tuple[int, ...], None],
    column_count: int,
    row_lengths: List[int],
) -> List[int]:
    """

    :param width:
    :param column_count:
    :param row_lengths:
    :return:
    """
    if isinstance(width, (tuple, list)) and column_count == len(width):
        return width

    if width is not None and isinstance(width, (tuple, list)):
        width: tuple[int]

        if len(width) < column_count:
            width: tuple = tuple((*width, *(width[-1],) * (column_count - len(width))))

        width: int = sum(width) + (3 * len(width)) + 1

    if width is not None and width < column_count + (3 * column_count) + 1:
        width: int = (
            sum(1 if rl > 1 else 0 for rl in row_lengths) + (3 * column_count) + 1
        )

    # Calculate the width of each column
    if width:
        sum_column_width = width - (3 * column_count) - 1
        max_widths = decrease_numbers(row_lengths, sum_column_width)
    else:
        max_widths = row_lengths

    return max_widths


def line_spliter(
    text: str,
    width: int = None,
    height: int = None,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
) -> Tuple[List[str], List[str]]:
    """

    :param text:
    :param width:
    :param height:
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :return:
    """
    lines = text.split("\n")
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
                    while get_text_width_in_console(line[:w]) <= width - 1:
                        w += 1
                    result_lines.append(line[:w])
                    result_breaks.append(line_break_symbol)
                    line = line[w:]

    if height and len(result_lines) > height:
        result_lines = result_lines[:height]
        result_breaks = result_breaks[:height]
        result_breaks[-1] = cell_break_symbol

    return result_lines, result_breaks


def fill_line(
    rows: List[List[str]],
    symbols: List[List[str]],
    widths: List[int],
    align: Tuple[str, ...],
) -> str:
    """

    :param rows:
    :param symbols:
    :param widths:
    :param align:
    :return:
    """
    # noinspection PyTypeChecker
    align_left, align_right = map(
        list, zip(*(a * 2 if len(a) == 1 else a for a in align))
    )

    if isinstance(rows[0], tuple):
        rows = list(map(list, rows))  # noqa

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
            align = align_left
        else:
            align = align_right

        def get_width(index: int):
            return widths[index] - (
                get_text_width_in_console(row[index]) - len(row[index])
            )

        template = "|" + "".join(
            f" {{:{align[cn]}{get_width(cn)}}}{symbol[rn][cn]}|"
            for cn in range(len(row))
        )
        lines.append(template.format(*row))

    return "\n".join(lines)
