from io import StringIO
from typing import Literal

from table2string.utils import (
    AlignType,
    get_text_width_in_console,
    transform_align,
    transform_width,
    line_spliter,
    fill_line,
)


def print_table(
    table,
    align: tuple[AlignType | str, ...] | AlignType | str = "*",
    name: str = None,
    name_align: Literal["<", ">", "^"] | str = None,
    max_width: int | tuple[int, ...] = None,
    max_height: int = None,
    maximize_height: bool = False,
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
    :param maximize_height:
    :param file:
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
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

        if maximize_height:
            max_row_height = max_height
        else:
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
    table,
    align: tuple[AlignType | str, ...] | AlignType | str = "*",
    name: str = None,
    name_align: Literal["<", ">", "^"] | str = None,
    max_width: int | tuple[int, ...] = None,
    max_height: int = None,
    maximize_height: bool = False,
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
    :param maximize_height:
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
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
        maximize_height=maximize_height,
        file=file,
        line_break_symbol=line_break_symbol,
        cell_break_symbol=cell_break_symbol,
        sep=sep,
        end=end,
    )
    file.seek(0)
    return file.read()
