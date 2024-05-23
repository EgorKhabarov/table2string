import unicodedata
from io import StringIO
from typing import TypeAlias, Literal


AlignType: TypeAlias = Literal[
    "<", ">", "^", "*", "<<", "<^", "<>", "^<", "^^", "^>", "><", ">^", ">>"
]


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
    row_lengths: list[int], max_width: int = 120, min_value: int = 10
) -> list[int]:
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
    column_count: int, align: tuple[AlignType | str, ...] | AlignType | str = "*"
) -> tuple[AlignType]:
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
    width: int | tuple[int, ...] | None, column_count: int, row_lengths: list[int]
) -> list[int]:
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
    cell_break_symbol: str = "…",  # chr(8230)
) -> tuple[list[str], list[str]]:
    """

    :param text:
    :param width:
    :param height:
    :param line_break_symbol:
    :param cell_break_symbol:
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
    rows: list[list[str]],
    symbols: list[list[str]],
    widths: list[int],
    align: tuple[AlignType | str, ...],
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


def print_table(
    table: list[tuple[str, ...]],
    align: tuple[AlignType | str] | AlignType | str = "*",
    name: str = None,
    name_align: Literal["<", ">", "^"] | str = None,
    max_width: int | tuple[int, ...] = None,
    max_height: int = None,
    file: StringIO = None,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    sep: bool | range | tuple = True,
    end: str | None = "\n",
) -> None:
    """

    :param table:
    :param align:
    :param name:
    :param name_align:
    :param max_width:
    :param max_height:
    :param file:
    :param line_break_symbol:
    :param cell_break_symbol:
    :param sep:
    :param end:
    :return:
    """

    if len(line_break_symbol) != 1:
        raise ValueError("length of line_break_symbol must be 1")

    if len(cell_break_symbol) != 1:
        raise ValueError("length of cell_break_symbol must be 1")

    row_lengths: list[int] = []

    for column in zip(*table):
        cell_widths = []
        for cell in column:
            if cell:
                lines = str(cell).splitlines() or [""]
                cell_width = get_text_width_in_console(
                    max(lines, key=get_text_width_in_console)
                )
                cell_widths.append(cell_width)
            else:
                cell_widths.append(1)

        row_lengths.append(max(cell_widths))

    column_count = max(map(len, table))
    align = transform_align(column_count, align)
    max_widths = transform_width(max_width, column_count, row_lengths)
    line_separator = "+" + "".join(("-" * (i + 2)) + "+" for i in max_widths)

    if name:
        # noinspection PyTypeChecker
        name_align = transform_align(1, name_align or "^")
        print("+" + line_separator.replace("+", "-")[1:-1] + "+", file=file)

        if not max_widths:
            max_name_width: int = sum(row_lengths) + (3 * column_count) + 1 - 4
        else:
            max_name_width = sum(max_widths) + (3 * column_count) + 1 - 4

        rows, symbols = zip(
            line_spliter(
                name, max_name_width, max_height, line_break_symbol, cell_break_symbol
            )
        )
        line = fill_line(rows, symbols, [max_name_width], name_align)
        print(line, file=file)

    # Trimming long lines
    table = (
        [
            line_spliter(
                column, max_widths[n], max_height, line_break_symbol, cell_break_symbol
            )
            for n, column in enumerate(map(str, row))
        ]
        for row in table
    )

    for n, row in enumerate(table):
        if (sep is True or n == 0) or (isinstance(sep, (range, tuple)) and n in sep):
            print(line_separator, file=file)

        max_row_height = max(map(len, tuple(zip(*row))[0]))

        for column in row:
            extend_data = (" ",) * (max_row_height - len(column[0]))
            column[0].extend(extend_data)
            column[1].extend(extend_data)

        rows, symbols = zip(*row)
        line = fill_line(rows, symbols, max_widths, align)
        print(line, file=file)

    print(line_separator.rstrip("\n"), file=file, end=end)


def stringify_table(
    table: list[tuple[str, ...]],
    align: tuple[AlignType | str] | AlignType | str = "*",
    name: str = None,
    name_align: Literal["<", ">", "^"] | str = None,
    max_width: int | tuple[int, ...] = None,
    max_height: int = None,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    sep: bool | range | tuple = True,
    end: str | None = "",
) -> str:
    """

    :param table:
    :param align:
    :param name:
    :param name_align:
    :param max_width:
    :param max_height:
    :param line_break_symbol:
    :param cell_break_symbol:
    :param sep:
    :param end:
    :return:
    """
    file = StringIO()
    print_table(
        table=table,
        align=align,
        name=name,
        name_align=name_align,
        max_width=max_width,
        max_height=max_height,
        file=file,
        line_break_symbol=line_break_symbol,
        cell_break_symbol=cell_break_symbol,
        sep=sep,
        end=end,
    )
    file.seek(0)
    return file.read()
