from table2string.table2string import Table, get_row_widths
from table2string.themes import Themes
from table2string.utils import (
    get_text_width_in_console,
    proportional_change,
    transform_align,
    transform_width,
    apply_metadata,
    apply_v_align,
    line_spliter,
    fill_line,
)


def test_get_text_width_in_console():
    assert get_text_width_in_console("123") == 3
    assert get_text_width_in_console("\U0001f34f\U0001f34e") == 4


def test_proportional_change():
    assert proportional_change([2, 2, 3], 10) == [3, 3, 4]
    assert proportional_change([2, 2, 3], 11) == [3, 3, 5]
    assert proportional_change([20, 2, 3], 10) == [5, 2, 3]
    assert proportional_change([20, 2, 3], 100) == [59, 19, 22]
    assert proportional_change(
        [19, 10, 7, 4, 12, 4, 4, 4, 1, 1168],
        185,
    ) == [7, 8, 8, 9, 9, 10, 10, 12, 13, 99]

    assert proportional_change([9, 6], 6, [5, 1]) == [5, 1]
    assert proportional_change([2, 2, 3], 10, [1, 1, 1]) == [3, 3, 4]
    assert proportional_change([2, 2, 3], 10, [1, 4, 1]) == [2, 4, 4]
    assert proportional_change(
        [19, 10, 7, 4, 12, 4, 4, 4, 1, 1168],
        185,
    ) == [7, 8, 8, 9, 9, 10, 10, 12, 13, 99]
    assert proportional_change(
        [19, 10, 7, 4, 12, 4, 4, 4, 1, 1168],
        185,
        [1, 1, 1, 1, 1, 1, 1, 1, 20, 1],
    ) == [6, 7, 7, 8, 8, 9, 10, 11, 21, 98]
    assert proportional_change([1, 1, 1], 10, [1, 1, 1]) == [4, 3, 3]
    assert proportional_change([1, 1, 1], 11, [1, 1, 1]) == [3, 4, 4]
    assert proportional_change([1, 1, 1], 12, [1, 1, 1]) == [4, 4, 4]
    assert proportional_change([1, 1, 1], 13, [1, 1, 1]) == [5, 4, 4]
    assert proportional_change([1, 1, 1], 14, [1, 1, 1]) == [4, 5, 5]
    assert proportional_change([1, 1, 1], 15, [1, 1, 1]) == [5, 5, 5]
    assert proportional_change([1, 1, 1], 16, [1, 1, 1]) == [5, 5, 6]
    assert proportional_change([1, 1, 1], 16, [1, 9, 6]) == [1, 9, 6]
    assert proportional_change([987654, 10000, 999999], 16, [1, 9, 1]) == [3, 9, 4]


def test_transform_align():
    assert transform_align(2, "*") == ("*", "*")
    assert transform_align(2, "<>") == ("<>", "<>")
    assert transform_align(3, "<") == ("<", "<", "<")
    assert transform_align(2, ("*",)) == ("*", "*")
    assert transform_align(2, ("<>",)) == ("<>", "*")
    assert transform_align(3, ("<",)) == ("<", "*", "*")
    assert transform_align(3, ("<", "<", "<")) == ("<", "<", "<")

    assert transform_align(2, "^", default="^") == ("^", "^")
    assert transform_align(2, "-", default="^") == ("-", "-")
    assert transform_align(3, "_", default="^") == ("_", "_", "_")
    assert transform_align(2, ("^",), default="^") == ("^", "^")
    assert transform_align(2, ("-",), default="^") == ("-", "^")
    assert transform_align(3, ("_",), default="^") == ("_", "^", "^")
    assert transform_align(3, ("^", "-", "_"), default="^") == ("^", "-", "_")


def test_transform_width():
    assert transform_width(1, 1, [1]) == [1]
    assert transform_width(1, 2, [2, 2]) == [1, 1]
    assert transform_width((1, 2), 1, [1]) == [1]
    assert transform_width((1, 2), 2, [2, 2]) == [1, 2]
    assert transform_width((3, 2), 2, [2, 2]) == [3, 2]


def test_line_spliter():
    assert line_spliter("", 1) == [[""], [" "], False, None]
    assert line_spliter("1", 1) == [["1"], [" "], False, None]
    assert line_spliter("123\n456", 1) == [
        ["1", "2", "3", "4", "5", "6"],
        ["↩", "↩", " ", "↩", "↩", " "],
        False,
        None,
    ]
    assert line_spliter("123\n\n456", 1) == [
        ["1", "2", "3", "", "4", "5", "6"],
        ["↩", "↩", " ", " ", "↩", "↩", " "],
        False,
        None,
    ]
    assert line_spliter("123\n456", 2) == [
        ["12", "3", "45", "6"],
        ["↩", " ", "↩", " "],
        False,
        None,
    ]
    assert line_spliter("123\n456", 3) == [["123", "456"], [" ", " "], False, None]
    assert line_spliter("123\n\n456", 3) == [
        ["123", "", "456"],
        [" ", " ", " "],
        False,
        None,
    ]

    assert line_spliter(
        text="123\n456\n789",
        width=3,
        height=2,
    ) == [["123", "456"], [" ", "…"], False, None]

    assert line_spliter(
        text="123\n456\n789",
        width=3,
        height=3,
    ) == [["123", "456", "789"], [" ", " ", " "], False, None]

    assert line_spliter(
        text="123\n456",
        width=3,
        height=3,
    ) == [["123", "456"], [" ", " "], False, None]
    assert line_spliter(text="12345\n123456\n1") == [
        ["12345", "123456", "1"],
        [" ", " ", " "],
        False,
        None,
    ]


def test_fill_line():
    assert (
        fill_line(
            [["1", "2", "3", "4", "5", "6"]],
            [["↩", "↩", " ", "↩", "↩", " "]],
            [False],
            (None,),
            [1],
            ("<",),
            ("^",),
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
            [False],
            (None,),
            [1],
            ("<",),
            ("^",),
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
        fill_line(
            [["12", "3", "45", "6"]],
            [["↩", " ", "↩", " "]],
            [False],
            (None,),
            [2],
            ("<",),
            ("^",),
        )
        == """
| 12↩|
| 3  |
| 45↩|
| 6  |
""".strip()
    )
    assert (
        fill_line(
            [["12", "3", "45", "6"]],
            [["↩", " ", "↩", " "]],
            [False],
            (None,),
            [2],
            (">",),
            ("^",),
        )
        == """
| 12↩|
|  3 |
| 45↩|
|  6 |
""".strip()
    )
    assert (
        fill_line(
            [["123", "456"]],
            [[" ", " "]],
            [False, False],
            (None, None),
            [3],
            ("<",),
            ("^",),
        )
        == """
| 123 |
| 456 |
""".strip()
    )
    assert (
        fill_line(
            [["123"], ["456"]],
            [[" "], [" "]],
            [False, False],
            (None, None),
            [3, 3],
            ("<", "<"),
            (
                "^",
                "^",
            ),
        )
        == "| 123 | 456 |"
    )
    assert (
        fill_line(
            [["1234567", "34", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [11],
            ("^<",),
            ("^",),
        )
        == """
|   1234567   |
|   34        |
|   787878    |
""".strip()
    )
    assert (
        fill_line(
            [["1234567", "34", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [12],
            ("^<",),
            ("^",),
        )
        == """
|   1234567    |
|   34         |
|   787878     |
""".strip()
    )
    assert (
        fill_line(
            [["1234567", "34", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [13],
            ("^<",),
            ("^",),
        )
        == """
|    1234567    |
|    34         |
|    787878     |
""".strip()
    )
    assert (
        fill_line(
            [["1234567", "34", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [11],
            ("^>",),
            ("^",),
        )
        == """
|   1234567   |
|        34   |
|    787878   |
""".strip()
    )
    assert (
        fill_line(
            [["1234567", "34", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [12],
            ("^>",),
            ("^",),
        )
        == """
|   1234567    |
|        34    |
|    787878    |
""".strip()
    )
    assert (
        fill_line(
            [["34", "1234567", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [11],
            ("^<",),
            ("^",),
        )
        == """
|   34        |
|   1234567   |
|   787878    |
""".strip()
    )
    assert (
        fill_line(
            [["34", "1234567", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [12],
            ("^<",),
            ("^",),
        )
        == """
|   34         |
|   1234567    |
|   787878     |
""".strip()
    )
    assert (
        fill_line(
            [["34", "1234567", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [11],
            ("^>",),
            ("^",),
        )
        == """
|        34   |
|   1234567   |
|    787878   |
""".strip()
    )
    assert (
        fill_line(
            [["34", "1234567", "787878"]],
            [[" ", " ", " "]],
            [False],
            (None,),
            [12],
            ("^>",),
            ("^",),
        )
        == """
|        34    |
|   1234567    |
|    787878    |
""".strip()
    )


def test_get_row_widths():
    assert get_row_widths([["123"]]) == [3]
    assert get_row_widths([["123"], ["q"]]) == [3]
    assert get_row_widths([["123"], ["qqqq"]]) == [4]
    assert get_row_widths([["123", "q"]]) == [3, 1]
    assert get_row_widths([["123", "qqqq"]]) == [3, 4]
    assert get_row_widths([["123", "qqqq"]], minimum=True) == [1, 1]
    assert get_row_widths(
        [
            ("123", "123"),
            (Table([("111", "222"), ("333", "444")]), "123"),
        ]
    ) == [9, 3]
    assert get_row_widths(
        [
            ("123", "123"),
            (Table([("111", "222"), ("333", "444")]), "123"),
        ],
        minimum=True,
    ) == [5, 1]
    assert get_row_widths(
        [
            ("123", "123"),
            (
                Table(
                    [("111", "222"), ("333", Table([("111", "222"), ("333", "444")]))]
                ),
                "123",
            ),
        ]
    ) == [15, 3]
    assert get_row_widths(
        [
            ("123", "123"),
            (
                Table(
                    [("111", "222"), ("333", Table([("111", "222"), ("333", "444")]))]
                ),
                "123",
            ),
        ],
        minimum=True,
    ) == [9, 1]


def test_apply_v_align():
    assert apply_v_align(["a", "", " "], "^") == ["a", " ", " "]
    assert apply_v_align([" ", "a", " "], "-") == [" ", "a", " "]
    assert apply_v_align([" ", "a", " "], "_") == [" ", " ", "a"]


def test_apply_metadata():
    assert (
        apply_metadata(
            "+-------+",
            "border_top",
            Themes.ascii_thin,
            ({"border_top": ("-", "+", "+", "-", "+")},),
            [3],
        )
        == "+--++-+-+"
    )
