import csv
from io import TextIOWrapper, StringIO
from typing import Union, Tuple, Any, Sequence, List, Dict, Optional

from table2string.themes import Theme, Themes
from table2string.aligns import HorizontalAlignment, VerticalAlignment
from table2string.utils import (
    line_spliter_for_sub_table,
    get_text_width_in_console,
    generate_borders,
    transform_align,
    transform_width,
    apply_metadata,
    line_spliter,
    fill_line,
)


def print_table(
    table: Sequence[Sequence[Any]],
    *,
    h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = "*",
    v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = "^",
    name: Optional[str] = None,
    name_h_align: Union[HorizontalAlignment, str] = "^",
    name_v_align: Union[VerticalAlignment, str] = "-",
    column_names: Optional[Sequence[str]] = None,
    column_names_h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = "^",
    column_names_v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = "-",
    max_width: Union[int, Tuple[int, ...], None] = None,
    max_height: Optional[int] = None,
    maximize_height: bool = False,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    sep: Union[bool, range, tuple] = True,
    end: Optional[str] = "\n",
    file: Optional[TextIOWrapper] = None,
    theme: Theme = Themes.ascii_thin,
    ignore_width_errors: bool = False,
    proportion_coefficient: float = 0.5,
) -> None:
    """
    Print the table in sys.stdout or file

    :param table: Two-dimensional matrix
    :param h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
    :param v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
    :param name: Table name
    :param name_h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
    :param name_v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
    :param column_names: Column names
    :param column_names_h_align: Horizontal aligns for column names
    :param column_names_v_align: Vertical aligns for column names
    :param max_width: Table width or width of individual columns
    :param max_height: The maximum number of lines in one line
    :param maximize_height: Make all lines of the same height max_height
    :param line_break_symbol: "\" or "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param sep: Settings of dividers. You can specify specific lines with dividers.
    :param end: Configure the last symbol of the table. \\n or nothing
    :param file: File where you can record the table by .write method.
    :param theme: Theme
    :param ignore_width_errors: Raise error when width is not enough
    :param proportion_coefficient: Proportion coefficient
    :return: None
    """
    table_: List[List[Any]] = list(list(row) for row in table)
    column_names_: Optional[List[str]] = list(column_names) if column_names else None

    # Raise errors
    if not any(table_) or not sum(hasattr(row, "__getitem__") for row in table_):
        raise ValueError(table_)

    if column_names_ is not None and not (column_names_ and column_names_[0]):
        raise ValueError(column_names_)

    if not (max_height >= 1 if max_height else True):
        raise ValueError(max_height)

    if len(line_break_symbol) != 1:
        raise ValueError(line_break_symbol)

    if len(cell_break_symbol) != 1:
        raise ValueError(cell_break_symbol)

    if not isinstance(theme, Theme):
        raise TypeError(theme)

    column_count = max(map(len, table_))

    # If there are column names, we write them at the beginning of the table
    if column_names_:
        column_names_len = len(column_names_)

        if column_names_len > column_count:
            column_names_ = column_names_[: column_names_len - 1]
        else:
            column_names_.extend((" ",) * (column_count - column_names_len))

        table_.insert(0, column_names_)

    row_widths = get_row_widths(table_)
    min_row_widths = get_row_widths(table_, minimum=True)

    if max_width is not None and not ignore_width_errors:
        min_width = sum(min_row_widths) + 3 * len(min_row_widths) + 1
        if isinstance(max_width, int):
            if max_width < min_width:
                raise ValueError(f"{max_width} >= {min_width}")
        else:
            invalid_widths = [mw for mw in max_width if mw < 1]
            if invalid_widths:
                raise ValueError(invalid_widths)
            max_width = max_width[:column_count]
            max_width = (
                *max_width,
                *(max_width[-1],) * (column_count - len(max_width)),
            )
            sum_max_width = sum(max_width) + 3 * len(max_width) + 1
            if sum_max_width < min_width:
                raise ValueError(f"{sum_max_width} >= {min_width}")

    h_align_t = transform_align(column_count, h_align)
    name_h_align_t = transform_align(1, name_h_align)
    column_names_h_align_t = transform_align(column_count, column_names_h_align)

    v_align_t = transform_align(column_count, v_align, default="^")
    name_v_align_t = transform_align(1, name_v_align, default="^")
    column_names_v_align_t = transform_align(
        column_count, column_names_v_align, default="^"
    )

    max_widths = transform_width(
        max_width, column_count, row_widths, min_row_widths, proportion_coefficient
    )
    (
        up_separator,
        under_name_separator,
        up_noname_separator,
        line_separator,
        line_separator_plus,
        down_separator,
    ) = generate_borders(theme, max_widths)

    if name:
        if up_separator.strip():
            print(up_separator, file=file)

        if not max_widths:
            max_name_width = sum(row_widths) + (3 * column_count) + 1 - 4
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
            fill_line(
                rows=rows,
                symbols=symbols,
                subtable_columns=subtable_columns,
                metadata_list=metadata_list,
                widths=[max_name_width],
                h_align=name_h_align_t,
                v_align=name_v_align_t,
                theme=theme,
            ),
            file=file,
        )

    prev_metadata = None
    result_table = []

    for ri, row in enumerate(table_):
        if ri != 0:
            result_table.append(("", "\n"))

        # Trimming long lines
        for ci, column in enumerate(row):
            if isinstance(column, Table):
                string_sub_table = column.stringify(
                    h_align=h_align_t[ci],
                    v_align=v_align_t[ci],
                    name_h_align=name_h_align,
                    name_v_align=name_v_align,
                    column_names_h_align=column_names_h_align,
                    column_names_v_align=column_names_v_align,
                    max_width=max_widths[ci] + 4,
                    line_break_symbol=line_break_symbol,
                    cell_break_symbol=cell_break_symbol,
                    theme=theme.custom_sub_table_theme,
                    ignore_width_errors=True,
                    proportion_coefficient=proportion_coefficient,
                )
                column_lines = line_spliter_for_sub_table(string_sub_table, max_height)
            else:
                column_lines = line_spliter(
                    str(column),
                    max_widths[ci],
                    max_height,
                    line_break_symbol,
                    cell_break_symbol,
                )
            row[ci] = column_lines

        if maximize_height and max_height:
            max_row_height = max_height
        else:
            max_row_height = max(map(len, tuple(zip(*row))[0]))

        for ci, column in enumerate(row):
            if column[2]:  # is subtable
                metadata: dict = column[3]
                string = (
                    " "
                    + "".join(
                        (
                            theme.border.vertical
                            if symbol == theme.border.bottom_horizontal
                            else " "
                        )
                        for symbol in metadata["border_bottom"]
                    )
                    + " "
                )
                extend_data = (string,) * (max_row_height - len(column[0]))
            else:
                extend_data = (" ",) * (max_row_height - len(column[0]))
            column[0].extend(extend_data)
            column[1].extend(extend_data)

        rows, symbols, subtable_columns, metadata_list = zip(*row)

        if ri == 0:
            prev_metadata = metadata_list

        if (
            (sep is True or ri == 0)  # under table name
            or (column_names_ and ri == 1)  # under column names
            or (
                isinstance(sep, (range, tuple))
                and (ri - 1 in sep if column_names_ else ri in sep)
            )  # if sep allows
        ):
            if ri == 0:
                # separator under table name
                s = under_name_separator if name else up_noname_separator
                ha = column_names_h_align_t if column_names_ else h_align_t
                va = column_names_v_align_t if column_names_ else v_align_t
            elif ri == 1:
                # separator under column names (if theme supports)
                s = line_separator_plus
                ha, va = h_align_t, v_align_t
            else:
                # normal separator
                s = line_separator
                ha, va = h_align_t, v_align_t

            if s.strip():
                # connect the borders from above
                s = apply_metadata(s, "border_top", theme, metadata_list, max_widths)
                # if possible, connect the borders from below.
                if ri > 0:
                    s = apply_metadata(
                        s, "border_bottom", theme, prev_metadata, max_widths
                    )
                result_table.append((s, "\n"))
        else:
            ha, va = h_align_t, v_align_t

        result_table.append(
            (
                fill_line(
                    rows=rows,
                    symbols=symbols,
                    subtable_columns=subtable_columns,
                    metadata_list=metadata_list,
                    widths=max_widths,
                    h_align=ha,
                    v_align=va,
                    theme=theme,
                ),
                "",
            )
        )
        prev_metadata = metadata_list

    if down_separator.strip():
        s = apply_metadata(
            down_separator.rstrip("\n"),
            "border_bottom",
            theme,
            prev_metadata,
            max_widths,
        )
        result_table.append(("\n" + s, end))
    elif end:
        result_table.append(("", end))

    for content, end in result_table:
        print(content, file=file, end=end)


def stringify_table(
    table: Sequence[Sequence[Any]],
    *,
    h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = "*",
    v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = "^",
    name: Optional[str] = None,
    name_h_align: Union[HorizontalAlignment, str] = "^",
    name_v_align: Union[VerticalAlignment, str] = "-",
    column_names: Optional[Sequence[str]] = None,
    column_names_h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = "^",
    column_names_v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = "-",
    max_width: Union[int, Tuple[int, ...], None] = None,
    max_height: Optional[int] = None,
    maximize_height: bool = False,
    line_break_symbol: str = "↩",
    cell_break_symbol: str = "…",
    sep: Union[bool, range, tuple] = True,
    end: Optional[str] = "",
    theme: Theme = Themes.ascii_thin,
    ignore_width_errors: bool = False,
    proportion_coefficient: float = 0.5,
) -> str:
    """

    :param table: Two-dimensional matrix
    :param h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
    :param v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
    :param name: Table name
    :param name_h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
    :param name_v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
    :param column_names: Column names
    :param column_names_h_align: Horizontal aligns for column names
    :param column_names_v_align: Vertical aligns for column names
    :param max_width: Table width or width of individual columns
    :param max_height: The maximum number of lines in one line
    :param maximize_height: Make all lines of the same height max_height
    :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param sep: Settings of dividers. You can specify specific lines with dividers.
    :param end: Configure the last symbol of the table. \\n or nothing
    :param theme: Theme
    :param ignore_width_errors: Raise error when width is not enough
    :param proportion_coefficient: Proportion coefficient
    :return: String table
    """
    file = StringIO()
    print_table(
        table=table,
        h_align=h_align,
        v_align=v_align,
        name=name,
        name_h_align=name_h_align,
        name_v_align=name_v_align,
        column_names=column_names,
        column_names_h_align=column_names_h_align,
        column_names_v_align=column_names_v_align,
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
        proportion_coefficient=proportion_coefficient,
    )
    file.seek(0)
    return file.read()


class Table:
    def __init__(
        self,
        table: Sequence[Sequence[Any]],
        name: Optional[str] = None,
        column_names: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ):
        self.table = table
        self.name = name
        self.column_names = column_names
        self.config = kwargs

    @classmethod
    def from_table(
        cls,
        table: Sequence[Sequence[Any]],
        name: Optional[str] = None,
        column_names: Optional[Sequence[str]] = None,
        **kwargs: Any,
    ) -> "Table":
        return cls(table=table, name=name, column_names=column_names, **kwargs)

    @classmethod
    def from_db_cursor(
        cls,
        cursor,
        name: Optional[str] = None,
        column_names: bool = False,
        **kwargs: Any,
    ) -> "Table":
        table = cursor.fetchall()

        if column_names and getattr(cursor, "description"):
            column_names_ = [column[0] for column in cursor.description] or None
        else:
            column_names_ = None

        return cls(table=table, name=name, column_names=column_names_, **kwargs)

    @classmethod
    def from_csv(
        cls,
        file: TextIOWrapper,
        name: Optional[str] = None,
        column_names: bool = True,
        reader_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> "Table":
        csv_table = list(csv.reader(file, **reader_kwargs or {}))
        table = csv_table[1:]
        column_names_ = csv_table[0] if column_names else None
        return cls(table=table, name=name, column_names=column_names_, **kwargs)

    def stringify(
        self,
        *,
        h_align: Union[
            Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
        ] = "*",
        v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = "^",
        name_h_align: Union[HorizontalAlignment, str] = "^",
        name_v_align: Union[VerticalAlignment, str] = "-",
        column_names_h_align: Union[
            Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
        ] = "^",
        column_names_v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = "-",
        max_width: Union[int, Tuple[int, ...], None] = None,
        max_height: Optional[int] = None,
        maximize_height: bool = False,
        line_break_symbol: str = "↩",
        cell_break_symbol: str = "…",
        sep: Union[bool, range, tuple] = True,
        end: Optional[str] = "",
        theme: Theme = Themes.ascii_thin,
        ignore_width_errors: bool = False,
        proportion_coefficient: float = 0.5,
    ) -> str:
        """

        :param h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
        :param v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
        :param name_h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
        :param name_v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
        :param column_names_h_align: Horizontal aligns for column names
        :param column_names_v_align: Vertical aligns for column names
        :param max_width: Table width or width of individual columns
        :param max_height: The maximum number of lines in one line
        :param maximize_height: Make all lines of the same height max_height
        :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
        :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
        :param sep: Settings of dividers. You can specify specific lines with dividers.
        :param end: Configure the last symbol of the table. \\n or nothing
        :param theme: Theme
        :param ignore_width_errors: Raise error when width is not enough
        :param proportion_coefficient: Proportion coefficient
        :return: String table
        """
        return stringify_table(
            table=self.table,
            h_align=self.config.get("h_align") or h_align,
            v_align=self.config.get("v_align") or v_align,
            name=self.name,
            name_h_align=self.config.get("name_h_align") or name_h_align,
            name_v_align=self.config.get("name_v_align") or name_v_align,
            column_names=self.column_names,
            column_names_h_align=self.config.get("column_names_h_align")
            or column_names_h_align,
            column_names_v_align=self.config.get("column_names_v_align")
            or column_names_v_align,
            max_width=max_width,
            max_height=self.config.get("max_height") or max_height,
            maximize_height=self.config.get("maximize_height") or maximize_height,
            line_break_symbol=self.config.get("line_break_symbol") or line_break_symbol,
            cell_break_symbol=self.config.get("cell_break_symbol") or cell_break_symbol,
            sep=sep,
            end=end,
            theme=theme,
            ignore_width_errors=ignore_width_errors,
            proportion_coefficient=self.config.get("proportion_coefficient")
            or proportion_coefficient,
        )

    def print(
        self,
        *,
        h_align: Union[
            Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
        ] = "*",
        v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = "^",
        name_h_align: Union[HorizontalAlignment, str] = "^",
        name_v_align: Union[VerticalAlignment, str] = "-",
        column_names_h_align: Union[
            Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
        ] = "^",
        column_names_v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = "-",
        max_width: Union[int, Tuple[int, ...], None] = None,
        max_height: Optional[int] = None,
        maximize_height: bool = False,
        line_break_symbol: str = "↩",
        cell_break_symbol: str = "…",
        sep: Union[bool, range, tuple] = True,
        end: Optional[str] = "\n",
        file: Optional[TextIOWrapper] = None,
        theme: Theme = Themes.ascii_thin,
        ignore_width_errors: bool = False,
        proportion_coefficient: float = 0.5,
    ) -> None:
        """
        Print the table in sys.stdout or file

        :param h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
        :param v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
        :param name_h_align: Can be a line or list, should be from utils.ALLOWED_H_ALIGNS
        :param name_v_align: Can be a line or list, should be from utils.ALLOWED_V_ALIGNS
        :param column_names_h_align: Horizontal aligns for column names
        :param column_names_v_align: Vertical aligns for column names
        :param max_width: Table width or width of individual columns
        :param max_height: The maximum number of lines in one line
        :param maximize_height: Make all lines of the same height max_height
        :param line_break_symbol: "↩" or chr(8617) or "\\U000021a9"
        :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
        :param sep: Settings of dividers. You can specify specific lines with dividers.
        :param end: Configure the last symbol of the table. \\n or nothing
        :param file: File where you can record the table by .write method.
        :param theme: Theme
        :param ignore_width_errors: Raise error when width is not enough
        :param proportion_coefficient: Proportion coefficient
        :return: None
        """
        print_table(
            table=self.table,
            h_align=self.config.get("h_align") or h_align,
            v_align=self.config.get("v_align") or v_align,
            name=self.name,
            name_h_align=self.config.get("name_h_align") or name_h_align,
            name_v_align=self.config.get("name_v_align") or name_v_align,
            column_names=self.column_names,
            column_names_h_align=self.config.get("column_names_h_align")
            or column_names_h_align,
            column_names_v_align=self.config.get("column_names_v_align")
            or column_names_v_align,
            max_width=max_width,
            max_height=self.config.get("max_height") or max_height,
            maximize_height=self.config.get("maximize_height") or maximize_height,
            line_break_symbol=self.config.get("line_break_symbol") or line_break_symbol,
            cell_break_symbol=self.config.get("cell_break_symbol") or cell_break_symbol,
            sep=sep,
            end=end,
            file=file,
            theme=theme,
            ignore_width_errors=ignore_width_errors,
            proportion_coefficient=self.config.get("proportion_coefficient")
            or proportion_coefficient,
        )

    def __str__(self):
        return self.stringify()

    def __repr__(self):
        return "Table({table}{name}{column_names})".format(
            table=f"{self.table!r}",
            name=f", name={self.name!r}" if self.name else "",
            column_names=(
                f", column_names={self.column_names!r}" if self.column_names else ""
            ),
        )


def get_row_widths(table: Sequence[Sequence], minimum: bool = False) -> List[int]:
    """
    Calculates and returns a list of column widths.
    If the matrix cell is an instance of Table recursion is used

    Not in utils.py due to recursive import
    :param table: Two-dimensional matrix
    :param minimum: Forces the function to return the minimum width for each column, which is 1
    """
    row_widths = [
        max(
            (
                (
                    lambda subtable_row_widths: (
                        sum(subtable_row_widths) + 3 * len(subtable_row_widths) + 1
                    )
                    - 4
                )(get_row_widths(cell.table, minimum=minimum))
                if isinstance(cell, Table)
                else (
                    1
                    if minimum
                    else (
                        max(
                            get_text_width_in_console(line)
                            for line in str(cell).splitlines() or [""]
                        )
                        if str(cell)
                        else 1
                    )
                )
            )
            for cell in column
        )
        for ci, column in enumerate(zip(*table))
    ]
    return row_widths
