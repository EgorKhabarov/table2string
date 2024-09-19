from table2string import Table


def test_widths():
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
        table.stringify(max_width=14)
        == """
+---+---+----+
| 1 | 2 |  3 |
+---+---+----+
| 3 | 4 |  5 |
+---+---+----+
| 6 | 7 |  8 |
+---+---+----+
| 9 | 1↩| 11 |
|   | 0 |    |
+---+---+----+
""".strip()
    )
    assert (
        table.stringify(max_width=15)
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
        table.stringify(max_width=13)
        == """
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
| 3 | 4 | 5 |
+---+---+---+
| 6 | 7 | 8 |
+---+---+---+
| 9 | 1↩| 1↩|
|   | 0 | 1 |
+---+---+---+
""".strip()
    )
    assert (
        table.stringify(max_width=(2, 1, 5))
        == """
+----+---+-------+
|  1 | 2 |     3 |
+----+---+-------+
|  3 | 4 |     5 |
+----+---+-------+
|  6 | 7 |     8 |
+----+---+-------+
|  9 | 1↩|    11 |
|    | 0 |       |
+----+---+-------+
""".strip()
    )
