import sqlite3
from io import StringIO

from table2string import stringify_table, Table, Themes
from table2string.utils import (
    decrease_numbers,
    transform_align,
    transform_width,
    line_spliter,
    fill_line,
)


def test_decrease_numbers():
    assert decrease_numbers([2, 2, 3], 10) == [3, 3, 4]
    assert decrease_numbers([2, 2, 3], 11) == [3, 3, 5]
    assert decrease_numbers([20, 2, 3], 10) == [8, 1, 1]
    assert decrease_numbers([20, 2, 3], 100) == [80, 8, 12]


def test_transform_align():
    assert transform_align(2, "*") == ("*", "*")
    assert transform_align(2, "<>") == ("<>", "<>")
    assert transform_align(3, "<") == ("<", "<", "<")
    assert transform_align(2, ("*",)) == ("*", "*")
    assert transform_align(2, ("<>",)) == ("<>", "*")
    assert transform_align(3, ("<",)) == ("<", "*", "*")
    assert transform_align(3, ("<", "<", "<")) == ("<", "<", "<")


def test_transform_width():
    assert transform_width(1, 1, [1]) == [1]
    assert transform_width(1, 2, [2, 2]) == [1, 1]
    assert transform_width((1, 2), 1, [1]) == [1]
    assert transform_width((1, 2), 2, [2, 2]) == [1, 2]
    assert transform_width((3, 2), 2, [2, 2]) == [3, 2]


def test_line_spliter():
    assert line_spliter("", 1) == [[" "], [" "]]
    assert line_spliter("1", 1) == [["1"], [" "]]
    assert line_spliter("123\n456", 1) == [
        ["1", "2", "3", "4", "5", "6"],
        ["↩", "↩", " ", "↩", "↩", " "],
    ]
    assert line_spliter("123\n\n456", 1) == [
        ["1", "2", "3", " ", "4", "5", "6"],
        ["↩", "↩", " ", " ", "↩", "↩", " "],
    ]
    assert line_spliter("123\n456", 2) == [["12", "3", "45", "6"], ["↩", " ", "↩", " "]]
    assert line_spliter("123\n456", 3) == [["123", "456"], [" ", " "]]
    assert line_spliter("123\n\n456", 3) == [["123", " ", "456"], [" ", " ", " "]]

    assert line_spliter(
        text="123\n456\n789",
        width=3,
        height=2,
    ) == [["123", "456"], [" ", "…"]]

    assert line_spliter(
        text="123\n456\n789",
        width=3,
        height=3,
    ) == [["123", "456", "789"], [" ", " ", " "]]

    assert line_spliter(
        text="123\n456",
        width=3,
        height=3,
    ) == [["123", "456"], [" ", " "]]
    assert line_spliter(text="12345\n123456\n1") == [
        ["12345", "123456", "1"],
        [" ", " ", " "],
    ]


def test_fill_line():
    assert (
        fill_line(
            [["1", "2", "3", "4", "5", "6"]],
            [["↩", "↩", " ", "↩", "↩", " "]],
            [1],
            ("<",),
        )
        == """
| 1↩|
| 2↩|
| 3 |
| 4↩|
| 5↩|
| 6 |
""".strip()
    )
    assert (
        fill_line(
            [["1", "2", "3", " ", "4", "5", "6"]],
            [["↩", "↩", " ", " ", "↩", "↩", " "]],
            [1],
            ("<",),
        )
        == """
| 1↩|
| 2↩|
| 3 |
|   |
| 4↩|
| 5↩|
| 6 |
""".strip()
    )
    assert (
        fill_line([["12", "3", "45", "6"]], [["↩", " ", "↩", " "]], [2], ("<",))
        == """
| 12↩|
| 3  |
| 45↩|
| 6  |
""".strip()
    )
    assert (
        fill_line([["12", "3", "45", "6"]], [["↩", " ", "↩", " "]], [2], (">",))
        == """
| 12↩|
|  3 |
| 45↩|
|  6 |
""".strip()
    )
    assert (
        fill_line([["123", "456"]], [[" ", " "]], [3], ("<",))
        == """
| 123 |
| 456 |
""".strip()
    )
    assert (
        fill_line([["123"], ["456"]], [[" "], [" "]], [3, 3], ("<", "<"))
        == "| 123 | 456 |"
    )
    assert (
        fill_line([["1234567", "34", "787878"]], [[" ", " ", " "]], [11], ("^<",))
        == """
|   1234567   |
|   34        |
|   787878    |
""".strip()
    )
    assert (
        fill_line([["1234567", "34", "787878"]], [[" ", " ", " "]], [12], ("^<",))
        == """
|   1234567    |
|   34         |
|   787878     |
""".strip()
    )
    assert (
        fill_line([["1234567", "34", "787878"]], [[" ", " ", " "]], [13], ("^<",))
        == """
|    1234567    |
|    34         |
|    787878     |
""".strip()
    )
    assert (
        fill_line([["1234567", "34", "787878"]], [[" ", " ", " "]], [11], ("^>",))
        == """
|   1234567   |
|        34   |
|    787878   |
""".strip()
    )
    assert (
        fill_line([["1234567", "34", "787878"]], [[" ", " ", " "]], [12], ("^>",))
        == """
|   1234567    |
|        34    |
|    787878    |
""".strip()
    )
    assert (
        fill_line([["34", "1234567", "787878"]], [[" ", " ", " "]], [11], ("^<",))
        == """
|   34        |
|   1234567   |
|   787878    |
""".strip()
    )
    assert (
        fill_line([["34", "1234567", "787878"]], [[" ", " ", " "]], [12], ("^<",))
        == """
|   34         |
|   1234567    |
|   787878     |
""".strip()
    )
    assert (
        fill_line([["34", "1234567", "787878"]], [[" ", " ", " "]], [11], ("^>",))
        == """
|        34   |
|   1234567   |
|    787878   |
""".strip()
    )
    assert (
        fill_line([["34", "1234567", "787878"]], [[" ", " ", " "]], [12], ("^>",))
        == """
|        34    |
|   1234567    |
|    787878    |
""".strip()
    )


def test_stringify_table():
    table_1 = [("1", "2", "3"), ("123", "456\n567", "")]
    assert (
        stringify_table(table_1)
        == """
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| 123 | 456 |   |
|     | 567 |   |
+-----+-----+---+
""".strip()
    )
    table_2 = [("1", "2", "3"), ("12345", "456\n\n567", ""), ("q", "NULL", "NULL")]
    assert (
        stringify_table(table_2)
        == """
+-------+------+------+
|     1 |    2 |    3 |
+-------+------+------+
| 12345 | 456  |      |
|       |      |      |
|       | 567  |      |
+-------+------+------+
| q     | NULL | NULL |
+-------+------+------+
""".strip()
    )
    assert (
        stringify_table(table_2, align="<", name="Table Name")
        == """
+---------------------+
|     Table Name      |
+-------+------+------+
| 1     | 2    | 3    |
+-------+------+------+
| 12345 | 456  |      |
|       |      |      |
|       | 567  |      |
+-------+------+------+
| q     | NULL | NULL |
+-------+------+------+
""".strip()
    )
    assert (
        stringify_table(table_2, align=">", name="Table Name")
        == """
+---------------------+
|     Table Name      |
+-------+------+------+
|     1 |    2 |    3 |
+-------+------+------+
| 12345 |  456 |      |
|       |      |      |
|       |  567 |      |
+-------+------+------+
|     q | NULL | NULL |
+-------+------+------+
""".strip()
    )
    table_3 = [("coll 1", "coll 2")]
    assert (
        stringify_table(table_3, name="Table\nName", name_align="<")
        == """
+-----------------+
| Table           |
| Name            |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    assert (
        stringify_table(table_3, name="Table\nName", name_align="^")
        == """
+-----------------+
|      Table      |
|      Name       |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    assert (
        stringify_table(table_3, name="Table\nName", name_align=">")
        == """
+-----------------+
|           Table |
|            Name |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    assert (
        stringify_table(table_3, name="Table\nName", name_align="<<")
        == """
+-----------------+
| Table           |
| Name            |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    assert (
        stringify_table(table_3, name="Table\nName", name_align=">>")
        == """
+-----------------+
|           Table |
|            Name |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    assert (
        stringify_table(table_3, name="Table\nName", name_align="<>")
        == """
+-----------------+
| Table           |
|            Name |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    assert (
        stringify_table(table_3, name="Table\nName", name_align="><")
        == """
+-----------------+
|           Table |
| Name            |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".strip()
    )
    table_4 = [("",)]
    assert (
        stringify_table(table_4)
        == """
+---+
|   |
+---+
""".strip()
    )
    table_5 = [("\n1",)]
    assert (
        stringify_table(table_5)
        == """
+---+
|   |
| 1 |
+---+
""".strip()
    )
    table_6 = [("123",)]
    assert (
        stringify_table(table_6, max_width=(1,))
        == """
+---+
| 1↩|
| 2↩|
| 3 |
+---+
""".strip()
    )
    table_7 = [("123",)]
    assert (
        stringify_table(table_7, max_width=(2,))
        == """
+----+
| 12↩|
| 3  |
+----+
""".strip()
    )
    table_7 = [("123",)]
    assert (
        stringify_table(table_7, max_width=(1,), max_height=2)
        == """
+---+
| 1↩|
| 2…|
+---+
""".strip()
    )
    table_8 = [("1",), ("q",), ("👍",)]
    assert (
        stringify_table(table_8)
        == """
+----+
|  1 |
+----+
| q  |
+----+
| 👍 |
+----+
""".strip()
    )
    table_9 = [("123456\n\n789000",)]
    assert (
        stringify_table(table_9, max_width=(3,), max_height=4)
        == """
+-----+
| 123↩|
| 456 |
|     |
| 789…|
+-----+
""".strip()
    )
    table_10 = [("1234567\n\n891\n234",)]
    assert (
        stringify_table(table_10, max_width=(2,), max_height=7)
        == """
+----+
| 12↩|
| 34↩|
| 56↩|
| 7  |
|    |
| 89↩|
| 1 …|
+----+
""".strip()
    )
    table_11 = [("1234567\n\n891\n234", "qwe" * 20)]
    assert (
        stringify_table(table_11, max_width=(2,), max_height=7)
        == """
+----+----+
| 12↩| qw↩|
| 34↩| eq↩|
| 56↩| we↩|
| 7  | qw↩|
|    | eq↩|
| 89↩| we↩|
| 1 …| qw…|
+----+----+
""".strip()
    )
    table_12 = [("long string",), ("1234567\n34\n787878",)]
    assert (
        stringify_table(table_12, align="^<")
        == """
+-------------+
| long string |
+-------------+
|   1234567   |
|   34        |
|   787878    |
+-------------+
""".strip()
    )
    table_13 = [
        ("filler " * 10,),
        (
            """
We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of
You wouldn't get this from any other guy

I just wanna tell you how I'm feeling
Gotta make you understand

Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
""".strip(),
        ),
    ]
    assert (
        stringify_table(table_13, align="^<")
        == """
+------------------------------------------------------------------------+
| filler filler filler filler filler filler filler filler filler filler  |
+------------------------------------------------------------------------+
|                We're no strangers to love                              |
|                You know the rules and so do I (do I)                   |
|                A full commitment's what I'm thinking of                |
|                You wouldn't get this from any other guy                |
|                                                                        |
|                I just wanna tell you how I'm feeling                   |
|                Gotta make you understand                               |
|                                                                        |
|                Never gonna give you up                                 |
|                Never gonna let you down                                |
|                Never gonna run around and desert you                   |
|                Never gonna make you cry                                |
|                Never gonna say goodbye                                 |
|                Never gonna tell a lie and hurt you                     |
+------------------------------------------------------------------------+
""".strip()
    )
    assert (
        stringify_table(table_13, align="^>")
        == """
+------------------------------------------------------------------------+
| filler filler filler filler filler filler filler filler filler filler  |
+------------------------------------------------------------------------+
|                              We're no strangers to love                |
|                   You know the rules and so do I (do I)                |
|                A full commitment's what I'm thinking of                |
|                You wouldn't get this from any other guy                |
|                                                                        |
|                   I just wanna tell you how I'm feeling                |
|                               Gotta make you understand                |
|                                                                        |
|                                 Never gonna give you up                |
|                                Never gonna let you down                |
|                   Never gonna run around and desert you                |
|                                Never gonna make you cry                |
|                                 Never gonna say goodbye                |
|                     Never gonna tell a lie and hurt you                |
+------------------------------------------------------------------------+
""".strip()
    )
    assert (
        stringify_table(table_13, align="^>", max_width=20)
        == """
+------------------+
| filler filler fi↩|
| ller filler fill↩|
| er filler filler↩|
|  filler filler f↩|
|           iller  |
+------------------+
| We're no strange↩|
|       rs to love |
| You know the rul↩|
| es and so do I (↩|
|            do I) |
| A full commitmen↩|
| t's what I'm thi↩|
|         nking of |
| You wouldn't get↩|
|  this from any o↩|
|         ther guy |
|                  |
| I just wanna tel↩|
| l you how I'm fe↩|
|            eling |
| Gotta make you u↩|
|        nderstand |
|                  |
| Never gonna give↩|
|           you up |
| Never gonna let ↩|
|         you down |
| Never gonna run ↩|
| around and deser↩|
|            t you |
| Never gonna make↩|
|          you cry |
| Never gonna say ↩|
|          goodbye |
| Never gonna tell↩|
|  a lie and hurt ↩|
|              you |
+------------------+
""".strip()
    )
    assert (
        stringify_table(table_13[:1], name=table_13[1][0], name_align="^<")
        == """
+------------------------------------------------------------------------+
|                We're no strangers to love                              |
|                You know the rules and so do I (do I)                   |
|                A full commitment's what I'm thinking of                |
|                You wouldn't get this from any other guy                |
|                                                                        |
|                I just wanna tell you how I'm feeling                   |
|                Gotta make you understand                               |
|                                                                        |
|                Never gonna give you up                                 |
|                Never gonna let you down                                |
|                Never gonna run around and desert you                   |
|                Never gonna make you cry                                |
|                Never gonna say goodbye                                 |
|                Never gonna tell a lie and hurt you                     |
+------------------------------------------------------------------------+
| filler filler filler filler filler filler filler filler filler filler  |
+------------------------------------------------------------------------+
""".strip()
    )
    table_14 = [("filler " * 2,), ("12345\n67890",)]
    assert (
        stringify_table(table_14, align="<>")
        == """
+----------------+
| filler filler  |
+----------------+
| 12345          |
|          67890 |
+----------------+
""".strip()
    )
    assert (
        stringify_table(table_14, align="><")
        == """
+----------------+
| filler filler  |
+----------------+
|          12345 |
| 67890          |
+----------------+
""".strip()
    )
    table_15 = [("qwe", "rty\nuio"), ("123456\n\n789000", "example")]
    kwargs = {
        "max_width": (3, 4),
        "max_height": 4,
        "line_break_symbol": "\\",
        "cell_break_symbol": "/",
    }
    assert (
        stringify_table(table_15, **kwargs, sep=True)
        == """
+-----+------+
| qwe | rty  |
|     | uio  |
+-----+------+
| 123\\| exam\\|
| 456 | ple  |
|     |      |
| 789/|      |
+-----+------+
""".strip()
    )
    assert (
        stringify_table(table_15, **kwargs, sep=False)
        == """
+-----+------+
| qwe | rty  |
|     | uio  |
| 123\\| exam\\|
| 456 | ple  |
|     |      |
| 789/|      |
+-----+------+
""".strip()
    )
    table_16 = [("1", "2"), ("3", "4")]
    assert (
        stringify_table(table_16, sep=True, name="Name")
        == """
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
+---+---+
""".strip()
    )
    assert (
        stringify_table(table_16, sep=False, name="Name")
        == """
+-------+
| Name  |
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
""".strip()
    )
    table_17 = [("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")]
    assert (
        stringify_table(table_17, sep=(1,))
        == """
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |
+---+---+
""".strip()
    )
    assert (
        stringify_table(table_17, sep=(2,))
        == """
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
| 5 | 6 |
| 7 | 8 |
+---+---+
""".strip()
    )
    assert (
        stringify_table(table_17, sep=(1, 3))
        == """
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
+---+---+
| 7 | 8 |
+---+---+
""".strip()
    )
    assert (
        stringify_table(table_17, sep=(1,), name="Name")
        == """
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |
+---+---+
""".strip()
    )
    assert (
        stringify_table(table_17, sep=(2,), name="Name")
        == """
+-------+
| Name  |
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
| 5 | 6 |
| 7 | 8 |
+---+---+
""".strip()
    )
    assert (
        stringify_table(table_17, sep=(1, 3), name="Name")
        == """
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
+---+---+
| 7 | 8 |
+---+---+
""".strip()
    )
    table_18 = [("123\n456\n789",)]
    assert (
        stringify_table(
            table=table_18,
            max_width=(3,),
            max_height=3,
        )
        == stringify_table(
            table=table_18,
            max_width=(3,),
            max_height=3,
            maximize_height=True,
        )
        == """
+-----+
| 123 |
| 456 |
| 789 |
+-----+
""".strip()
    )
    assert (
        stringify_table(
            table=table_18,
            max_width=(3,),
            max_height=2,
            maximize_height=True,
        )
        == """
+-----+
| 123 |
| 456…|
+-----+
""".strip()
    )
    assert (
        stringify_table(
            table=table_18,
            max_width=(3,),
            max_height=4,
            maximize_height=True,
        )
        == """
+-----+
| 123 |
| 456 |
| 789 |
|     |
+-----+
""".strip()
    )
    assert (
        stringify_table(
            table=table_18,
            max_width=(3,),
            max_height=8,
            maximize_height=True,
        )
        == """
+-----+
| 123 |
| 456 |
| 789 |
|     |
|     |
|     |
|     |
|     |
+-----+
""".strip()
    )
    assert (
        stringify_table(
            table=[
                ("City name", "Area", "Population", "Annual Rainfall"),
                ("Adelaide", 1295, 1158259, 600.5),
                ("Brisbane", 5905, 1857594, 1146.4),
                ("Darwin", 112, 120900, 1714.7),
                ("Hobart", 1357, 205556, 619.5),
                ("Sydney", 2058, 4336374, 1214.8),
                ("Melbourne", 1566, 3806092, 646.9),
                ("Perth", 5386, 1554769, 869.4),
            ],
            sep=(1,),
        )
        == """
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Adelaide  | 1295 |    1158259 |           600.5 |
| Brisbane  | 5905 |    1857594 |          1146.4 |
| Darwin    |  112 |     120900 |          1714.7 |
| Hobart    | 1357 |     205556 |           619.5 |
| Sydney    | 2058 |    4336374 |          1214.8 |
| Melbourne | 1566 |    3806092 |           646.9 |
| Perth     | 5386 |    1554769 |           869.4 |
+-----------+------+------------+-----------------+
""".strip()
    )
    assert (
        stringify_table(
            table=[
                ("City name", "Area", "Population", "Annual Rainfall"),
                *sorted(
                    [
                        ("Adelaide", 1295, 1158259, 600.5),
                        ("Brisbane", 5905, 1857594, 1146.4),
                        ("Darwin", 112, 120900, 1714.7),
                        ("Hobart", 1357, 205556, 619.5),
                        ("Sydney", 2058, 4336374, 1214.8),
                        ("Melbourne", 1566, 3806092, 646.9),
                        ("Perth", 5386, 1554769, 869.4),
                    ],
                    key=lambda x: x[3],
                ),
            ],
            sep=(1, 5),
        )
        == """
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Adelaide  | 1295 |    1158259 |           600.5 |
| Hobart    | 1357 |     205556 |           619.5 |
| Melbourne | 1566 |    3806092 |           646.9 |
| Perth     | 5386 |    1554769 |           869.4 |
+-----------+------+------------+-----------------+
| Brisbane  | 5905 |    1857594 |          1146.4 |
| Sydney    | 2058 |    4336374 |          1214.8 |
| Darwin    |  112 |     120900 |          1714.7 |
+-----------+------+------------+-----------------+
""".strip()
    )
    table_19 = [("1", "2", "3"), ("qwe", "rty\nuio", "")]
    name_1 = "Table Name"
    assert (
        stringify_table(table_19, theme=Themes.ascii_thin)
        == """
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_thin, name=name_1)
        == """
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_thin_double)
        == """
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_thin_double, name=name_1)
        == """
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_double)
        == """
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_double, name=name_1)
        == """
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_double_thin)
        == """
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_double_thin, name=name_1)
        == """
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_booktabs)
        == """
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
""".strip(
            "\n"
        )
    )
    assert (
        stringify_table(table_19, theme=Themes.ascii_booktabs, name=name_1)
        == """
 --------------- 
   Table Name    
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
""".strip(
            "\n"
        )
    )
    assert (
        stringify_table(table_19, theme=Themes.thin)
        == """
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thin, name=name_1)
        == """
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thin_thick)
        == """
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thin_thick, name=name_1)
        == """
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thin_double)
        == """
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thin_double, name=name_1)
        == """
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.rounded)
        == """
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.rounded, name=name_1)
        == """
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.rounded_thick)
        == """
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.rounded_thick, name=name_1)
        == """
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.rounded_double)
        == """
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.rounded_double, name=name_1)
        == """
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thick)
        == """
┏━━━━━┳━━━━━┳━━━┓
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thick, name=name_1)
        == """
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thick_thin)
        == """
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┠━━━━━╂━━━━━╂━━━┨
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.thick_thin, name=name_1)
        == """
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┠━━━━━╂━━━━━╂━━━┨
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.double)
        == """
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.double, name=name_1)
        == """
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.double_thin)
        == """
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.double_thin, name=name_1)
        == """
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.booktabs)
        == """
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
""".strip(
            "\n"
        )
    )
    assert (
        stringify_table(table_19, theme=Themes.booktabs, name=name_1)
        == """
 ─────────────── 
   Table Name    
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
""".strip(
            "\n"
        )
    )
    assert (
        stringify_table(table_19, theme=Themes.markdown)
        == """
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |
""".strip()
    )
    assert (
        stringify_table(table_19, theme=Themes.markdown, name=name_1)
        == """
|  Table Name   |
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |
""".strip()
    )
    assert (
        stringify_table(
            table_19, name=name_1, max_width=(10,), max_height=5, maximize_height=True
        )
        == """
+--------------------------------------+
|              Table Name              |
+------------+------------+------------+
|          1 |          2 |          3 |
|            |            |            |
|            |            |            |
|            |            |            |
|            |            |            |
+------------+------------+------------+
| qwe        | rty        |            |
|            | uio        |            |
|            |            |            |
|            |            |            |
|            |            |            |
+------------+------------+------------+
""".strip()
    )


# noinspection PyPep8Naming
def test_Table():
    table_1 = [("1", "2", "3"), ("qwe", "rty\nuio", "")]
    assert (
        Table(table_1, name="Table Name").stringify()
        == """
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    assert (
        Table.from_table(table_1, name="Table Name").stringify()
        == """
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    file_1 = StringIO(
        """
c1,c2,c3
1,2,3
qwe,"rty
uio",
""".strip()
    )
    assert (
        Table.from_csv(file_1, name="Table Name").stringify()
        == """
+----------------+
|   Table Name   |
+-----+-----+----+
| c1  | c2  | c3 |
+-----+-----+----+
|   1 |   2 |  3 |
+-----+-----+----+
| qwe | rty |    |
|     | uio |    |
+-----+-----+----+
    """.strip()
    )
    file_1.seek(0)
    assert (
        Table.from_csv(file_1, name="Table Name", skip_first_line=True).stringify()
        == """
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE data (c1 TEXT, c2 TEXT, c3 TEXT);")
    cursor.executemany(
        "INSERT INTO data (c1, c2, c3) VALUES (?, ?, ?);",
        [("1", "2", "3"), ("qwe", "rty\nuio", "")],
    )
    cursor.execute("SELECT c1, c2, c3 FROM data;")
    assert (
        Table.from_db_cursor(cursor, name="Table Name").stringify()
        == """
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
""".strip()
    )
    cursor.execute("SELECT c1, c2, c3 FROM data;")
    assert (
        Table.from_db_cursor(cursor, name="Table Name", column_names=True).stringify()
        == """
+----------------+
|   Table Name   |
+-----+-----+----+
| c1  | c2  | c3 |
+-----+-----+----+
|   1 |   2 |  3 |
+-----+-----+----+
| qwe | rty |    |
|     | uio |    |
+-----+-----+----+
""".strip()
    )
