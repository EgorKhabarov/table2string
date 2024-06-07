import csv
from io import TextIOWrapper, StringIO
from typing import Union, Tuple, Any, Sequence

from table2string.utils import (
    get_text_width_in_console,
    transform_align,
    transform_width,
    ALLOWED_ALIGNS,
    line_spliter,
    fill_line,
    Themes,
    Theme,
)


def print_table(
    table: Sequence[Sequence[Any]],
    *,
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
    theme: Theme = Themes.ascii_thin,
    ignore_width_errors: bool = False,
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
    :param theme:
    :param ignore_width_errors:
    :return: None
    """
    assert any(table), table
    assert sum(hasattr(row, "__getitem__") for row in table)
    assert max_height >= 1 if max_height else True, max_height
    assert len(line_break_symbol) == 1, len(line_break_symbol)
    assert len(cell_break_symbol) == 1, len(cell_break_symbol)
    assert isinstance(theme, Theme), type(theme)
    not_allowed_aligns = {
        *((align,) if isinstance(align, str) else align),
        name_align,
    } - set(ALLOWED_ALIGNS)
    assert not not_allowed_aligns, not_allowed_aligns

    column_count = max(map(len, table))

    if max_width is not None and not ignore_width_errors:
        if isinstance(max_width, int):
            min_width = column_count * 4 + 1
            assert max_width >= min_width, f"{max_width} >= {min_width}"
        else:
            assert not [mw for mw in max_width if mw < 1], [
                mw for mw in max_width if mw < 1
            ]
            max_width = max_width[:column_count]
            max_width = (
                *max_width,
                *(max_width[-1],) * (column_count - len(max_width)),
            )
            min_width = column_count
            assert sum(max_width) >= min_width, f"{sum(max_width)} >= {min_width}"

    table = list(table)
    border = theme.border
    row_lengths = [
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

    max_widths = transform_width(max_width, column_count, row_lengths)
    align_t = transform_align(column_count, align)

    horizontally = [(border.horizontal * (i + 2)) for i in max_widths]
    up_separator = (
        border.top_left
        + "".join(horizontally)
        + border.horizontal * (len(max_widths) - 1)
        + border.top_right
    )
    under_name_separator = (
        border.vertical_left
        + border.top_horizontal.join(horizontally)
        + border.vertical_right
    )
    up_noname_separator = (
        border.top_left + border.top_horizontal.join(horizontally) + border.top_right
    )
    line_separator = (
        border.vertical_left + border.central.join(horizontally) + border.vertical_right
    )
    line_separator_plus = (
        border.vertical_left_plus
        + border.central_plus.join(
            (border.horizontal_plus * (i + 2)) for i in max_widths
        )
        + border.vertical_right_plus
    )
    down_separator = (
        border.bottom_left
        + border.bottom_horizontal.join(horizontally)
        + border.bottom_right
    )

    if name:
        name_align_t = transform_align(1, name_align)

        if up_separator.strip():
            print(up_separator, file=file)

        if not max_widths:
            max_name_width = sum(row_lengths) + (3 * column_count) + 1 - 4
        else:
            max_name_width = sum(max_widths) + (3 * column_count) + 1 - 4

        rows, symbols = zip(
            line_spliter(
                name,
                max_name_width,
                max_height,
                line_break_symbol,
                cell_break_symbol,
            )
        )
        print(
            fill_line(rows, symbols, [max_name_width], name_align_t, theme), file=file
        )

    # Trimming long lines
    table_g = (
        [
            line_spliter(
                column,
                max_widths[n],
                max_height,
                line_break_symbol,
                cell_break_symbol,
            )
            for n, column in enumerate(map(str, row))
        ]
        for row in table
    )

    for n, row in enumerate(table_g):
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

        if maximize_height and max_height:
            max_row_height = max_height
        else:
            max_row_height = max(map(len, tuple(zip(*row))[0]))

        for column in row:
            extend_data = (" ",) * (max_row_height - len(column[0]))
            column[0].extend(extend_data)
            column[1].extend(extend_data)

        rows, symbols = zip(*row)
        print(fill_line(rows, symbols, max_widths, align_t, theme), file=file, end="")

    if down_separator.strip():
        print("\n" + down_separator.rstrip("\n"), file=file, end=end)


def stringify_table(
    table: Sequence[Sequence[Any]],
    *,
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
    theme: Theme = Themes.ascii_thin,
    ignore_width_errors: bool = False,
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
    :param theme:
    :param ignore_width_errors:
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
        theme=theme,
        ignore_width_errors=ignore_width_errors,
    )
    file.seek(0)
    return file.read()


class Table:
    def __init__(self, table: Sequence[Sequence[Any]], name: Union[str, None] = None):
        self.table = table
        self.name = name

    @classmethod
    def from_table(
        cls, table: Sequence[Sequence[Any]], name: Union[str, None] = None
    ) -> "Table":
        return cls(table=table, name=name)

    @classmethod
    def from_db_cursor(
        cls, cursor, name: Union[str, None] = None, column_names: bool = False
    ) -> "Table":
        table = cursor.fetchall()

        if column_names and getattr(cursor, "description"):
            table = [[column[0] for column in cursor.description], *table]

        return cls(table=table, name=name)

    @classmethod
    def from_csv(
        cls,
        file: TextIOWrapper,
        name: Union[str, None] = None,
        skip_first_line: bool = False,
        **kwargs,
    ) -> "Table":
        return cls(table=list(csv.reader(file, **kwargs))[skip_first_line:], name=name)

    def stringify(
        self,
        *,
        align: Union[Tuple[str, ...], str] = "*",
        name_align: str = "^",
        max_width: Union[int, Tuple[int, ...], None] = None,
        max_height: Union[int, None] = None,
        maximize_height: bool = False,
        line_break_symbol: str = "↩",
        cell_break_symbol: str = "…",
        sep: Union[bool, range, tuple] = True,
        end: Union[str, None] = "",
        theme: Theme = Themes.ascii_thin,
        ignore_width_errors: bool = False,
    ) -> str:
        return stringify_table(
            table=self.table,
            align=align,
            name=self.name,
            name_align=name_align,
            max_width=max_width,
            max_height=max_height,
            maximize_height=maximize_height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
            sep=sep,
            end=end,
            theme=theme,
            ignore_width_errors=ignore_width_errors,
        )

    def print(
        self,
        *,
        align: Union[Tuple[str, ...], str] = "*",
        name_align: str = "^",
        max_width: Union[int, Tuple[int, ...], None] = None,
        max_height: Union[int, None] = None,
        maximize_height: bool = False,
        line_break_symbol: str = "↩",
        cell_break_symbol: str = "…",
        sep: Union[bool, range, tuple] = True,
        end: Union[str, None] = "\n",
        file: Union[TextIOWrapper, None] = None,
        theme: Theme = Themes.ascii_thin,
        ignore_width_errors: bool = False,
    ) -> None:
        print_table(
            table=self.table,
            align=align,
            name=self.name,
            name_align=name_align,
            max_width=max_width,
            max_height=max_height,
            maximize_height=maximize_height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
            sep=sep,
            end=end,
            file=file,
            theme=theme,
            ignore_width_errors=ignore_width_errors,
        )

    def __str__(self):
        return self.stringify()
