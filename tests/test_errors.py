from table2string import Table
from table2string.utils import proportional_change


def test_table2string_errors():
    try:
        Table([]).stringify()
    except ValueError:
        pass

    try:
        Table([(" ",)], column_names=[""]).stringify()
    except ValueError:
        pass

    try:
        Table([(" ",)]).stringify(max_height=0)
    except ValueError:
        pass

    try:
        Table([(" ",)]).stringify(line_break_symbol="")
    except ValueError:
        pass

    try:
        Table([(" ",)]).stringify(line_break_symbol="123")
    except ValueError:
        pass

    try:
        Table([(" ",)]).stringify(cell_break_symbol="")
    except ValueError:
        pass

    try:
        Table([(" ",)]).stringify(cell_break_symbol="123")
    except ValueError:
        pass

    try:
        Table([(" ",)]).stringify(theme=None)  # type: ignore
    except TypeError:
        pass


def test_proportional_change_errors():
    try:
        proportional_change((1, 1, 1), 16, (6, 6, 6))
    except ValueError:
        pass

    try:
        proportional_change((1, 1, 1), 16, (1, 1, 1), proportion_coefficient=-1)
    except ValueError:
        pass

    try:
        proportional_change((1, 1, 1), 16, (1, 1, 1), proportion_coefficient=2.1)
    except ValueError:
        pass


def test_width_errors():
    table = Table(
        [
            ("1", "2", "3"),
            ("3", "4", "5"),
            ("6", Table([("1", "2"), ("3", "4")]), "8"),
            ("9", "10", "11"),
        ],
    )
    try:
        table.stringify(max_width=1)
    except ValueError:
        pass

    try:
        table.stringify(max_width=(1, 1, 1))
    except ValueError:
        pass

    try:
        table.stringify(max_width=(1, -1, 1))
    except ValueError:
        pass

    try:
        table.stringify(max_width=(10, 3, 10))
    except ValueError:
        pass
