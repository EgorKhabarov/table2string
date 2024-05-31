from io import TextIOWrapper, StringIO
from typing import Union, Tuple, Any, Sequence

from table2string.utils import (
    get_text_width_in_console,
    transform_align,
    transform_width,
    line_spliter,
    fill_line,
    BORDERS,
    _Border,
)


def print_table(
    table: Sequence[Sequence[Any]],
    align: Union[Tuple[str, ...], str] = "*",
    name: Union[str, None] = None,
    name_align: str = "^",
    max_width: Union[int, Tuple[int, ...], None] = None,
    max_height: Union[int, None] = None,
    maximize_height: bool = False,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    sep: Union[bool, range, tuple] = True,
    end: Union[str, None] = "\n",
    file: Union[TextIOWrapper, None] = None,
    border: _Border = BORDERS["ascii_thin"],
) -> None:
    """
    Print the table in sys.stdout or file

    :param table: Two-dimensional matrix
    :param align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
    :param name: Table name
    :param name_align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
    :param max_width: Table width or width of individual columns
    :param max_height: The maximum number of lines in one line
    :param maximize_height: Make all lines of the same height max_height
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param sep: Settings of dividers. You can specify specific lines with dividers.
    :param end: Configure the last symbol of the table. \\n or nothing
    :param file: File where you can record the table by .write method.
    :param border:
    :return: None
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

    horizontally = [(border.h * (i + 2)) for i in max_widths]
    up_separator = (
        border.ul + "".join(horizontally) + border.h * (len(max_widths) - 1) + border.ur
    )
    under_name_separator = border.vl + border.uh.join(horizontally) + border.vr
    up_noname_separator = border.ul + border.uh.join(horizontally) + border.ur
    line_separator = border.vl + border.c.join(horizontally) + border.vr
    line_separator_plus = (
        border.vlp
        + border.cp.join((border.hp * (i + 2)) for i in max_widths)
        + border.vrp
    )
    down_separator = border.dl + border.dh.join(horizontally) + border.dr

    if name:
        # noinspection PyTypeChecker
        name_align = transform_align(1, name_align)
        if up_separator.strip():
            print(up_separator, file=file)

        if not max_widths:
            max_name_width: int = sum(row_lengths) + (3 * column_count) + 1 - 4
        else:
            max_name_width = sum(max_widths) + (3 * column_count) + 1 - 4

        rows, symbols = zip(
            line_spliter(
                name, max_name_width, max_height, line_break_symbol, cell_break_symbol
            )
        )
        line = fill_line(rows, symbols, [max_name_width], name_align, border)
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
        if n != 0:
            print(file=file)

        if (sep is True or n == 0) or (isinstance(sep, (range, tuple)) and n in sep):
            if (name and n == 1) or ((not name) and n == 1):
                s = line_separator_plus
            elif name and n == 0:
                s = under_name_separator
            elif (not name) and n == 0:
                s = up_noname_separator
            else:
                s = line_separator

            if s.strip():
                print(s, file=file)

        if maximize_height:
            max_row_height = max_height
        else:
            max_row_height = max(map(len, tuple(zip(*row))[0]))

        for column in row:
            extend_data = (" ",) * (max_row_height - len(column[0]))
            column[0].extend(extend_data)
            column[1].extend(extend_data)

        rows, symbols = zip(*row)
        line = fill_line(rows, symbols, max_widths, align, border)
        print(line, file=file, end="")

    if down_separator.strip():
        print("\n" + down_separator.rstrip("\n"), file=file, end=end)


def stringify_table(
    table: Sequence[Sequence[Any]],
    align: Union[Tuple[str, ...], str] = "*",
    name: Union[str, None] = None,
    name_align: str = "^",
    max_width: Union[int, Tuple[int, ...], None] = None,
    max_height: Union[int, None] = None,
    maximize_height: bool = False,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    sep: Union[bool, range, tuple] = True,
    end: Union[str, None] = "",
    border: _Border = BORDERS["ascii_thin"],
) -> str:
    """

    :param table: Two-dimensional matrix
    :param align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
    :param name: Table name
    :param name_align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
    :param max_width: Table width or width of individual columns
    :param max_height: The maximum number of lines in one line
    :param maximize_height: Make all lines of the same height max_height
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param sep: Settings of dividers. You can specify specific lines with dividers.
    :param end: Configure the last symbol of the table. \\n or nothing
    :param border:
    :return: String table
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
        line_break_symbol=line_break_symbol,
        cell_break_symbol=cell_break_symbol,
        sep=sep,
        end=end,
        file=file,
        border=border,
    )
    file.seek(0)
    return file.read()
