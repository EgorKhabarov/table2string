from io import StringIO
from typing import Callable

from table2string.table2string import (
    decrease_numbers,
    transform_align,
    transform_width,
    line_spliter,
    print_table,
    fill_line,
)


def test_decrease_numbers():
    assert decrease_numbers([2, 2, 3], 10) == [3, 3, 4]
    assert decrease_numbers([2, 2, 3], 11) == [3, 4, 4]
    assert decrease_numbers([20, 2, 3], 10) == [3, 3, 4]
    assert decrease_numbers([20, 2, 3], 100) == [44, 27, 27]


def test_transform_align():
    assert transform_align(2, "*") == ("*", "*")
    assert transform_align(2, "<>") == ("<>", "<>")
    assert transform_align(3, "<") == ("<", "<", "<")
    assert transform_align(2, ("*",)) == ("*", "*")
    assert transform_align(2, ("<>",)) == ("<>", "*")
    assert transform_align(3, ("<",)) == ("<", "*", "*")
    assert transform_align(3, ("<", "<", "<")) == ("<", "<", "<")


def test_transform_width():
    assert transform_width(1, 1, [1]) == [0]
    assert transform_width(1, 2, [2, 2]) == [1, 1]
    assert transform_width((1, 2), 1, [1]) == [6]
    assert transform_width((1, 2), 2, [2, 2]) == [1, 2]


def test_line_spliter():
    assert line_spliter("", 1) == ([" "], [" "])
    assert line_spliter("1", 1) == (["1"], [" "])
    assert line_spliter("123\n456", 1) == (
        ["1", "2", "3", "4", "5", "6"],
        ["↩", "↩", " ", "↩", "↩", " "],
    )
    assert line_spliter("123\n\n456", 1) == (
        ["1", "2", "3", " ", "4", "5", "6"],
        ["↩", "↩", " ", " ", "↩", "↩", " "],
    )
    assert line_spliter("123\n456", 2) == (["12", "3", "45", "6"], ["↩", " ", "↩", " "])
    assert line_spliter("123\n456", 3) == (["123", "456"], [" ", " "])
    assert line_spliter("123\n\n456", 3) == (["123", " ", "456"], [" ", " ", " "])


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


def test_print_table():
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            file = StringIO()
            func(*args, **kwargs, file=file)
            file.seek(0)
            return file.read()

        return wrapper

    get_table = decorator(print_table)
    table_1 = [(1, 2, 3), ("123", "456\n567", "")]
    assert (
        get_table(table_1)
        == """
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| 123 | 456 |   |
|     | 567 |   |
+-----+-----+---+
""".lstrip()
    )
    table_2 = [(1, 2, 3), ("12345", "456\n\n567", ""), ("q", "NULL", "NULL")]
    assert (
        get_table(table_2)
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
""".lstrip()
    )
    assert (
        get_table(table_2, align="<", name="Table Name")
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
""".lstrip()
    )
    assert (
        get_table(table_2, align=">", name="Table Name")
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
""".lstrip()
    )
    table_3 = [("coll 1", "coll 2")]
    assert (
        get_table(table_3, name="Table\nName", name_align="<")
        == """
+-----------------+
| Table           |
| Name            |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    assert (
        get_table(table_3, name="Table\nName", name_align="^")
        == """
+-----------------+
|      Table      |
|      Name       |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    assert (
        get_table(table_3, name="Table\nName", name_align=">")
        == """
+-----------------+
|           Table |
|            Name |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    assert (
        get_table(table_3, name="Table\nName", name_align="<<")
        == """
+-----------------+
| Table           |
| Name            |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    assert (
        get_table(table_3, name="Table\nName", name_align=">>")
        == """
+-----------------+
|           Table |
|            Name |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    assert (
        get_table(table_3, name="Table\nName", name_align="<>")
        == """
+-----------------+
| Table           |
|            Name |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    assert (
        get_table(table_3, name="Table\nName", name_align="><")
        == """
+-----------------+
|           Table |
| Name            |
+--------+--------+
| coll 1 | coll 2 |
+--------+--------+
""".lstrip()
    )
    table_4 = [("",)]
    assert (
        get_table(table_4)
        == """
+---+
|   |
+---+
""".lstrip()
    )
    table_5 = [("\n1",)]
    assert (
        get_table(table_5)
        == """
+---+
|   |
| 1 |
+---+
""".lstrip()
    )
    table_6 = [("123",)]
    assert (
        get_table(table_6, max_width=1)
        == """
+---+
| 1↩|
| 2↩|
| 3 |
+---+
""".lstrip()
    )
    table_7 = [("123",)]
    assert (
        get_table(table_7, max_width=(2,))
        == """
+----+
| 12↩|
| 3  |
+----+
""".lstrip()
    )
    table_7 = [("123",)]
    assert (
        get_table(table_7, max_width=(1,), max_height=2)
        == """
+---+
| 1↩|
| 2…|
+---+
""".lstrip()
    )
    table_8 = [("1",), ("q",), ("👍",)]
    assert (
        get_table(table_8)
        == """
+----+
|  1 |
+----+
| q  |
+----+
| 👍 |
+----+
""".lstrip()
    )
    table_9 = [("123456\n\n789000",)]
    assert (
        get_table(table_9, max_width=(3,), max_height=4)
        == """
+-----+
| 123↩|
| 456 |
|     |
| 789…|
+-----+
""".lstrip()
    )
    table_10 = [("1234567\n\n891\n234",)]
    assert (
        get_table(table_10, max_width=(2,), max_height=7)
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
""".lstrip()
    )
    table_11 = [("1234567\n\n891\n234", "qwe" * 20)]
    assert (
        get_table(table_11, max_width=(2,), max_height=7)
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
""".lstrip()
    )
    table_12 = [("long string",), ("1234567\n34\n787878",)]
    assert (
        get_table(table_12, align="^<")
        == """
+-------------+
| long string |
+-------------+
|   1234567   |
|   34        |
|   787878    |
+-------------+
""".lstrip()
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
        get_table(table_13, align="^<")
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
""".lstrip()
    )
    assert (
        get_table(table_13, align="^>")
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
""".lstrip()
    )
    assert (
        get_table(table_13, align="^>", max_width=20)
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
""".lstrip()
    )
    assert (
        get_table(table_13[:1], name=table_13[1][0], name_align="^<")
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
""".lstrip()
    )
    table_14 = [("filler" * 2,), ("12345\n67890",)]
    assert (
        get_table(table_14, align="<>")
        == """
+--------------+
| fillerfiller |
+--------------+
| 12345        |
|        67890 |
+--------------+
""".lstrip()
    )
    assert (
        get_table(table_14, align="><")
        == """
+--------------+
| fillerfiller |
+--------------+
|        12345 |
| 67890        |
+--------------+
""".lstrip()
    )
