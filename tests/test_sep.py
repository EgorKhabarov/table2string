from table2string import Table, Themes


def test_sep():
    table = Table(
        [
            ("1", "2", "3"),
            ("3", "4", "5"),
            ("6", "7", "8"),
            ("9", "10", "11"),
        ],
    )
    assert (
        table.stringify()
        == """
+---+----+----+
| 1 |  2 |  3 |
+---+----+----+
| 3 |  4 |  5 |
+---+----+----+
| 6 |  7 |  8 |
+---+----+----+
| 9 | 10 | 11 |
+---+----+----+
""".strip()
    )
    assert (
        table.stringify(sep=False)
        == """
+---+----+----+
| 1 |  2 |  3 |
| 3 |  4 |  5 |
| 6 |  7 |  8 |
| 9 | 10 | 11 |
+---+----+----+
""".strip()
    )
    assert (
        table.stringify(sep=range(0, 100, 2))
        == """
+---+----+----+
| 1 |  2 |  3 |
| 3 |  4 |  5 |
+---+----+----+
| 6 |  7 |  8 |
| 9 | 10 | 11 |
+---+----+----+
""".strip()
    )
    assert (
        table.stringify(sep=range(0, 100, 2))
        == """
+---+----+----+
| 1 |  2 |  3 |
| 3 |  4 |  5 |
+---+----+----+
| 6 |  7 |  8 |
| 9 | 10 | 11 |
+---+----+----+
""".strip()
    )
    table_2 = Table(
        [
            ("1", "2", "3"),
            ("3", "4", "5"),
            ("6", "7", "8"),
            ("9", "10", "11"),
        ],
        name="Table Name",
    )
    assert (
        table_2.stringify(sep=False, theme=Themes.thin)
        == """
┌─────────────┐
│ Table Name  │
├───┬────┬────┤
│ 1 │  2 │  3 │
│ 3 │  4 │  5 │
│ 6 │  7 │  8 │
│ 9 │ 10 │ 11 │
└───┴────┴────┘
""".strip()
    )
    table_3 = Table(
        [
            ("1", "2", "3"),
            ("3", "4", "5"),
            ("6", "7", "8"),
            ("9", "10", "11"),
        ],
        column_names=["c1", "c2", "c3"],
    )
    assert (
        table_3.stringify(sep=False, theme=Themes.thin)
        == """
┌────┬────┬────┐
│ c1 │ c2 │ c3 │
├────┼────┼────┤
│  1 │  2 │  3 │
│  3 │  4 │  5 │
│  6 │  7 │  8 │
│  9 │ 10 │ 11 │
└────┴────┴────┘
""".strip()
    )
    table_4 = Table(
        [
            ("1", "2", "3"),
            ("3", "4", "5"),
            ("6", "7", "8"),
            ("9", "10", "11"),
        ],
        name="Table Name",
        column_names=["c1", "c2", "c3"],
    )
    assert (
        table_4.stringify(sep=False, theme=Themes.thin)
        == """
┌──────────────┐
│  Table Name  │
├────┬────┬────┤
│ c1 │ c2 │ c3 │
├────┼────┼────┤
│  1 │  2 │  3 │
│  3 │  4 │  5 │
│  6 │  7 │  8 │
│  9 │ 10 │ 11 │
└────┴────┴────┘
""".strip()
    )
