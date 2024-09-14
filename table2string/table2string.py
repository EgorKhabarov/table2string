import csv
from io import TextIOWrapper, StringIO
from typing import Union, Tuple, Any, Sequence, List

from table2string.utils import (
    get_text_width_in_console,
    transform_align,
    transform_width,
    ALLOWED_ALIGNS,
    apply_metadata,
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
    column_names: Union[Sequence[str], None] = None,
    column_names_align: Union[Tuple[str, ...], str] = "^",
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
    :param column_names: Column names
    :param column_names_align: Aligns for column names
    :param max_width: Table width or width of individual columns
    :param max_height: The maximum number of lines in one line
    :param maximize_height: Make all lines of the same height max_height
    :param line_break_symbol: "\" or "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param sep: Settings of dividers. You can specify specific lines with dividers.
    :param end: Configure the last symbol of the table. \\n or nothing
    :param file: File where you can record the table by .write method.
    :param theme:
    :param ignore_width_errors:
    :return: None
    """
    table: list[list[Any]] = list(list(row) for row in table)
    assert any(table), table
    assert sum(hasattr(row, "__getitem__") for row in table)
    if column_names is not None:
        assert column_names and column_names[0], column_names

    assert max_height >= 1 if max_height else True, max_height
    assert len(line_break_symbol) == 1, len(line_break_symbol)
    assert len(cell_break_symbol) == 1, len(cell_break_symbol)
    assert isinstance(theme, Theme), type(theme)
    not_allowed_aligns = {
        *((align,) if isinstance(align, str) else align),
        name_align,
        *column_names_align,
    } - set(ALLOWED_ALIGNS)
    assert (
        not not_allowed_aligns
    ), f"not allowed alignments: {tuple(not_allowed_aligns)}"

    column_count = max(map(len, table))

    if column_names:
        column_names = list(column_names)
        column_names_len = len(column_names)

        if column_names_len > column_count:
            column_names = column_names[: column_names_len - 1]
        else:
            column_names.extend((" ",) * (column_count - column_names_len))

        table.insert(0, column_names)

    row_lengths = get_row_lengths(table)
    min_row_lengths = get_row_lengths(table, minimum=True)

    if max_width is not None and not ignore_width_errors:  # TODO ignore_width_errors
        min_width = sum(min_row_lengths) + 3 * len(min_row_lengths) + 1
        if isinstance(max_width, int):
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
            sum_max_width = sum(max_width) + 3 * len(max_width) + 1
            assert sum_max_width >= min_width, f"{sum_max_width} >= {min_width}"

    border = theme.border
    max_widths = transform_width(max_width, column_count, row_lengths)
    align_t = transform_align(column_count, align)
    column_names_align_t = transform_align(column_count, column_names_align)

    horizontally = [(border.horizontal * (i + 2)) for i in max_widths]
    up_separator = "".join(
        (
            border.top_left,
            "".join(horizontally),
            border.horizontal * (len(max_widths) - 1),
            border.top_right,
        )
    )
    under_name_separator = "".join(
        (
            border.vertical_left,
            border.top_horizontal.join(horizontally),
            border.vertical_right,
        )
    )
    up_noname_separator = "".join(
        (
            border.top_left,
            border.top_horizontal.join(horizontally),
            border.top_right,
        )
    )
    line_separator = "".join(
        (
            border.vertical_left,
            border.central.join(horizontally),
            border.vertical_right,
        )
    )
    line_separator_plus = "".join(
        (
            border.vertical_left_plus,
            border.central_plus.join(
                (border.horizontal_plus * (i + 2)) for i in max_widths
            ),
            border.vertical_right_plus,
        )
    )
    down_separator = "".join(
        (
            border.bottom_left,
            border.bottom_horizontal.join(horizontally),
            border.bottom_right,
        )
    )

    """
# EXAMPLE

theme                = Themes.thin_double
up_separator         = "┌───────────┐"
under_name_separator = "├───┬───┬───┤"
up_noname_separator  = "┌───┬───┬───┐"
line_separator       = "├───┼───┼───┤"
line_separator_plus  = "╞═══╪═══╪═══╡"
down_separator       = "└───┴───┴───┘"
    """

    if name:
        name_align_t = transform_align(1, name_align)

        if up_separator.strip():
            print(up_separator, file=file)

        if not max_widths:
            max_name_width = sum(row_lengths) + (3 * column_count) + 1 - 4
        else:
            max_name_width = sum(max_widths) + (3 * column_count) + 1 - 4

        rows, symbols, subtable_columns, metadata_list = zip(
            line_spliter(
                name,
                max_name_width,
                max_height,
                line_break_symbol,
                cell_break_symbol,
            )
        )
        print(
            fill_line(rows, symbols, subtable_columns, metadata_list, [max_name_width], name_align_t, theme),
            file=file,
        )

    # Trimming long lines
    # TODO переделать в table[i] = ...
    def line_spliter_for_sub_table(sub_table: Table, ci: int) -> list[list[str] | bool | dict[str, tuple[str, ...]]]:
        string_sub_table = sub_table.stringify(
            align=align,
            max_width=max_widths[ci] + 4,
            max_height=max_height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
            theme=theme.custom_sub_table_theme,
            ignore_width_errors=True,
        )
        sub_table_lines = string_sub_table.splitlines()
        if max_height:
            sub_table_lines = sub_table_lines[:max_height+2]
        blank_line = ""
        sub_table_symbols = [blank_line for _ in range(len(sub_table_lines))]
        result = [
            [line[1:-1] for line in sub_table_lines[1:-1]],
            sub_table_symbols,
            True,
            {
                "border_top": tuple(sub_table_lines[0][2:-2]),
                "border_bottom": tuple(sub_table_lines[-1][2:-2]),
                "border_left": tuple(line[0] for line in sub_table_lines[1:-1]) or (" ",),
                "border_right": tuple(line[-1] for line in sub_table_lines[1:-1]) or (" ",),
            },
        ]
        return result

    table_g = (
        [
            line_spliter_for_sub_table(cell, ci)
            if isinstance(cell, Table)
            else line_spliter(
                str(cell),
                max_widths[ci],
                max_height,
                line_break_symbol,
                cell_break_symbol,
            )
            for ci, cell in enumerate(row)
        ]
        for row in table
    )
    table_g = list(table_g)
    prev_metadata = None
    result_table = []

    for n, row in enumerate(table_g):  # TODO rename n to ri (row index)
        if n != 0:
            result_table.append(("", "\n"))

        if maximize_height and max_height:
            max_row_height = max_height
        else:
            max_row_height = max(map(len, tuple(zip(*row))[0]))

        for ci, column in enumerate(row):
            if column[2]:  # subtable
                metadata: dict = column[3]
                string = " "+"".join(
                    theme.border.vertical if symbol == theme.border.bottom_horizontal else " "
                    for symbol in metadata["border_bottom"]
                )+" "
                extend_data = (string,) * (max_row_height - len(column[0]))
            else:
                extend_data = (" ",) * (max_row_height - len(column[0]))
            column[0].extend(extend_data)
            column[1].extend(extend_data)

        rows, symbols, subtable_columns, metadata_list = zip(*row)
        if n == 0:
            prev_metadata = metadata_list

        def n_in_sep():
            if column_names:
                return n - 1 in sep
            else:
                return n in sep

        if (
            (sep is True or n == 0)
            or (isinstance(sep, (range, tuple)) and n_in_sep())
            or (n == 1 and column_names)
        ):
            if (name and n == 1) or ((not name) and n == 1):
                s = line_separator_plus
                a = align_t
            elif name and n == 0:
                s = under_name_separator
                a = column_names_align_t if column_names else align_t
            elif (not name) and n == 0:
                s = up_noname_separator
                a = column_names_align_t if column_names else align_t
            else:
                s = line_separator
                a = align_t

            if s.strip():
                s = apply_metadata(s, "border_top", theme, metadata_list, max_widths)
                if n > 0:
                    s = apply_metadata(s, "border_bottom", theme, prev_metadata, max_widths)
                result_table.append((s, "\n"))
        else:
            a = align_t

        result_table.append((fill_line(rows, symbols, subtable_columns, metadata_list, max_widths, a, theme), ""))
        prev_metadata = metadata_list

    if down_separator.strip():
        s = apply_metadata(down_separator.rstrip("\n"), "border_bottom", theme, prev_metadata, max_widths)
        result_table.append(("\n" + s, end))
    elif end:
        result_table.append(("", end))

    for content, end in result_table:
        print(content, file=file, end=end)


def stringify_table(
    table: Sequence[Sequence[Any]],
    *,
    align: Union[Tuple[str, ...], str] = "*",
    name: Union[str, None] = None,
    name_align: str = "^",
    column_names: Union[Sequence[str], None] = None,
    column_names_align: Union[Tuple[str, ...], str] = "^",
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
    :param column_names: Column names
    :param column_names_align: Aligns for column names
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
        column_names=column_names,
        column_names_align=column_names_align,
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
    def __init__(
        self,
        table: Sequence[Sequence[Any]],
        name: Union[str, None] = None,
        column_names: Union[Sequence[str], None] = None,
    ):
        self.table = table
        self.name = name
        self.column_names = column_names

    @classmethod
    def from_table(
        cls,
        table: Sequence[Sequence[Any]],
        name: Union[str, None] = None,
        column_names: Union[Sequence[str], None] = None,
    ) -> "Table":
        return cls(table=table, name=name, column_names=column_names)

    @classmethod
    def from_db_cursor(
        cls,
        cursor,
        name: Union[str, None] = None,
        column_names: bool = False,
    ) -> "Table":
        table = cursor.fetchall()

        if column_names and getattr(cursor, "description"):
            column_names_ = [column[0] for column in cursor.description] or None
        else:
            column_names_ = None

        return cls(table=table, name=name, column_names=column_names_)

    @classmethod
    def from_csv(
        cls,
        file: TextIOWrapper,
        name: Union[str, None] = None,
        column_names: bool = True,
        **kwargs,
    ) -> "Table":
        csv_table = list(csv.reader(file, **kwargs))
        table = csv_table[1:]
        column_names_ = csv_table[0] if column_names else None
        return cls(table=table, name=name, column_names=column_names_)

    def stringify(
        self,
        *,
        align: Union[Tuple[str, ...], str] = "*",
        name_align: str = "^",
        column_names_align: Union[Tuple[str, ...], str] = "^",
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

        :param align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
        :param name_align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
        :param column_names_align: Aligns for column names
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
        return stringify_table(
            table=self.table,
            align=align,
            name=self.name,
            name_align=name_align,
            column_names=self.column_names,
            column_names_align=column_names_align,
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
        column_names_align: Union[Tuple[str, ...], str] = "^",
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

        :param align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
        :param name_align: Can be a line or list, should be from utils.ALLOWED_ALIGNS
        :param column_names_align: Aligns for column names
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
        print_table(
            table=self.table,
            align=align,
            name=self.name,
            name_align=name_align,
            column_names=self.column_names,
            column_names_align=column_names_align,
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

    def __repr__(self):
        return "Table({table}{name}{column_names})".format(
            table=f"{self.table!r}",
            name=f", name={self.name!r}" if self.name else "",
            column_names=f", column_names={self.column_names!r}" if self.column_names else "",
        )


def get_row_lengths(table: Sequence[Sequence], minimum: bool = False) -> List[int]:
    """
    Вычисляет и возвращает список ширин колонок
    Если ячейка матрицы это экземпляр table2string.Table используется рекурсия

    Не в utils.py из-за рекурсивного импорта
    :param table: Two-dimensional matrix
    :param minimum: 1
    """
    row_lengths = [
        max(
            (
                lambda subtable_row_lengths: (sum(subtable_row_lengths) + 3 * len(subtable_row_lengths) + 1)-4
            )(get_row_lengths(cell.table, minimum=minimum))
            if isinstance(cell, Table)
            else 1 if minimum else (
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
    return row_lengths
