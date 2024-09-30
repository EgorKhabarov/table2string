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
