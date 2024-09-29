import json
import sqlite3
from table2string import Table, Themes


def test_subtable():
    assert (
        Table(
            [
                map(
                    lambda t: t.stringify(theme=Themes.thin, h_align="^"),
                    (
                        Table([("1",), (Table([("2", "3")]),)]),
                        Table([(Table([("2", "3")]),), ("1",)]),
                        Table([("1",), (Table([("2",), ("3",)]),)]),
                        Table([(Table([("2",), ("3",)]),), ("1",)]),
                        Table([("1", Table([("2", "3")]))]),
                        Table([(Table([("2", "3")]), "1")]),
                        Table([("1", Table([("2",), ("3",)]))]),
                        Table([(Table([("2",), ("3",)]), "1")]),
                    ),
                ),
                (
                    Table([("1",), (Table([("2", "3")]),)]),
                    Table([(Table([("2", "3")]),), ("1",)]),
                    Table([("1",), (Table([("2",), ("3",)]),)]),
                    Table([(Table([("2",), ("3",)]),), ("1",)]),
                    Table([("1", Table([("2", "3")]))]),
                    Table([(Table([("2", "3")]), "1")]),
                    Table([("1", Table([("2",), ("3",)]))]),
                    Table([(Table([("2",), ("3",)]), "1")]),
                ),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^")
        == """
┌───────────┬───────────┬───────┬───────┬───────────────┬───────────────┬───────────┬───────────┐
│ ┌───────┐ │ ┌───┬───┐ │ ┌───┐ │ ┌───┐ │ ┌───┬───┬───┐ │ ┌───┬───┬───┐ │ ┌───┬───┐ │ ┌───┬───┐ │
│ │   1   │ │ │ 2 │ 3 │ │ │ 1 │ │ │ 2 │ │ │ 1 │ 2 │ 3 │ │ │ 2 │ 3 │ 1 │ │ │ 1 │ 2 │ │ │ 2 │ 1 │ │
│ ├───┬───┤ │ ├───┴───┤ │ ├───┤ │ ├───┤ │ └───┴───┴───┘ │ └───┴───┴───┘ │ │   ├───┤ │ ├───┤   │ │
│ │ 2 │ 3 │ │ │   1   │ │ │ 2 │ │ │ 3 │ │               │               │ │   │ 3 │ │ │ 3 │   │ │
│ └───┴───┘ │ └───────┘ │ ├───┤ │ ├───┤ │               │               │ └───┴───┘ │ └───┴───┘ │
│           │           │ │ 3 │ │ │ 1 │ │               │               │           │           │
│           │           │ └───┘ │ └───┘ │               │               │           │           │
┝━━━━━━━━━━━┿━━━━━┯━━━━━┿━━━━━━━┿━━━━━━━┿━━━━━┯━━━━┯━━━━┿━━━━┯━━━━┯━━━━━┿━━━━━┯━━━━━┿━━━━━┯━━━━━┥
│     1     │  2  │  3  │   1   │   2   │  1  │ 2  │ 3  │ 2  │ 3  │  1  │  1  │  2  │  2  │  1  │
├─────┬─────┼─────┴─────┼───────┼───────┤     │    │    │    │    │     │     ├─────┼─────┤     │
│  2  │  3  │     1     │   2   │   3   │     │    │    │    │    │     │     │  3  │  3  │     │
│     │     │           ├───────┼───────┤     │    │    │    │    │     │     │     │     │     │
│     │     │           │   3   │   1   │     │    │    │    │    │     │     │     │     │     │
└─────┴─────┴───────────┴───────┴───────┴─────┴────┴────┴────┴────┴─────┴─────┴─────┴─────┴─────┘
""".strip()
    )
    assert (
        Table(
            [
                (
                    "111111",
                    Table(
                        [
                            (
                                "2",
                                Table(
                                    [
                                        (
                                            Table(
                                                [
                                                    ("33333333333333333333", "4"),
                                                    (
                                                        Table(
                                                            [
                                                                ("55", "666"),
                                                                ("777", "8888"),
                                                            ]
                                                        ),
                                                        "9",
                                                    ),
                                                ]
                                            ),
                                            "0",
                                        ),
                                        ("10101010", "1"),
                                    ]
                                ),
                            ),
                            (
                                "2",
                                "13131313131313",
                            ),
                        ]
                    ),
                )
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^")
        == """
┌────────┬───┬──────────────────────┬───┬───┐
│ 111111 │ 2 │ 33333333333333333333 │ 4 │ 0 │
│        │   ├──────────┬───────────┼───┤   │
│        │   │    55    │    666    │ 9 │   │
│        │   ├──────────┼───────────┤   │   │
│        │   │   777    │   8888    │   │   │
│        │   ├──────────┴───────────┴───┼───┤
│        │   │         10101010         │ 1 │
│        ├───┼──────────────────────────┴───┤
│        │ 2 │        13131313131313        │
└────────┴───┴──────────────────────────────┘
""".strip()
    )
    assert (
        Table(
            [
                ("1",),
                (
                    Table(
                        [
                            (
                                "2",
                                Table(
                                    [
                                        (Table([("5", "4")]),),
                                        ("3",),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^")
        == """
┌───────────┐
│     1     │
┝━━━┯━━━┯━━━┥
│ 2 │ 5 │ 4 │
│   ├───┴───┤
│   │   3   │
└───┴───────┘
""".strip()
    )
    assert (
        Table(
            [
                ("1",),
                (
                    Table(
                        [
                            (
                                "2",
                                Table(
                                    [
                                        (Table([("5", "4")]),),
                                        ("3",),
                                    ]
                                ),
                            )
                        ]
                    ),
                ),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^", max_width=50)
        == """
┌────────────────────────────────────────────────┐
│                       1                        │
┝━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━┥
│       2       │       5       │       4        │
│               ├───────────────┴────────────────┤
│               │               3                │
└───────────────┴────────────────────────────────┘
""".strip()
    )
    assert (
        Table(
            [
                ("987",),
                (Table([("123456", "789123")]),),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^", max_width=9)
        == r"""
┌───────┐
│  987  │
┝━━━┯━━━┥
│ 1\│ 7\│
│ 2\│ 8\│
│ 3\│ 9\│
│ 4\│ 1\│
│ 5\│ 2\│
│ 6 │ 3 │
└───┴───┘
""".strip()
    )
    assert (
        Table(
            [
                ("987qwertyuiop",),
                (Table([("123456", "789123")]),),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^", max_width=9)
        == r"""
┌───────┐
│ 987qw\│
│ ertyu\│
│  iop  │
┝━━━┯━━━┥
│ 1\│ 7\│
│ 2\│ 8\│
│ 3\│ 9\│
│ 4\│ 1\│
│ 5\│ 2\│
│ 6 │ 3 │
└───┴───┘
""".strip()
    )
    assert (
        Table(
            [
                ("987qwertyuiop",),
                (
                    Table(
                        [
                            (Table([("bbb", "mmm")]), ",,,"),
                            ("123456", "789123"),
                        ]
                    ),
                ),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^")
        == """
┌────────────────────┐
│   987qwertyuiop    │
┝━━━━━┯━━━━━┯━━━━━━━━┥
│ bbb │ mmm │  ,,,   │
├─────┴─────┼────────┤
│  123456   │ 789123 │
└───────────┴────────┘
""".strip()
    )
    assert (
        Table(
            [
                ("987qwertyuiop",),
                (
                    Table(
                        [
                            (Table([("bbb", "mmm")]), ",,,"),
                            ("123456", "789123"),
                        ]
                    ),
                ),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^", max_width=(9,))
        == r"""
┌───────────┐
│ 987qwerty\│
│   uiop    │
┝━━━┯━━━┯━━━┥
│ b\│ m\│ ,\│
│ b\│ m\│ ,\│
│ b │ m │ , │
├───┴───┼───┤
│ 12345\│ 7\│
│   6   │ 8\│
│       │ 9\│
│       │ 1\│
│       │ 2\│
│       │ 3 │
└───────┴───┘
""".strip()
    )
    assert (
        Table(
            [
                ("987qwertyuiop",),
                (
                    Table(
                        [
                            (Table([("bbb", "mmm")]), ",,,"),
                            ("123456", "789123"),
                        ]
                    ),
                ),
            ]
        ).stringify(theme=Themes.thin_thick, h_align="^", max_width=13)
        == r"""
┌───────────┐
│ 987qwerty\│
│   uiop    │
┝━━━┯━━━┯━━━┥
│ b\│ m\│ ,\│
│ b\│ m\│ ,\│
│ b │ m │ , │
├───┴───┼───┤
│ 12345\│ 7\│
│   6   │ 8\│
│       │ 9\│
│       │ 1\│
│       │ 2\│
│       │ 3 │
└───────┴───┘
""".strip()
    )
    cursor = (
        sqlite3.connect(":memory:")
        .cursor()
        .execute("CREATE TABLE data (c1 TEXT, c2 TEXT, c3 TEXT);")
        .executemany(
            "INSERT INTO data (c1, c2, c3) VALUES (?, ?, ?);",
            [
                ("1", r'[[".\n1", 2], [3, 4]]', "3"),
                ("qwe", r'[[1, 2], ["3 g", "4\n6"]]', "rty"),
            ],
        )
        .execute("SELECT c1, c2, c3 FROM data;")
    )
    table = Table.from_db_cursor(cursor, column_names=True)
    table.table = list(list(row) for row in table.table)
    for i, row in enumerate(table.table):
        try:
            json_data = json.loads(row[1])
            row[1] = Table(json_data)
            table.table[i] = row
        except json.JSONDecodeError:
            pass
    assert (
        table.stringify(theme=Themes.thin_thick)
        == """
┌─────┬─────────┬─────┐
│ c1  │   c2    │ c3  │
┝━━━━━┿━━━━┯━━━━┿━━━━━┥
│   1 │ .  │  2 │   3 │
│     │ 1  │    │     │
│     ├────┼────┤     │
│     │  3 │  4 │     │
├─────┼────┴┬───┼─────┤
│ qwe │   1 │ 2 │ rty │
│     ├─────┼───┤     │
│     │ 3 g │ 4 │     │
│     │     │ 6 │     │
└─────┴─────┴───┴─────┘
""".strip()
    )
    assert (
        table.stringify(h_align="^")
        == """
+-----+---------+-----+
| c1  |   c2    | c3  |
+-----+----+----+-----+
|  1  | .  | 2  |  3  |
|     | 1  |    |     |
|     +----+----+     |
|     | 3  | 4  |     |
+-----+----++---+-----+
| qwe |  1  | 2 | rty |
|     +-----+---+     |
|     | 3 g | 4 |     |
|     |     | 6 |     |
+-----+-----+---+-----+
""".strip()
    )
    table = Table(
        [
            ("1", "2"),
            (
                "3",
                Table(
                    [
                        ("1", "2"),
                        (
                            "3",
                            Table(
                                [
                                    ("1", "2"),
                                    (
                                        "3",
                                        Table(
                                            [
                                                ("1", "2"),
                                                (
                                                    "3",
                                                    "4",
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        ],
    )
    assert (
        table.stringify()
        == """
+---+---------------+
| 1 |             2 |
+---+---+-----------+
| 3 | 1 |         2 |
|   +---+---+-------+
|   | 3 | 1 |     2 |
|   |   +---+---+---+
|   |   | 3 | 1 | 2 |
|   |   |   +---+---+
|   |   |   | 3 | 4 |
+---+---+---+---+---+
""".strip()
    )
    assert (
        Table(
            [
                (
                    Table(
                        [
                            (
                                Table(
                                    [
                                        (
                                            Table(
                                                [
                                                    (
                                                        Table(
                                                            [
                                                                (
                                                                    Table(
                                                                        [
                                                                            (
                                                                                Table(
                                                                                    [
                                                                                        (
                                                                                            Table(
                                                                                                [
                                                                                                    (
                                                                                                        "1",
                                                                                                    ),
                                                                                                    (
                                                                                                        Table(
                                                                                                            [
                                                                                                                (
                                                                                                                    "2",
                                                                                                                    "3",
                                                                                                                )
                                                                                                            ]
                                                                                                        ).stringify(),
                                                                                                    ),
                                                                                                ]
                                                                                            ).stringify(),
                                                                                        )
                                                                                    ]
                                                                                ).stringify(),
                                                                            )
                                                                        ]
                                                                    ).stringify(),
                                                                )
                                                            ]
                                                        ).stringify(),
                                                    )
                                                ]
                                            ).stringify(),
                                        )
                                    ]
                                ).stringify(),
                            )
                        ]
                    ).stringify(),
                )
            ]
        ).stringify()
        == """
+---------------------------------------+
| +-----------------------------------+ |
| | +-------------------------------+ | |
| | | +---------------------------+ | | |
| | | | +-----------------------+ | | | |
| | | | | +-------------------+ | | | | |
| | | | | | +---------------+ | | | | | |
| | | | | | | +-----------+ | | | | | | |
| | | | | | | |         1 | | | | | | | |
| | | | | | | +-----------+ | | | | | | |
| | | | | | | | +---+---+ | | | | | | | |
| | | | | | | | | 2 | 3 | | | | | | | | |
| | | | | | | | +---+---+ | | | | | | | |
| | | | | | | +-----------+ | | | | | | |
| | | | | | +---------------+ | | | | | |
| | | | | +-------------------+ | | | | |
| | | | +-----------------------+ | | | |
| | | +---------------------------+ | | |
| | +-------------------------------+ | |
| +-----------------------------------+ |
+---------------------------------------+
""".strip()
    )
    assert (
        Table(
            [
                (
                    Table(
                        [
                            (
                                Table(
                                    [
                                        (
                                            Table(
                                                [
                                                    (
                                                        Table(
                                                            [
                                                                (
                                                                    Table(
                                                                        [
                                                                            (
                                                                                Table(
                                                                                    [
                                                                                        (
                                                                                            Table(
                                                                                                [
                                                                                                    (
                                                                                                        "1",
                                                                                                    ),
                                                                                                    (
                                                                                                        Table(
                                                                                                            [
                                                                                                                (
                                                                                                                    "2",
                                                                                                                    "3",
                                                                                                                )
                                                                                                            ]
                                                                                                        ),
                                                                                                    ),
                                                                                                ]
                                                                                            ),
                                                                                        )
                                                                                    ]
                                                                                ),
                                                                            )
                                                                        ]
                                                                    ),
                                                                )
                                                            ]
                                                        ),
                                                    )
                                                ]
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ]
                    ),
                )
            ]
        ).stringify()
        == """
+-------+
|     1 |
+---+---+
| 2 | 3 |
+---+---+
""".strip()
    )
