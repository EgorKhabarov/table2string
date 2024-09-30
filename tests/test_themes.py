from table2string import Table, Themes


def test_themes():
    table = Table(
        [
            ("1", "2", "3"),
            ("3", Table([("4.1", "4.2"), ("4.3", "4.4")]), "5"),
            ("6", "7", "8"),
            ("9", "10", "11"),
            (
                Table([("1",), (Table([("2", "3")]),)]),
                Table([(Table([("2", "3")]),), ("1",)]),
                "14",
            ),
            (
                "15",
                Table([("1", Table([("2",), ("3",)]))]),
                Table([(Table([("2",), ("3",)]), "1")]),
            ),
        ],
    )

    assert (
        table.stringify(theme=Themes.ascii_booktabs)
        == """
 --------------------------- 
      1           2       3  
 =========================== 
      3   4.1   4.2       5  
         ===========         
          4.3   4.4          
 --------------------------- 
      6           7       8  
 --------------------------- 
      9          10      11  
 --------------------------- 
      1     2     3      14  
 ======= ===========         
  2   3           1          
 --------------------------- 
     15     1     2   2   1  
               ===== ===     
                  3   3      
 --------------------------- 
""".strip(
            "\n"
        )
    )
    assert (
        table.stringify(theme=Themes.ascii_double)
        == """
+=======+===========+=======+
‖     1 ‖         2 ‖     3 ‖
+=======+=====+=====+=======+
‖     3 ‖ 4.1 ‖ 4.2 ‖     5 ‖
‖       +=====+=====+       ‖
‖       ‖ 4.3 ‖ 4.4 ‖       ‖
+=======+=====+=====+=======+
‖     6 ‖         7 ‖     8 ‖
+=======+===========+=======+
‖     9 ‖        10 ‖    11 ‖
+=======+=====+=====+=======+
‖     1 ‖   2 ‖   3 ‖    14 ‖
+===+===+=====+=====+       ‖
‖ 2 ‖ 3 ‖         1 ‖       ‖
+===+===+=====+=====+===+===+
‖    15 ‖   1 ‖   2 ‖ 2 ‖ 1 ‖
‖       ‖     +=====+===+   ‖
‖       ‖     ‖   3 ‖ 3 ‖   ‖
+=======+=====+=====+===+===+
""".strip()
    )
    assert (
        table.stringify(theme=Themes.ascii_double_thin)
        == """
+=======+===========+=======+
‖     1 ‖         2 ‖     3 ‖
+-------+-----+-----+-------+
‖     3 ‖ 4.1 ‖ 4.2 ‖     5 ‖
‖       +=====+=====+       ‖
‖       ‖ 4.3 ‖ 4.4 ‖       ‖
+=======+=====+=====+=======+
‖     6 ‖         7 ‖     8 ‖
+=======+===========+=======+
‖     9 ‖        10 ‖    11 ‖
+=======+=====+=====+=======+
‖     1 ‖   2 ‖   3 ‖    14 ‖
+===+===+=====+=====+       ‖
‖ 2 ‖ 3 ‖         1 ‖       ‖
+===+===+=====+=====+===+===+
‖    15 ‖   1 ‖   2 ‖ 2 ‖ 1 ‖
‖       ‖     +=====+===+   ‖
‖       ‖     ‖   3 ‖ 3 ‖   ‖
+=======+=====+=====+===+===+
""".strip()
    )
    assert (
        table.stringify(theme=Themes.ascii_thin)
        == """
+-------+-----------+-------+
|     1 |         2 |     3 |
+-------+-----+-----+-------+
|     3 | 4.1 | 4.2 |     5 |
|       +-----+-----+       |
|       | 4.3 | 4.4 |       |
+-------+-----+-----+-------+
|     6 |         7 |     8 |
+-------+-----------+-------+
|     9 |        10 |    11 |
+-------+-----+-----+-------+
|     1 |   2 |   3 |    14 |
+---+---+-----+-----+       |
| 2 | 3 |         1 |       |
+---+---+-----+-----+---+---+
|    15 |   1 |   2 | 2 | 1 |
|       |     +-----+---+   |
|       |     |   3 | 3 |   |
+-------+-----+-----+---+---+
""".strip()
    )
    assert (
        table.stringify(theme=Themes.ascii_thin_double)
        == """
+-------+-----------+-------+
|     1 |         2 |     3 |
+=======+=====+=====+=======+
|     3 | 4.1 | 4.2 |     5 |
|       +-----+-----+       |
|       | 4.3 | 4.4 |       |
+-------+-----+-----+-------+
|     6 |         7 |     8 |
+-------+-----------+-------+
|     9 |        10 |    11 |
+-------+-----+-----+-------+
|     1 |   2 |   3 |    14 |
+---+---+-----+-----+       |
| 2 | 3 |         1 |       |
+---+---+-----+-----+---+---+
|    15 |   1 |   2 | 2 | 1 |
|       |     +-----+---+   |
|       |     |   3 | 3 |   |
+-------+-----+-----+---+---+
""".strip()
    )
    assert (
        table.stringify(theme=Themes.booktabs)
        == """
 ─────────────────────────── 
      1           2       3  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
      3   4.1   4.2       5  
         ━━━━━━━━━━━         
          4.3   4.4          
 ─────────────────────────── 
      6           7       8  
 ─────────────────────────── 
      9          10      11  
 ─────────────────────────── 
      1     2     3      14  
 ━━━━━━━ ━━━━━━━━━━━         
  2   3           1          
 ─────────────────────────── 
     15     1     2   2   1  
               ━━━━━ ━━━     
                  3   3      
 ─────────────────────────── 
""".strip(
            "\n"
        )
    )
    assert (
        table.stringify(theme=Themes.double)
        == """
╔═══════╦═══════════╦═══════╗
║     1 ║         2 ║     3 ║
╠═══════╬═════╦═════╬═══════╣
║     3 ║ 4.1 ║ 4.2 ║     5 ║
║       ╠═════╬═════╣       ║
║       ║ 4.3 ║ 4.4 ║       ║
╠═══════╬═════╩═════╬═══════╣
║     6 ║         7 ║     8 ║
╠═══════╬═══════════╬═══════╣
║     9 ║        10 ║    11 ║
╠═══════╬═════╦═════╬═══════╣
║     1 ║   2 ║   3 ║    14 ║
╠═══╦═══╬═════╩═════╣       ║
║ 2 ║ 3 ║         1 ║       ║
╠═══╩═══╬═════╦═════╬═══╦═══╣
║    15 ║   1 ║   2 ║ 2 ║ 1 ║
║       ║     ╠═════╬═══╣   ║
║       ║     ║   3 ║ 3 ║   ║
╚═══════╩═════╩═════╩═══╩═══╝
""".strip()
    )
    assert (
        table.stringify(theme=Themes.double_thin)
        == """
╔═══════╦═══════════╦═══════╗
║     1 ║         2 ║     3 ║
╟───────╫─────╥─────╫───────╢
║     3 ║ 4.1 ║ 4.2 ║     5 ║
║       ╠═════╬═════╣       ║
║       ║ 4.3 ║ 4.4 ║       ║
╠═══════╬═════╩═════╬═══════╣
║     6 ║         7 ║     8 ║
╠═══════╬═══════════╬═══════╣
║     9 ║        10 ║    11 ║
╠═══════╬═════╦═════╬═══════╣
║     1 ║   2 ║   3 ║    14 ║
╠═══╦═══╬═════╩═════╣       ║
║ 2 ║ 3 ║         1 ║       ║
╠═══╩═══╬═════╦═════╬═══╦═══╣
║    15 ║   1 ║   2 ║ 2 ║ 1 ║
║       ║     ╠═════╬═══╣   ║
║       ║     ║   3 ║ 3 ║   ║
╚═══════╩═════╩═════╩═══╩═══╝
""".strip()
    )
    assert (
        table.stringify(theme=Themes.markdown)
        == """
|     1 |         2 |     3 |
|-------|-----------|-------|
|     3 | 4.1 | 4.2 |     5 |
|       |-----+-----|       |
|       | 4.3 | 4.4 |       |
|     6 |         7 |     8 |
|     9 |        10 |    11 |
|     1 |   2 |   3 |    14 |
|---+---|-----+-----|       |
| 2 | 3 |         1 |       |
|    15 |   1 |   2 | 2 | 1 |
|       |     +-----|---+   |
|       |     |   3 | 3 |   |
""".strip()
    )
    assert (
        table.stringify(theme=Themes.rounded)
        == """
╭───────┬───────────┬───────╮
│     1 │         2 │     3 │
├───────┼─────┬─────┼───────┤
│     3 │ 4.1 │ 4.2 │     5 │
│       ├─────┼─────┤       │
│       │ 4.3 │ 4.4 │       │
├───────┼─────┴─────┼───────┤
│     6 │         7 │     8 │
├───────┼───────────┼───────┤
│     9 │        10 │    11 │
├───────┼─────┬─────┼───────┤
│     1 │   2 │   3 │    14 │
├───┬───┼─────┴─────┤       │
│ 2 │ 3 │         1 │       │
├───┴───┼─────┬─────┼───┬───┤
│    15 │   1 │   2 │ 2 │ 1 │
│       │     ├─────┼───┤   │
│       │     │   3 │ 3 │   │
╰───────┴─────┴─────┴───┴───╯
""".strip()
    )
    assert (
        table.stringify(theme=Themes.rounded_double)
        == """
╭───────┬───────────┬───────╮
│     1 │         2 │     3 │
╞═══════╪═════╤═════╪═══════╡
│     3 │ 4.1 │ 4.2 │     5 │
│       ├─────┼─────┤       │
│       │ 4.3 │ 4.4 │       │
├───────┼─────┴─────┼───────┤
│     6 │         7 │     8 │
├───────┼───────────┼───────┤
│     9 │        10 │    11 │
├───────┼─────┬─────┼───────┤
│     1 │   2 │   3 │    14 │
├───┬───┼─────┴─────┤       │
│ 2 │ 3 │         1 │       │
├───┴───┼─────┬─────┼───┬───┤
│    15 │   1 │   2 │ 2 │ 1 │
│       │     ├─────┼───┤   │
│       │     │   3 │ 3 │   │
╰───────┴─────┴─────┴───┴───╯
""".strip()
    )
    assert (
        table.stringify(theme=Themes.rounded_thick)
        == """
╭───────┬───────────┬───────╮
│     1 │         2 │     3 │
┝━━━━━━━┿━━━━━┯━━━━━┿━━━━━━━┥
│     3 │ 4.1 │ 4.2 │     5 │
│       ├─────┼─────┤       │
│       │ 4.3 │ 4.4 │       │
├───────┼─────┴─────┼───────┤
│     6 │         7 │     8 │
├───────┼───────────┼───────┤
│     9 │        10 │    11 │
├───────┼─────┬─────┼───────┤
│     1 │   2 │   3 │    14 │
├───┬───┼─────┴─────┤       │
│ 2 │ 3 │         1 │       │
├───┴───┼─────┬─────┼───┬───┤
│    15 │   1 │   2 │ 2 │ 1 │
│       │     ├─────┼───┤   │
│       │     │   3 │ 3 │   │
╰───────┴─────┴─────┴───┴───╯
""".strip()
    )
    assert (
        table.stringify(theme=Themes.thick)
        == """
┏━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃     1 ┃         2 ┃     3 ┃
┣━━━━━━━╋━━━━━┳━━━━━╋━━━━━━━┫
┃     3 ┃ 4.1 ┃ 4.2 ┃     5 ┃
┃       ┣━━━━━╋━━━━━┫       ┃
┃       ┃ 4.3 ┃ 4.4 ┃       ┃
┣━━━━━━━╋━━━━━┻━━━━━╋━━━━━━━┫
┃     6 ┃         7 ┃     8 ┃
┣━━━━━━━╋━━━━━━━━━━━╋━━━━━━━┫
┃     9 ┃        10 ┃    11 ┃
┣━━━━━━━╋━━━━━┳━━━━━╋━━━━━━━┫
┃     1 ┃   2 ┃   3 ┃    14 ┃
┣━━━┳━━━╋━━━━━┻━━━━━┫       ┃
┃ 2 ┃ 3 ┃         1 ┃       ┃
┣━━━┻━━━╋━━━━━┳━━━━━╋━━━┳━━━┫
┃    15 ┃   1 ┃   2 ┃ 2 ┃ 1 ┃
┃       ┃     ┣━━━━━╋━━━┫   ┃
┃       ┃     ┃   3 ┃ 3 ┃   ┃
┗━━━━━━━┻━━━━━┻━━━━━┻━━━┻━━━┛
""".strip()
    )
    assert (
        table.stringify(theme=Themes.thick_thin)
        == """
┏━━━━━━━┳━━━━━━━━━━━┳━━━━━━━┓
┃     1 ┃         2 ┃     3 ┃
┠───────╂─────┰─────╂───────┨
┃     3 ┃ 4.1 ┃ 4.2 ┃     5 ┃
┃       ┣━━━━━╋━━━━━┫       ┃
┃       ┃ 4.3 ┃ 4.4 ┃       ┃
┣━━━━━━━╋━━━━━┻━━━━━╋━━━━━━━┫
┃     6 ┃         7 ┃     8 ┃
┣━━━━━━━╋━━━━━━━━━━━╋━━━━━━━┫
┃     9 ┃        10 ┃    11 ┃
┣━━━━━━━╋━━━━━┳━━━━━╋━━━━━━━┫
┃     1 ┃   2 ┃   3 ┃    14 ┃
┣━━━┳━━━╋━━━━━┻━━━━━┫       ┃
┃ 2 ┃ 3 ┃         1 ┃       ┃
┣━━━┻━━━╋━━━━━┳━━━━━╋━━━┳━━━┫
┃    15 ┃   1 ┃   2 ┃ 2 ┃ 1 ┃
┃       ┃     ┣━━━━━╋━━━┫   ┃
┃       ┃     ┃   3 ┃ 3 ┃   ┃
┗━━━━━━━┻━━━━━┻━━━━━┻━━━┻━━━┛
""".strip()
    )
    assert (
        table.stringify(theme=Themes.thin)
        == """
┌───────┬───────────┬───────┐
│     1 │         2 │     3 │
├───────┼─────┬─────┼───────┤
│     3 │ 4.1 │ 4.2 │     5 │
│       ├─────┼─────┤       │
│       │ 4.3 │ 4.4 │       │
├───────┼─────┴─────┼───────┤
│     6 │         7 │     8 │
├───────┼───────────┼───────┤
│     9 │        10 │    11 │
├───────┼─────┬─────┼───────┤
│     1 │   2 │   3 │    14 │
├───┬───┼─────┴─────┤       │
│ 2 │ 3 │         1 │       │
├───┴───┼─────┬─────┼───┬───┤
│    15 │   1 │   2 │ 2 │ 1 │
│       │     ├─────┼───┤   │
│       │     │   3 │ 3 │   │
└───────┴─────┴─────┴───┴───┘
""".strip()
    )
    assert (
        table.stringify(theme=Themes.thin_double)
        == """
┌───────┬───────────┬───────┐
│     1 │         2 │     3 │
╞═══════╪═════╤═════╪═══════╡
│     3 │ 4.1 │ 4.2 │     5 │
│       ├─────┼─────┤       │
│       │ 4.3 │ 4.4 │       │
├───────┼─────┴─────┼───────┤
│     6 │         7 │     8 │
├───────┼───────────┼───────┤
│     9 │        10 │    11 │
├───────┼─────┬─────┼───────┤
│     1 │   2 │   3 │    14 │
├───┬───┼─────┴─────┤       │
│ 2 │ 3 │         1 │       │
├───┴───┼─────┬─────┼───┬───┤
│    15 │   1 │   2 │ 2 │ 1 │
│       │     ├─────┼───┤   │
│       │     │   3 │ 3 │   │
└───────┴─────┴─────┴───┴───┘
""".strip()
    )
    assert (
        table.stringify(theme=Themes.thin_thick)
        == """
┌───────┬───────────┬───────┐
│     1 │         2 │     3 │
┝━━━━━━━┿━━━━━┯━━━━━┿━━━━━━━┥
│     3 │ 4.1 │ 4.2 │     5 │
│       ├─────┼─────┤       │
│       │ 4.3 │ 4.4 │       │
├───────┼─────┴─────┼───────┤
│     6 │         7 │     8 │
├───────┼───────────┼───────┤
│     9 │        10 │    11 │
├───────┼─────┬─────┼───────┤
│     1 │   2 │   3 │    14 │
├───┬───┼─────┴─────┤       │
│ 2 │ 3 │         1 │       │
├───┴───┼─────┬─────┼───┬───┤
│    15 │   1 │   2 │ 2 │ 1 │
│       │     ├─────┼───┤   │
│       │     │   3 │ 3 │   │
└───────┴─────┴─────┴───┴───┘
""".strip()
    )
    assert (
        table.stringify(theme=Themes.markdown, end="\n")
        == """
|     1 |         2 |     3 |
|-------|-----------|-------|
|     3 | 4.1 | 4.2 |     5 |
|       |-----+-----|       |
|       | 4.3 | 4.4 |       |
|     6 |         7 |     8 |
|     9 |        10 |    11 |
|     1 |   2 |   3 |    14 |
|---+---|-----+-----|       |
| 2 | 3 |         1 |       |
|    15 |   1 |   2 | 2 | 1 |
|       |     +-----|---+   |
|       |     |   3 | 3 |   |
""".lstrip()
    )
    assert repr(Themes.thin) == "Themes.thin"
