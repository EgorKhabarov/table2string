from table2string.utils import (
    get_text_width_in_console,
    decrease_numbers,
    transform_align,
    transform_width,
    get_row_lengths,
    line_spliter,
    fill_line,
)


def test_get_text_width_in_console():
    assert get_text_width_in_console("123") == 3
    assert get_text_width_in_console("\U0001f34f\U0001f34e") == 4


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
    assert line_spliter("123\n456", 2) == [
        ["12", "3", "45", "6"],
        ["↩", " ", "↩", " "],
    ]
    assert line_spliter("123\n456", 3) == [["123", "456"], [" ", " "]]
    assert line_spliter("123\n\n456", 3) == [
        ["123", " ", "456"],
        [" ", " ", " "],
    ]

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
        fill_line(
            [["12", "3", "45", "6"]],
            [["↩", " ", "↩", " "]],
            [2],
            ("<",),
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
            [2],
            (">",),
        )
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
        fill_line(
            [["1234567", "34", "787878"]],
            [[" ", " ", " "]],
            [11],
            ("^<",),
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
            [12],
            ("^<",),
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
            [13],
            ("^<",),
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
            [11],
            ("^>",),
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
            [12],
            ("^>",),
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
            [11],
            ("^<",),
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
            [12],
            ("^<",),
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
            [11],
            ("^>",),
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
            [12],
            ("^>",),
        )
        == """
|        34    |
|   1234567    |
|    787878    |
""".strip()
    )


def test_get_row_lengths():
    assert get_row_lengths([["123"]]) == [3]
    assert get_row_lengths([["123"], ["q"]]) == [3]
    assert get_row_lengths([["123"], ["qqqq"]]) == [4]
    assert get_row_lengths([["123", "q"]]) == [3, 1]
    assert get_row_lengths([["123", "qqqq"]]) == [3, 4]
