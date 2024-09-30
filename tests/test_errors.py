from table2string import Table


def test_table2string_errors():
    try:
        Table([]).stringify()
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)], column_names=[""]).stringify()
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)]).stringify(max_height=0)
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)]).stringify(line_break_symbol="")
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)]).stringify(line_break_symbol="123")
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)]).stringify(cell_break_symbol="")
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)]).stringify(cell_break_symbol="123")
    except ValueError:
        pass
    else:
        raise

    try:
        Table([(" ",)]).stringify(theme=None)  # type: ignore
    except TypeError:
        pass
    else:
        raise
