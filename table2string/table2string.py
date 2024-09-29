import csv
from io import TextIOWrapper, StringIO
from typing import Union, Tuple, Any, Sequence, List, Dict, Optional, Iterable, cast

from table2string.themes import Theme, Themes
from table2string.aligns import HorizontalAlignment, VerticalAlignment
from table2string.utils import (
    get_text_width_in_console,
    split_text_for_sub_table,
    proportional_change,
    apply_border_data,
    generate_borders,
    transform_align,
    transform_width,
    split_text,
    fill_line,
)


def print_table(
    table: Sequence[Sequence[Any]],
    *,
    h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = HorizontalAlignment.AUTO,
    v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = VerticalAlignment.TOP,
    name: Optional[str] = None,
    name_h_align: Union[HorizontalAlignment, str] = HorizontalAlignment.CENTER,
    name_v_align: Union[VerticalAlignment, str] = VerticalAlignment.MIDDLE,
    column_names: Optional[Sequence[str]] = None,
    column_names_h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = HorizontalAlignment.CENTER,
    column_names_v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = VerticalAlignment.MIDDLE,
    max_width: Union[int, Tuple[int, ...], None] = None,
    max_height: Optional[int] = None,
    maximize_height: bool = False,
    line_break_symbol: str = "\\",
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
    :param ignore_width_errors: Fixes errors in max_width if they exist
    :param proportion_coefficient: Reduction coefficient for too large numbers
    :return: None
    """
    list_table: List[List[Union[str, Table, Any]]] = list(list(row) for row in table)
    column_names_list: List[Union[str, Table, Any]] = (
        list(column_names) if column_names else []
    )

    # Raise errors
    if not any(list_table) or not sum(
        hasattr(row, "__getitem__") for row in list_table
    ):
        raise ValueError(list_table)

    if column_names_list != [] and not (column_names_list and column_names_list[0]):
        raise ValueError(column_names_list)

    if not (max_height >= 1 if max_height else True):
        raise ValueError(max_height)

    if len(line_break_symbol) != 1 or not line_break_symbol.isprintable():
        raise ValueError(f"line_break_symbol={line_break_symbol!r}")

    if len(cell_break_symbol) != 1 or not cell_break_symbol.isprintable():
        raise ValueError(f"cell_break_symbol={cell_break_symbol!r}")

    if not isinstance(theme, Theme):
        raise TypeError(theme)

    column_count = max(map(len, list_table))

    # If there are column names, we write them at the beginning of the table
    if column_names_list:
        column_names_len = len(column_names_list)

        if column_names_len > column_count:
            column_names_list = column_names_list[: column_names_len - 1]
        else:
            column_names_list.extend((" ",) * (column_count - column_names_len))

        list_table.insert(0, column_names_list)

    row_widths = get_column_widths(list_table)
    min_row_widths = get_column_widths(list_table, minimum=True)

    if max_width is not None:
        min_width = sum(min_row_widths) + 3 * column_count + 1
        if isinstance(max_width, int):
            if max_width < min_width:
                if ignore_width_errors:
                    max_width = min_width
                else:
                    raise ValueError(f"{max_width} >= {min_width}")
        else:
            invalid_widths = [mw for mw in max_width if mw < 1]
            if invalid_widths:
                if ignore_width_errors:
                    max_width = tuple(1 if mw < 1 else mw for mw in max_width)
                else:
                    raise ValueError(
                        f"Values in {invalid_widths} from max_width are less than one"
                    )
            max_width = max_width[:column_count]
            max_width = (
                *max_width,
                *(max_width[-1],) * (column_count - len(max_width)),
            )
            sum_max_width = sum(max_width) + 3 * column_count + 1
            if sum_max_width < min_width:
                if ignore_width_errors:
                    max_width = proportional_change(
                        row_widths,
                        sum(max_width) + (min_width - sum_max_width),
                    )
                else:
                    raise ValueError(
                        f"{sum_max_width} >= {min_width}: "
                        f"Increase the sum of max_width by {min_width - sum_max_width}"
                    )

            incorrect_max_widths = tuple(
                max_w
                for max_w, min_w in zip(max_width, min_row_widths)
                if max_w < min_w
            )
            if incorrect_max_widths:
                if ignore_width_errors:
                    max_width = tuple(
                        max(max_w, min_w)
                        for max_w, min_w in zip(max_width, min_row_widths)
                    )
                else:
                    raise ValueError(
                        f"Values in {max_width} must be greater than or equal "
                        f"to the corresponding values from {min_row_widths}. "
                        f"Incorrect values: {incorrect_max_widths}"
                    )

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

    rows: Tuple[List[str], ...]
    symbols: Tuple[List[str], ...]
    subtable_columns: Tuple[bool, ...]
    border_data_list: Tuple[Dict[str, Tuple[str, ...]], ...]

    if name:
        if up_separator.strip():
            print(up_separator, file=file)

        if not max_widths:
            max_name_width = sum(row_widths) + (3 * column_count) + 1 - 4
        else:
            max_name_width = sum(max_widths) + (3 * column_count) + 1 - 4

        rows, symbols, subtable_columns, border_data_list = cast(
            Tuple[
                Tuple[List[str], ...],
                Tuple[List[str], ...],
                Tuple[bool, ...],
                Tuple[Dict[str, Tuple[str, ...]], ...],
            ],
            zip(
                split_text(
                    name,
                    max_name_width,
                    max_height,
                    line_break_symbol,
                    cell_break_symbol,
                )
            ),
        )
        print(
            fill_line(
                columns_lines=rows,
                columns_symbols=symbols,
                subtable_columns=subtable_columns,
                border_data_list=border_data_list,
                widths=(max_name_width,),
                h_align=name_h_align_t,
                v_align=name_v_align_t,
                theme=theme,
            ),
            file=file,
        )

    previous_border_data: Tuple[Dict[str, Tuple[str, ...]], ...] = ({"": ("",)},)

    for ri, row in enumerate(list_table):
        if ri != 0:
            print("", file=file, end="\n")

        splitted_row: List[
            Tuple[List[str], List[str], bool, Dict[str, Tuple[str, ...]]]
        ] = []

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
                column_lines = split_text_for_sub_table(string_sub_table, max_height)
            else:
                column_lines = split_text(
                    str(column),
                    max_widths[ci],
                    max_height,
                    line_break_symbol,
                    cell_break_symbol,
                )
            splitted_row.append(column_lines)

        if maximize_height and max_height:
            max_row_height = max_height
        else:
            max_row_height = max(map(len, tuple(zip(*splitted_row))[0]))

        for ci, column in enumerate(splitted_row):
            if column[2]:  # is subtable
                border_data: dict = column[3]
                string = (
                    " "
                    + "".join(
                        (
                            theme.border.vertical
                            if symbol == theme.border.bottom_horizontal
                            else " "
                        )
                        for symbol in border_data["border_bottom"]
                    )
                    + " "
                )
                extend_data = (string,) * (max_row_height - len(column[0]))
            else:
                extend_data = (" ",) * (max_row_height - len(column[0]))
            column[0].extend(extend_data)
            column[1].extend(extend_data)

        rows, symbols, subtable_columns, border_data_list = zip(*splitted_row)

        if (
            (sep is True or ri == 0)  # under table name
            or (column_names_list and ri == 1)  # under column names
            or (
                isinstance(sep, (range, tuple))
                and (ri - 1 in sep if column_names_list else ri in sep)
            )  # if sep allows
        ):
            if ri == 0:
                # separator under table name
                s = under_name_separator if name else up_noname_separator
                ha = column_names_h_align_t if column_names_list else h_align_t
                va = column_names_v_align_t if column_names_list else v_align_t
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
                s = apply_border_data(
                    s, "border_top", theme, border_data_list, max_widths
                )
                # if possible, connect the borders from below.
                if ri > 0:
                    s = apply_border_data(
                        s, "border_bottom", theme, previous_border_data, max_widths
                    )
                print(s, file=file, end="\n")
        else:
            ha, va = h_align_t, v_align_t

        line = fill_line(
            columns_lines=rows,
            columns_symbols=symbols,
            subtable_columns=subtable_columns,
            border_data_list=border_data_list,
            widths=max_widths,
            h_align=ha,
            v_align=va,
            theme=theme,
        )
        print(line, file=file, end="")
        previous_border_data = border_data_list

    if down_separator.strip():
        s = apply_border_data(
            down_separator.rstrip("\n"),
            "border_bottom",
            theme,
            previous_border_data,
            max_widths,
        )
        print("\n" + s, file=file, end=end)
    elif end:
        print("", file=file, end=end)


def stringify_table(
    table: Sequence[Sequence[Any]],
    *,
    h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = HorizontalAlignment.AUTO,
    v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = VerticalAlignment.TOP,
    name: Optional[str] = None,
    name_h_align: Union[HorizontalAlignment, str] = HorizontalAlignment.CENTER,
    name_v_align: Union[VerticalAlignment, str] = VerticalAlignment.MIDDLE,
    column_names: Optional[Sequence[str]] = None,
    column_names_h_align: Union[
        Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
    ] = HorizontalAlignment.CENTER,
    column_names_v_align: Union[
        Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
    ] = VerticalAlignment.MIDDLE,
    max_width: Union[int, Tuple[int, ...], None] = None,
    max_height: Optional[int] = None,
    maximize_height: bool = False,
    line_break_symbol: str = "\\",
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
    :param line_break_symbol: "\" or "↩" or chr(8617) or "\\U000021a9"
    :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
    :param sep: Settings of dividers. You can specify specific lines with dividers.
    :param end: Configure the last symbol of the table. \\n or nothing
    :param theme: Theme
    :param ignore_width_errors: Fixes errors in max_width if they exist
    :param proportion_coefficient: Reduction coefficient for too large numbers
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
        file: Iterable[str],
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
        ] = HorizontalAlignment.AUTO,
        v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = VerticalAlignment.TOP,
        name_h_align: Union[HorizontalAlignment, str] = HorizontalAlignment.CENTER,
        name_v_align: Union[VerticalAlignment, str] = VerticalAlignment.MIDDLE,
        column_names_h_align: Union[
            Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
        ] = HorizontalAlignment.CENTER,
        column_names_v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = VerticalAlignment.MIDDLE,
        max_width: Union[int, Tuple[int, ...], None] = None,
        max_height: Optional[int] = None,
        maximize_height: bool = False,
        line_break_symbol: str = "\\",
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
        :param line_break_symbol: "\" or "↩" or chr(8617) or "\\U000021a9"
        :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
        :param sep: Settings of dividers. You can specify specific lines with dividers.
        :param end: Configure the last symbol of the table. \\n or nothing
        :param theme: Theme
        :param ignore_width_errors: Fixes errors in max_width if they exist
        :param proportion_coefficient: Reduction coefficient for too large numbers
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
        ] = HorizontalAlignment.AUTO,
        v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = VerticalAlignment.TOP,
        name_h_align: Union[HorizontalAlignment, str] = HorizontalAlignment.CENTER,
        name_v_align: Union[VerticalAlignment, str] = VerticalAlignment.MIDDLE,
        column_names_h_align: Union[
            Tuple[Union[HorizontalAlignment, str], ...], Union[HorizontalAlignment, str]
        ] = HorizontalAlignment.CENTER,
        column_names_v_align: Union[
            Tuple[Union[VerticalAlignment, str], ...], Union[VerticalAlignment, str]
        ] = VerticalAlignment.MIDDLE,
        max_width: Union[int, Tuple[int, ...], None] = None,
        max_height: Optional[int] = None,
        maximize_height: bool = False,
        line_break_symbol: str = "\\",
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
        :param line_break_symbol: "\" or "↩" or chr(8617) or "\\U000021a9"
        :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
        :param sep: Settings of dividers. You can specify specific lines with dividers.
        :param end: Configure the last symbol of the table. \\n or nothing
        :param file: File where you can record the table by .write method.
        :param theme: Theme
        :param ignore_width_errors: Fixes errors in max_width if they exist
        :param proportion_coefficient: Reduction coefficient for too large numbers
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
        return "Table({table}{name}{column_names}{kwargs})".format(
            table=f"{self.table!r}",
            name=f", name={self.name!r}" if self.name else "",
            column_names=(
                f", column_names={self.column_names!r}" if self.column_names else ""
            ),
            kwargs=f", **{self.config!r}" if self.config else "",
        )


def get_column_widths(
    table: Sequence[Sequence], minimum: bool = False
) -> Tuple[int, ...]:
    """
    Calculates and returns a list of column widths.
    If the matrix cell is an instance of Table recursion is used

    Not in utils.py due to recursive import
    Uses table2string.Table

    :param table: Two-dimensional matrix
    :param minimum: Forces the function to return the minimum width for each column, which is 1
    """
    row_widths = tuple(
        max(
            (
                (
                    lambda subtable_row_widths: (
                        sum(subtable_row_widths) + 3 * len(subtable_row_widths) + 1
                    )
                    - 4
                )(get_column_widths(cell.table, minimum=minimum))
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
    )
    return row_widths
