from table2string import Table, Color, BgColor
from table2string.text_splitters import (
    BaseTextSplitter,
    AnsiTextSplitter,
    HtmlTextSplitter,
    AnsiTextSplitterUnsafe,
)


text_spliter = AnsiTextSplitterUnsafe()
text_spliter_escape_unsafe = AnsiTextSplitter()

split_text = text_spliter.split_text
split_text_escape_unsafe = text_spliter_escape_unsafe.split_text


def test_split_text():
    assert split_text("text") == (["text"], [" "], False, {})
    assert split_text("te\nxt") == (["te", "xt"], [" ", " "], False, {})
    assert split_text("te\n\nxt") == (["te", "", "xt"], [" ", " ", " "], False, {})
    assert split_text("", 1) == ([""], [" "], False, {})
    assert split_text("1", 1) == (["1"], [" "], False, {})
    assert split_text("123\n456", 1) == (
        ["1", "2", "3", "4", "5", "6"],
        ["/", "/", " ", "/", "/", " "],
        False,
        {},
    )
    assert split_text("123\n\n456", 1) == (
        ["1", "2", "3", "", "4", "5", "6"],
        ["/", "/", " ", " ", "/", "/", " "],
        False,
        {},
    )
    assert split_text("123\n456", 2) == (
        ["12", "3", "45", "6"],
        ["/", " ", "/", " "],
        False,
        {},
    )
    assert split_text("123\n456", 3) == (["123", "456"], [" ", " "], False, {})
    assert split_text("123\n\n456", 3) == (
        ["123", "", "456"],
        [" ", " ", " "],
        False,
        {},
    )

    assert split_text(
        text="123\n456\n789",
        width=3,
        height=2,
    ) == (["123", "456"], [" ", "…"], False, {})

    assert split_text(
        text="123\n456\n789",
        width=3,
        height=3,
    ) == (["123", "456", "789"], [" ", " ", " "], False, {})

    assert split_text(
        text="123\n456",
        width=3,
        height=3,
    ) == (["123", "456"], [" ", " "], False, {})
    assert split_text(text="12345\n123456\n1") == (
        ["12345", "123456", "1"],
        [" ", " ", " "],
        False,
        {},
    )


def test_color_escape_sequence():
    assert split_text("\x1b[34mbl\nue\x1b[0m text")[0] == [
        "\x1b[34mbl\x1b[0m",
        "\x1b[34mue\x1b[0m text",
    ]
    assert split_text("t\x1b[31mex\x1b[0mt")[0] == ["t\x1b[31mex\x1b[0mt"]
    assert split_text("t\x1b[31me\x1b[1mx\x1b[0mt", width=1)[0] == [
        "t",
        "\x1b[31me\x1b[0m",
        "\x1b[31m\x1b[1mx\x1b[0m",
        "t",
    ]
    assert split_text("\x1b[32m\x1b[40;1m\x1b[1mtext\n\x1b[0mtext1")[0] == [
        "\x1b[32m\x1b[40;1m\x1b[1mtext\x1b[0m",
        "text1",
    ]
    assert split_text("\x1b[32m\x1b[40;1m\x1b[1mtext\x1b[0m\ntex\nt2")[0] == [
        "\x1b[32m\x1b[40;1m\x1b[1mtext\x1b[0m",
        "tex",
        "t2",
    ]
    assert split_text("\x1b[32m\x1b[40;1m\x1b[1mtext\x1b[0m\ntext1")[0] == [
        "\x1b[32m\x1b[40;1m\x1b[1mtext\x1b[0m",
        "text1",
    ]
    assert split_text("123\x1b[32m123\x1b[32m\x1b[32m\x1b[0mqpow", width=1)[0] == [
        "1",
        "2",
        "3",
        "\x1b[32m1\x1b[0m",
        "\x1b[32m2\x1b[0m",
        "\x1b[32m3\x1b[0m",
        "q",
        "p",
        "o",
        "w",
    ]
    assert split_text("123\x1b[32m123\x1b[32m\x1b[32m\x1b[0mqpow", width=2)[0] == [
        "12",
        "3\x1b[32m1\x1b[0m",
        "\x1b[32m23\x1b[0m",
        "qp",
        "ow",
    ]
    assert split_text("123\x1b[32m123\x1b[32m\x1b[32m\x1b[0mqpow", width=3)[0] == [
        "123",
        "\x1b[32m123\x1b[0m",
        "qpo",
        "w",
    ]
    assert split_text("123\x1b[32m123\x1b[32m\x1b[32m\x1b[0mqpow", width=4)[0] == [
        "123\x1b[32m1\x1b[0m",
        "\x1b[32m23\x1b[0mqp",
        "ow",
    ]
    assert split_text("\x1b[31m1234")[0] == ["\x1b[31m1234\x1b[0m"]

    table = Table(
        [
            (
                "\x1b[31m1234",
                "5",
                "67\x1b[31m890\n1112",
                "abc\x1b[31mXYZ\x1b[0mdef",
                "\x1b[32mgreen\x1b[0m",
                "\x1b[34mbl\nue\x1b[0m text",
                "123\x1b[32m123\x1b[32m\x1b[32m\x1b[0mqpow",
            ),
        ]
    )
    assert (
        table.stringify(
            max_width=(4,),
            line_break_symbol="-",
            text_spliter=AnsiTextSplitterUnsafe(),
        )
        == """
+------+------+------+------+------+------+------+
| \x1b[31m1234\x1b[0m |    5 | 67\x1b[31m89\x1b[0m-| abc\x1b[31mX\x1b[0m-| \x1b[32mgree\x1b[0m-| \x1b[34mbl\x1b[0m   | 123\x1b[32m1\x1b[0m-|
|      |      | \x1b[31m0\x1b[0m    | \x1b[31mYZ\x1b[0mde-| \x1b[32mn\x1b[0m    | \x1b[34mue\x1b[0m t-| \x1b[32m23\x1b[0mqp-|
|      |      | \x1b[31m1112\x1b[0m | f    |      | ext  | ow   |
+------+------+------+------+------+------+------+
""".strip()
    )
    table = Table(
        [
            ("\x1b[31mq\x1b[33mw\x1b[34me\x1b[35mr\x1b[0mt\x1b[46my",),
        ]
    )
    assert (
        table.stringify(
            max_width=(4,),
            line_break_symbol="-",
            text_spliter=AnsiTextSplitterUnsafe(),
        )
        == """
+------+
| \x1b[31mq\x1b[33mw\x1b[34me\x1b[35mr\x1b[0m-|
| t\x1b[46my\x1b[0m   |
+------+
""".strip()
    )


def test_osc_link_escape_sequence():
    assert split_text(
        "#0nk: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\ end", width=3
    )[0] == [
        "#0n",
        "k: ",
        "\x1b]8;;https://example.com\x1b\\Exa\x1b]8;;\x1b\\",
        "\x1b]8;;https://example.com\x1b\\mpl\x1b]8;;\x1b\\",
        "\x1b]8;;https://example.com\x1b\\e\x1b]8;;\x1b\\ e",
        "nd",
    ]
    assert split_text(
        "#1nk: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\ end"
    )[0] == ["#1nk: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\ end"]
    assert split_text(
        "#2nk: \x1b]8;;https://example.com\x1b\\Ex\x1b[31mam\x1b[0mple\x1b]8;;\x1b\\ end"
    )[0] == [
        "#2nk: \x1b]8;;https://example.com\x1b\\Ex\x1b[31mam\x1b[0mple\x1b]8;;\x1b\\ end"
    ]
    assert split_text(
        "#3nk: \x1b]8;;https://example.com\x1b\\Ex\x1b[31mam\x1b[0mple\x1b]8;;\x1b\\ end",
        width=3,
    )[0] == [
        "#3n",
        "k: ",
        "\x1b]8;;https://example.com\x1b\\Ex\x1b[31ma\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[31m\x1b]8;;https://example.com\x1b\\m\x1b[0mpl\x1b]8;;\x1b\\",
        "\x1b]8;;https://example.com\x1b\\e\x1b]8;;\x1b\\ e",
        "nd",
    ]
    assert split_text(
        "link: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\",
    )[0] == [
        "link: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\",
    ]
    assert split_text(
        "Link: "
        "\x1b]8;;https://site.com\x1b\\"
        "\x1b[38;2;255;100;100m\x1b[1mRed\x1b[0m"
        "\x1b[4m&\x1b[0m"
        "\x1b[9m\x1b[34mBlue\x1b[0m"
        "\x1b]8;;\x1b\\"
        " Text \x1b[3mItalic\x1b[0m!",
        width=4,
    )[0] == [
        "Link",
        ": \x1b]8;;https://site.com\x1b\\\x1b[38;2;255;100;100m\x1b[1mRe\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[38;2;255;100;100m\x1b[1m\x1b]8;;https://site.com\x1b\\d\x1b[0m"
        "\x1b[4m&\x1b[0m\x1b[9m\x1b[34mBl\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[9m\x1b[34m\x1b]8;;https://site.com\x1b\\ue\x1b]8;;\x1b\\\x1b[0m T",
        "ext ",
        "\x1b[3mItal\x1b[0m",
        "\x1b[3mic\x1b[0m!",
    ]
    assert split_text(
        "@ "
        "\x1b]8;;https://a.io\x1b\\"
        "\x1b[1m\x1b[31mRe\x1b[0m"
        "\x1b[32mg"
        "\x1b]8;;\x1b\\"
        "\x1b[3m\x1b[48;2;0;255;0mN\x1b[0m"
        "\x1b]8;;https://b.io\x1b\\"
        "\x1b[4met\x1b[0m"
        "\x1b[9m\x1b[38;2;255;255;0mX\x1b[0m"
        "\x1b]8;;\x1b\\"
        " END",
        width=4,
    )[0] == [
        "@ \x1b]8;;https://a.io\x1b\\\x1b[1m\x1b[31mRe\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[1m\x1b[31m\x1b]8;;https://a.io\x1b\\\x1b[0m\x1b[32mg\x1b]8;;\x1b\\"
        "\x1b[3m\x1b[48;2;0;255;0mN\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[4met\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[4m\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[9m\x1b[38;2;255;255;0mX\x1b]8;;\x1b\\\x1b[0m EN",
        "D",
    ]
    assert split_text(
        "\x1b]8;;https://a.com\x1b\\A\x1b]8;;\x1b\\\x1b]8;;https://b.com\x1b\\B\x1b]8;;\x1b\\",
    )[0] == [
        "\x1b]8;;https://a.com\x1b\\A\x1b]8;;\x1b\\\x1b]8;;https://b.com\x1b\\B\x1b]8;;\x1b\\",
    ]
    assert split_text(
        "\x1b]8;;https://a.com\x1b\\A\x1b]8;;\x1b\\"
        "\x1b]8;;https://b.com\x1b\\n\x1b]8;;\x1b\\"
        "\x1b]8;;https://c.com\x1b\\s\x1b]8;;\x1b\\"
        "\x1b]8;;https://d.com\x1b\\I\x1b]8;;\x1b\\"
        "s \x1b]8;;https://e.com\x1b\\F\x1b]8;;\x1b\\un!",
        width=3,
    )[0] == [
        "\x1b]8;;https://a.com\x1b\\A\x1b]8;;\x1b\\\x1b]8;;https://b.com\x1b\\n\x1b]8;;\x1b\\"
        "\x1b]8;;https://c.com\x1b\\s\x1b]8;;\x1b\\",
        "\x1b]8;;https://d.com\x1b\\I\x1b]8;;\x1b\\s ",
        "\x1b]8;;https://e.com\x1b\\F\x1b]8;;\x1b\\un",
        "!",
    ]
    assert split_text(
        "\x1b]8;;https://a.com\x1b\\1\x1b]8;;\x1b\\"
        "\x1b]8;;https://b.com\x1b\\2\x1b]8;;\x1b\\"
        "\x1b]8;;https://c.com\x1b\\3\x1b]8;;\x1b\\",
        width=1,
    )[0] == [
        "\x1b]8;;https://a.com\x1b\\1\x1b]8;;\x1b\\",
        "\x1b]8;;https://b.com\x1b\\2\x1b]8;;\x1b\\",
        "\x1b]8;;https://c.com\x1b\\3\x1b]8;;\x1b\\",
    ]
    assert split_text(
        "\x1b[1m\x1b]8;;https://a.com\x1b\\A\x1b]8;;\x1b\\\x1b[0m"
        "\x1b[3m\x1b]8;;https://b.com\x1b\\n\x1b]8;;\x1b\\\x1b[0m"
        "\x1b[4m\x1b[38;2;255;0;0m\x1b]8;;https://c.com\x1b\\s\x1b]8;;\x1b\\\x1b[0m"
        "\x1b[9m\x1b[48;5;25m\x1b]8;;https://d.com\x1b\\I\x1b]8;;\x1b\\\x1b[0m"
        "s \x1b[38;5;196m\x1b[1m\x1b]8;;https://e.com\x1b\\F\x1b]8;;\x1b\\\x1b[0mu\x1b[0mn!",
        width=3,
    )[0] == [
        "\x1b]8;;https://a.com\x1b\\\x1b[1mA\x1b]8;;\x1b\\\x1b]8;;https://b.com\x1b\\\x1b[0m\x1b[3mn\x1b]8;;\x1b\\"
        "\x1b]8;;https://c.com\x1b\\\x1b[0m\x1b[4m\x1b[38;2;255;0;0ms\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[4m\x1b[38;2;255;0;0m\x1b]8;;https://d.com\x1b\\\x1b[0m\x1b[9m\x1b[48;5;25mI\x1b]8;;\x1b\\\x1b[0ms ",
        "\x1b]8;;https://e.com\x1b\\\x1b[38;5;196m\x1b[1mF\x1b]8;;\x1b\\\x1b[0mu\x1b[0mn",
        "!",
    ]
    assert split_text(
        "\x1b[1m\x1b[31m\x1b]8;;https://x.com\x1b\\A\x1b[0m\x1b[3mB\x1b]8;;\x1b\\"
        "\x1b[4m\x1b[48;2;10;10;10m\x1b]8;;https://y.com\x1b\\C\x1b[0m\x1b[9mD\x1b]8;;\x1b\\"
        "\x1b[7mE\x1b[0m\x1b[38;2;200;100;50m\x1b]8;;https://z.com\x1b\\F\x1b[0m\x1b]8;;\x1b\\"
        "\x1b[35mGH\x1b[0m",
        width=1,
    )[0] == [
        "\x1b]8;;https://x.com\x1b\\\x1b[1m\x1b[31mA\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[1m\x1b[31m\x1b]8;;https://x.com\x1b\\\x1b[0m\x1b[3mB\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[3m\x1b]8;;https://y.com\x1b\\\x1b[4m\x1b[48;2;10;10;10mC\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[3m\x1b[4m\x1b[48;2;10;10;10m\x1b]8;;https://y.com\x1b\\\x1b[0m\x1b[9mD\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[9m\x1b[7mE\x1b[0m",
        "\x1b[9m\x1b[7m\x1b]8;;https://z.com\x1b\\\x1b[0m\x1b[38;2;200;100;50mF\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[35mG\x1b[0m",
        "\x1b[35mH\x1b[0m",
    ]
    assert split_text(
        "\x1b[1m\x1b[31m\x1b]8;;https://a.io\x1b\\😎\x1b[0m\x1b]8;;\x1b\\"
        "\x1b[3m\x1b[38;2;123;45;67m\x1b]8;;https://b.io\x1b\\B\x1b[0m\x1b[4m"
        "\x1b[48;5;200mC\x1b[999m\x1b[0m\x1b"
        "\x1b[7m\x1b]8;;https://c.io\x1b\\D\x1b[0m\x1b]8;;\x1b\\E\x1b[35mF\x1b[0m",
        width=3,
    )[0] == [
        "\x1b]8;;https://a.io\x1b\\\x1b[1m\x1b[31m😎\x1b]8;;\x1b\\"
        "\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[3m\x1b[38;2;123;45;67mB\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[3m\x1b[38;2;123;45;67m\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[4m"
        "\x1b[48;5;200mC\x1b[0m\x1b\x1b[7mD\x1b]8;;\x1b\\\x1b[0mE",
        "\x1b[35mF\x1b[0m",
    ]
    assert split_text(
        "\x1b[1m\x1b[31m\x1b]8;;https://a.io\x1b\\😎\x1b[0m\x1b]8;;\x1b\\"
        "\x1b[3m\x1b[38;2;123;45;67m\x1b]8;;https://b.io\x1b\\B\x1b[0m\x1b[4m"
        "\x1b[48;5;200mC\x1b[999m\x1b[0m"
        "\x1b[7m\x1b]8;;https://c.io\x1b\\D\x1b[0m\x1b]8;;\x1b\\E\x1b[35mF\x1b[0m",
        width=3,
    )[0] == [
        "\x1b]8;;https://a.io\x1b\\\x1b[1m\x1b[31m😎\x1b]8;;\x1b\\"
        "\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[3m\x1b[38;2;123;45;67mB\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[3m\x1b[38;2;123;45;67m\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[4m"
        "\x1b[48;5;200mC\x1b[0m\x1b[7mD\x1b]8;;\x1b\\\x1b[0mE",
        "\x1b[35mF\x1b[0m",
    ]
    assert split_text(
        "\x1b[1m\x1b[38;2;255;0;0mW\x1b]8;;https://link.com\x1b\\中\x1b[0m\x1b]8;;\x1b\\"
        "\x1b[3mi—\x1b[4m😈\x1b[0m\n"
        "\x1b[9m\x1b[35mZ\x1b[0m",
        width=3,
    )[0] == [
        "\x1b[1m\x1b[38;2;255;0;0mW\x1b]8;;https://link.com\x1b\\中\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[3mi—\x1b[4m😈\x1b[0m",
        "\x1b[9m\x1b[35mZ\x1b[0m",
    ]

    table = Table(
        [
            (
                # Простой случай без escape последовательностей
                "1234",
                "5",
                "67890\n1112",
            ),
            (
                # Строка с CSI-последовательностями (цвет и сброс)
                "abc\x1b[31mXYZ\x1b[0mdef",
                "\x1b[32mgreen\x1b[0m",
                "normal",
            ),
            (
                # Строка с OSC-последовательностями для кликабельной ссылки и CSI для цвета
                "link: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\",
                "\x1b[34mblue\x1b[0m text",
                "Multiple escapes: \x1b[1;31mBold Red\x1b[0m, \x1b[4mUnderlined\x1b[0m",
            ),
            (
                "\x1b[34mbl\nue\x1b[0m text",
                "te\nxt",
                "",
            ),
        ]
    )
    assert (
        table.stringify(
            text_spliter=AnsiTextSplitterUnsafe(),
        )
        == """
+---------------+-----------+----------------------------------------+
|          1234 |         5 | 67890                                  |
|               |           | 1112                                   |
+---------------+-----------+----------------------------------------+
| abc\x1b[31mXYZ\x1b[0mdef     | \x1b[32mgreen\x1b[0m     | normal                                 |
+---------------+-----------+----------------------------------------+
| link: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\ | \x1b[34mblue\x1b[0m text | Multiple escapes: \x1b[1;31mBold Red\x1b[0m, \x1b[4mUnderlined\x1b[0m |
+---------------+-----------+----------------------------------------+
| \x1b[34mbl\x1b[0m            | te        |                                        |
| \x1b[34mue\x1b[0m text       | xt        |                                        |
+---------------+-----------+----------------------------------------+
""".strip()
    )
    table = Table(
        [
            ("link: \x1b]8;;https://example.com\x1b\\Example\x1b]8;;\x1b\\end",),
        ],
    )
    assert (
        table.stringify(
            max_width=(3,),
            line_break_symbol="↩",
            text_spliter=AnsiTextSplitterUnsafe(),
        )
        == """
+-----+
| lin↩|
| k: ↩|
| \x1b]8;;https://example.com\x1b\\Exa\x1b]8;;\x1b\\↩|
| \x1b]8;;https://example.com\x1b\\mpl\x1b]8;;\x1b\\↩|
| \x1b]8;;https://example.com\x1b\\e\x1b]8;;\x1b\\en↩|
| d   |
+-----+
""".strip()
    )
    table = Table(
        [
            ("link: \x1b]8;;https://example.com\x1b\\Ex\nample\x1b]8;;\x1b\\end",),
        ],
    )
    assert (
        table.stringify(
            max_width=(3,),
            line_break_symbol="↩",
            text_spliter=AnsiTextSplitterUnsafe(),
        )
        == """
+-----+
| lin↩|
| k: ↩|
| \x1b]8;;https://example.com\x1b\\Ex\x1b]8;;\x1b\\  |
| \x1b]8;;https://example.com\x1b\\amp\x1b]8;;\x1b\\↩|
| \x1b]8;;https://example.com\x1b\\le\x1b]8;;\x1b\\e↩|
| nd  |
+-----+
""".strip()
    )


def test_wrong_escape_sequence():
    assert split_text(
        "#0\x1b[31mnk: \x1b]8;;https://example.com\x1b\\Example end",
        width=3,
    )[0] == [
        "#0\x1b[31mn\x1b[0m",
        "\x1b[31mk: \x1b[0m",
        "\x1b[31mExa\x1b[0m",
        "\x1b[31mmpl\x1b[0m",
        "\x1b[31me e\x1b[0m",
        "\x1b[31mnd\x1b[0m",
    ]
    assert split_text(
        "#0nk\x1b[0m\x1b[1m\x1b[0m\x1b[0m\x1b[0m\x1b[1m\x1b[0m\x1b[0m\x1b[0m\x1b[0m: Example\x1b]8;;\x1b\\ end",
        width=3,
    )[0] == [
        "#0n",
        "k\x1b[0m: ",
        "Exa",
        "mpl",
        "e e",
        "nd",
    ]


def test_split_text_escape_unsafe():
    assert split_text_escape_unsafe("\x1b[31m\x1b[1EA\x1b[0m")[0] == [
        "\x1b[31m\\x1b[1EA\x1b[0m",
    ]
    assert split_text_escape_unsafe("\x1b[31m1\x07A\x1b[0m", width=1)[0] == [
        "\x1b[31m1\x1b[0m",
        "\x1b[31m\\\x1b[0m",
        "\x1b[31mx\x1b[0m",
        "\x1b[31m0\x1b[0m",
        "\x1b[31m7\x1b[0m",
        "\x1b[31mA\x1b[0m",
    ]
    assert split_text_escape_unsafe(
        "\x1b[1m\x1b[31m\x1b]8;;https://a.io\x1b\\😎\x1b[0m\x1b]8;;\x1b\\"
        "\x1b[3m\x1b[38;2;123;45;67m\x1b]8;;https://b.io\x1b\\B\x1b[0m\x1b[4m"
        "\x1b[48;5;200mC\x1b[999m\x1b[0m\x1b"
        "\x1b[7m\x1b]8;;https://c.io\x1b\\D\x1b[0m\x1b]8;;\x1b\\E\x1b[35mF\x1b[0m",
        width=3,
    )[0] == [
        "\x1b]8;;https://a.io\x1b\\\x1b[1m\x1b[31m😎\x1b]8;;\x1b\\"
        "\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[3m\x1b[38;2;123;45;67mB\x1b]8;;\x1b\\\x1b[0m",
        "\x1b[3m\x1b[38;2;123;45;67m\x1b]8;;https://b.io\x1b\\\x1b[0m\x1b[4m\x1b[48;5;200mC\x1b[0m\\x\x1b]8;;\x1b\\",
        "\x1b]8;;https://b.io\x1b\\1b\x1b[7mD\x1b]8;;\x1b\\\x1b[0m",
        "E\x1b[35mF\x1b[0m",
    ]


def test_html_spliter():
    html_text_spliter = HtmlTextSplitter()
    html_split_text = html_text_spliter.split_text
    assert html_split_text("123", width=2)[0] == ["12", "3"]
    assert html_split_text("1\x1b[32m23", width=2)[0] == [
        "1\\",
        "x1",
        "b[",
        "32",
        "m2",
        "3",
    ]
    assert html_split_text("123<b>456</b>789")[0] == ["123\x1b[1m456\x1b[0m789"]
    assert (
        html_split_text(
            """
<p><span style="color:#2ecc71;">Lorem ipsum dolor sit amet</span>, <span style="color:#3498db;">consectetur adipiscing elit</span>.</p>
<p>Sed do eiusmod <a href="https://example.com"><span style="color:#e67e22;">tempor incididunt</span></a> ut labore et dolore magna aliqua. <span style="color:#9b59b6;">Ut enim ad minim veniam</span>, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. <a href="https://w3schools.com" style="color:#e74c3c;">Duis aute irure dolor</a> in reprehenderit in voluptate velit esse <span style="color:#34495e;">cillum dolore eu fugiat nulla pariatur</span>.</p>
Excepteur sint occaecat cupidatat non p<span style="background-color:rgb(255,0,0)">roide</span>nt, sunt in culpa qui officia
<a href="https://openai.com" style="color:#1abc9c;">deserunt mollit anim</a> id est laborum.
""".strip()
        )[0]
        == [
            "\x1b[38;2;46;204;113mLorem ipsum dolor sit amet\x1b[0m, \x1b[38;2;52;152;219mconsecte\x1b[0m",
            "\x1b[38;2;52;152;219mtur adipiscing elit\x1b[0m.",
            "",
            "",
            "Sed do eiusmod \x1b]8;;https://example.com\x1b\\\x1b[38;2;230;126;34mtempor incididunt\x1b]8;;\x1b\\\x1b[0m ut ",
            "labore et dolore magna aliqua. \x1b[38;2;155;89;182mUt en\x1b[0m",
            "\x1b[38;2;155;89;182mim ad minim veniam\x1b[0m, quis nostrud exe",
            "rcitation ullamco laboris nisi ut al",
            "iquip ex ea commodo consequat. \x1b]8;;https://w3schools.com\x1b\\\x1b[38;2;231;76;60mDuis \x1b]8;;\x1b\\\x1b[0m",
            "\x1b[38;2;231;76;60m\x1b]8;;https://w3schools.com\x1b\\aute irure dolor\x1b]8;;\x1b\\\x1b[0m in reprehenderit in",
            " voluptate velit esse \x1b[38;2;52;73;94mcillum dolore \x1b[0m",
            "\x1b[38;2;52;73;94meu fugiat nulla pariatur\x1b[0m.",
            "",
            "Excepteur sint occaecat cupidatat no",
            "n p\x1b[48;2;255;0;0mroide\x1b[0mnt, sunt in culpa qui offici",
            "a",
            "\x1b]8;;https://openai.com\x1b\\\x1b[38;2;26;188;156mdeserunt mollit anim\x1b]8;;\x1b\\\x1b[0m id est laborum.",
        ]
    )
    assert (
        html_split_text(
            """
<p><span style="color:#2ecc71;">Lorem ipsum dolor sit amet</span>, <span style="color:#3498db;">consectetur adipiscing elit</span>.</p>
<p>Sed do eiusmod <a href="https://example.com"><span style="color:#e67e22;">tempor incididunt</span></a> ut labore et dolore magna aliqua. <span style="color:#9b59b6;">Ut enim ad minim veniam</span>, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. <a href="https://w3schools.com" style="color:#e74c3c;">Duis aute irure dolor</a> in reprehenderit in voluptate velit esse <span style="color:#34495e;">cillum dolore eu fugiat nulla pariatur</span>.</p>
Excepteur sint occaecat cupidatat non p<span style="background-color:rgb(255,0,0)">roide</span>nt, sunt in culpa qui officia
<a href="https://openai.com" style="color:#1abc9c;">deserunt mollit anim</a> id est laborum.
""".strip(),
            width=50,
        )[0]
        == [
            "\x1b[38;2;46;204;113mLorem ipsum dolor sit amet\x1b[0m, \x1b[38;2;52;152;219mconsectetur adipiscing\x1b[0m",
            "\x1b[38;2;52;152;219m elit\x1b[0m.",
            "",
            "",
            "Sed do eiusmod \x1b]8;;https://example.com\x1b\\\x1b[38;2;230;126;34mtempor incididunt\x1b]8;;\x1b\\\x1b[0m ut labore et dolo",
            "re magna aliqua. \x1b[38;2;155;89;182mUt enim ad minim veniam\x1b[0m, quis nos",
            "trud exercitation ullamco laboris nisi ut aliquip ",
            "ex ea commodo consequat. \x1b]8;;https://w3schools.com\x1b\\\x1b[38;2;231;76;60mDuis aute irure dolor\x1b]8;;\x1b\\\x1b[0m in ",
            "reprehenderit in voluptate velit esse \x1b[38;2;52;73;94mcillum dolor\x1b[0m",
            "\x1b[38;2;52;73;94me eu fugiat nulla pariatur\x1b[0m.",
            "",
            "Excepteur sint occaecat cupidatat non p\x1b[48;2;255;0;0mroide\x1b[0mnt, su",
            "nt in culpa qui officia",
            "\x1b]8;;https://openai.com\x1b\\\x1b[38;2;26;188;156mdeserunt mollit anim\x1b]8;;\x1b\\\x1b[0m id est laborum.",
        ]
    )
    table = Table(
        [
            (
                """<b>ANSI escape sequences</b> are a standard for <a href="https://en.wikipedia.org/wiki/In-band_signaling">in-band signaling</a> to control cursor location, color, font styling, and other options on video <a href="https://en.wikipedia.org/wiki/Text_terminal">text terminals</a> and <a href="https://en.wikipedia.org/wiki/Terminal_emulator">terminal emulators</a>. Certain sequences of <a href="https://en.wikipedia.org/wiki/Byte">bytes</a>, most starting with an <a href="https://en.wikipedia.org/wiki/Escape_character#ASCII_escape_character">ASCII escape</a> character and a <a href="https://en.wikipedia.org/wiki/Bracket">bracket</a> character, are embedded into text. The terminal interprets these sequences as commands, rather than text to display verbatim.""",
            ),
        ],
        name='<a href="https://en.wikipedia.org/wiki/ANSI_escape_code">https://en.wikipedia.org/wiki/ANSI_escape_code</a>',
    )
    assert (
        table.stringify(
            max_width=51,
            name_spliter=HtmlTextSplitter(),
            text_spliter=HtmlTextSplitter(),
            line_break_symbol="/",
        )
        == """
+-------------------------------------------------+
| \x1b]8;;https://en.wikipedia.org/wiki/ANSI_escape_code\x1b\\https://en.wikipedia.org/wiki/ANSI_escape_code\x1b]8;;\x1b\\  |
+-------------------------------------------------+
| \x1b[1mANSI escape sequences\x1b[0m are a standard for \x1b]8;;https://en.wikipedia.org/wiki/In-band_signaling\x1b\\in-ban\x1b]8;;\x1b\\/|
| \x1b]8;;https://en.wikipedia.org/wiki/In-band_signaling\x1b\\d signaling\x1b]8;;\x1b\\\x1b[0m to control cursor location, color, /|
| font styling, and other options on video \x1b]8;;https://en.wikipedia.org/wiki/Text_terminal\x1b\\text t\x1b]8;;\x1b\\/|
| \x1b]8;;https://en.wikipedia.org/wiki/Text_terminal\x1b\\erminals\x1b]8;;\x1b\\\x1b[0m and \x1b]8;;https://en.wikipedia.org/wiki/Terminal_emulator\x1b\\terminal emulators\x1b]8;;\x1b\\\x1b[0m. Certain sequen/|
| ces of \x1b]8;;https://en.wikipedia.org/wiki/Byte\x1b\\bytes\x1b]8;;\x1b\\\x1b[0m, most starting with an \x1b]8;;https://en.wikipedia.org/wiki/Escape_character#ASCII_escape_character\x1b\\ASCII escap\x1b]8;;\x1b\\/|
| \x1b]8;;https://en.wikipedia.org/wiki/Escape_character#ASCII_escape_character\x1b\\e\x1b]8;;\x1b\\\x1b[0m character and a \x1b]8;;https://en.wikipedia.org/wiki/Bracket\x1b\\bracket\x1b]8;;\x1b\\\x1b[0m character, are embedd/|
| ed into text. The terminal interprets these seq/|
| uences as commands, rather than text to display/|
|  verbatim.                                      |
+-------------------------------------------------+
""".strip()
    )
    table = Table(
        [
            (
                """
text<br>text
""",
            ),
        ],
    )
    assert (
        table.stringify(text_spliter=HtmlTextSplitter())
        == """
+------+
| text |
| text |
+------+
""".strip()
    )
    table = Table(
        [
            (
                """
<i>text</i>
<u>text</u>
<s>text</s>
<mark>text</mark>
""",
            ),
        ],
    )
    assert (
        table.stringify(text_spliter=HtmlTextSplitter())
        == """
+------+
| \x1b[3mtext\x1b[0m |
| \x1b[4mtext\x1b[0m |
| \x1b[9mtext\x1b[0m |
| \x1b[48;2;255;255;0mtext\x1b[0m |
+------+
""".strip()
    )
    splitter = HtmlTextSplitter(
        html_classes={"red": Color.RED, "green": Color.GREEN, "bg-red": BgColor.RED},
    )
    table = Table(
        [
            (
                """
<span class="red">red text<span style="color:#000" class="bg-red">black & bg red text</span></span>
plain text
<a class="green" href="example.com">example green hyperlink</a>
""",
            )
        ]
    )
    assert (
        table.stringify(text_spliter=splitter)
        == """
+-----------------------------+
| \x1b[31mred text\x1b[41m\x1b[38;2;0;0;0mblack & bg red text\x1b[0m |
| plain text                  |
| \x1b]8;;https://example.com\x1b\\\x1b[32mexample green hyperlink\x1b]8;;\x1b\\\x1b[0m     |
+-----------------------------+
""".strip()
    )
    assert (
        splitter.split_text('<span style="color:#f00">text</span>')[0]
        == splitter.split_text('<span style="color:#ff0000">text</span>')[0]
        == splitter.split_text('<span style="color:rgb(255,0,0)">text</span>')[0]
        == ["\x1b[38;2;255;0;0mtext\x1b[0m"]
    )
    assert (
        splitter.split_text('<span style="background-color:#f00">text</span>')[0]
        == splitter.split_text('<span style="background-color:#ff0000">text</span>')[0]
        == splitter.split_text(
            '<span style="background-color:rgb(255,0,0)">text</span>'
        )[0]
        == ["\x1b[48;2;255;0;0mtext\x1b[0m"]
    )
    assert (
        splitter.split_text('<span style="color:IncorrectValue">t<b>ex</b>t</span>')[0]
        == splitter.split_text(
            '<span style="background-color:IncorrectValue">t<b>ex</b>t</span>'
        )[0]
        == ["t\x1b[1mex\x1b[0mt"]
    )


def test_different_splitters():
    table = Table(
        [
            (
                "t\x1b[31mex\x1b[0mt",
                "plain text",
                "123<b>456</b>789",
            ),
        ],
        name='<span style="color:#f00">Table</span>',
        column_names=(
            "qwoef<b>qd&lt;f</b> qld",
            "1oijf\x1b[32m1iofj\x1b[0m1woejf",
            "w1\x1b[32m23",
        ),
    )
    assert (
        table.stringify(
            name_spliter=HtmlTextSplitter(),
            column_names_spliter=(
                HtmlTextSplitter(),
                AnsiTextSplitter(),
            ),
            text_spliter=(
                AnsiTextSplitter(),
                BaseTextSplitter(),
                HtmlTextSplitter(),
            ),
        )
        == """
+----------------------------------------------+
|                    \x1b[38;2;255;0;0mTable\x1b[0m                     |
+---------------+------------------+-----------+
| qwoef\x1b[1mqd<f\x1b[0m qld | 1oijf\x1b[32m1iofj\x1b[0m1woejf |   w1\x1b[32m23\x1b[0m    |
+---------------+------------------+-----------+
| t\x1b[31mex\x1b[0mt          | plain text       | 123\x1b[1m456\x1b[0m789 |
+---------------+------------------+-----------+
""".strip()
    )
