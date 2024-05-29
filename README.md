# table2string

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/EgorKhabarov/table2string/tests.yml?style=flat&logo=GitHub&label=Tests)](https://github.com/EgorKhabarov/table2string/actions/workflows/tests.yml)
[![Publish Python Package to PyPI](https://img.shields.io/github/actions/workflow/status/EgorKhabarov/table2string/publish.yml?style=flat&logo=GitHub&label=Publish%20to%20PyPI)](https://github.com/EgorKhabarov/table2string/actions/workflows/publish.yml)

[![PyPi Package Version](https://img.shields.io/pypi/v/table2string.svg?style=flat&logo=pypi)](https://pypi.python.org/pypi/table2string)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/table2string.svg?style=flat&logo=pypi)](https://pypi.python.org/pypi/table2string)
[![PyPi status](https://img.shields.io/pypi/status/table2string.svg?style=flat&logo=pypi)](https://pypi.python.org/pypi/table2string)
[![PyPi downloads](https://img.shields.io/pypi/dm/table2string.svg?style=flat&logo=pypi)](https://pypi.org/project/table2string/)

## Convert table to string

While there are several libraries available for converting tables to strings in Python, none seemed to meet my specific requirements. 

- **Line Break Support:** Easily include line breaks within cells for enhanced readability.
- **Emoji Integration:** Effortlessly incorporate emoji characters into your tables to add visual appeal and context.

---

# Install

# PyPI

```shell
pip install -U table2string
```

## GitHub

```shell
pip install -U git+https://github.com/EgorKhabarov/table2string.git@master
```

---

## Usage example

```pycon
>>> from table2string import print_table, stringify_table
>>> print_table([("1", "2", "3"), ("qwe", "rty\nuio", "")], name="Table Name")
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print(stringify_table([("1", "2", "3"), ("qwe", "rty\nuio", "")], name="Table Name"))
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+

```

## Custom width and height settings

<details>
<summary>Example</summary>

```pycon
>>> # Width of the entire table with borders
>>> print_table([(1,), (2.345,), ("example",)], max_width=10)
+--------+
|      1 |
+--------+
|  2.345 |
+--------+
| exampl↩|
| e      |
+--------+
>>> # Width of each column individually
>>> print_table([(1,), (2.345,), ("example",)], max_width=(10,))
+------------+
|          1 |
+------------+
|      2.345 |
+------------+
| example    |
+------------+
>>> print_table([("123456\n\n789000", "example")], max_width=(3, 4), max_height=4)
+-----+------+
| 123↩| exam↩|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> print_table([("123456789",)], max_width=(1,), max_height=1)
+---+
| 1…|
+---+
>>> print_table(
...     table=[("123\n456\n789",)],
...     max_width=(3,),
...     max_height=4,
...     maximize_height=True,
... )
+-----+
| 123 |
| 456 |
| 789 |
|     |
+-----+
>>> print_table(
...     table=[("123456789",)],
...     max_width=(3,),
...     max_height=4,
...     maximize_height=True,
... )
+-----+
| 123↩|
| 456↩|
| 789 |
|     |
+-----+

```
</details>

## Text alignment

<details>
<summary>Example</summary>

```pycon
>>> kwargs_1 = {
...     "table": [("1", "123456789\nqwerty\nasdfghjklzxcvb")],
...     "name": "Table Name\nName\nNaaaaame",
...     "max_width": (5, 15),
... }
>>> print_table(**kwargs_1)
+-------------------------+
|       Table Name        |
|          Name           |
|        Naaaaame         |
+-------+-----------------+
|     1 | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="*", name_align="*")  # align="**", name_align="**"
+-------------------------+
| Table Name              |
| Name                    |
| Naaaaame                |
+-------+-----------------+
|     1 | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="<", name_align="<")  # align="<<", name_align="<<"
+-------------------------+
| Table Name              |
| Name                    |
| Naaaaame                |
+-------+-----------------+
| 1     | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align=">", name_align=">")  # align=">>", name_align=">>"
+-------------------------+
|              Table Name |
|                    Name |
|                Naaaaame |
+-------+-----------------+
|     1 |       123456789 |
|       |          qwerty |
|       |  asdfghjklzxcvb |
+-------+-----------------+
>>> print_table(**kwargs_1, align="^", name_align="^")  # align="^^", name_align="^^"
+-------------------------+
|       Table Name        |
|          Name           |
|        Naaaaame         |
+-------+-----------------+
|   1   |    123456789    |
|       |     qwerty      |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="^<", name_align="^<")
+-------------------------+
|       Table Name        |
|       Name              |
|       Naaaaame          |
+-------+-----------------+
|   1   | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="^>", name_align="^>")
+-------------------------+
|       Table Name        |
|             Name        |
|         Naaaaame        |
+-------+-----------------+
|   1   |      123456789  |
|       |         qwerty  |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table([("qwerty\n123456789\nasdfghjklzxcvb",)], max_width=(18,), align="^<")
+--------------------+
|   qwerty           |
|   123456789        |
|   asdfghjklzxcvb   |
+--------------------+
>>> print_table([("qwerty\n123456789\nasdfghjklzxcvb",)], max_width=(18,), align="^>")
+--------------------+
|           qwerty   |
|        123456789   |
|   asdfghjklzxcvb   |
+--------------------+

```
</details>

# Separator settings

<details>
<summary>Example</summary>

```pycon
>>> table_1 = [("qwe", "rty\nuio"), ("123456\n\n789000", "example")]
>>> kwargs = {
...     "max_width": (3, 4),
...     "max_height": 4,
...     "line_break_symbol": "/",
...     "cell_break_symbol": "…",
... }
>>> print_table(table_1, **kwargs, sep=True)
+-----+------+
| qwe | rty  |
|     | uio  |
+-----+------+
| 123/| exam/|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> print_table(table_1, **kwargs, sep=False)
+-----+------+
| qwe | rty  |
|     | uio  |
| 123/| exam/|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> table_2 = [("1", "2"), ("3", "4")]
>>> print_table(table_2, sep=True, name="Name")
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
+---+---+
>>> print_table(table_2, sep=False, name="Name")
+-------+
| Name  |
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
>>> table_3 = [("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")]
>>> print_table(table_3, sep=(1,))
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> print_table(table_3, sep=(2,))
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> print_table(table_3, sep=(1, 3))
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
+---+---+
| 7 | 8 |
+---+---+
>>> print_table(table_3, sep=(1,), name="Name")
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> print_table(table_3, sep=(2,), name="Name")
+-------+
| Name  |
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> print_table(table_3, sep=(1, 3), name="Name")
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

```
</details>

# Borders

<details>
<summary>Border types</summary>

```text
╭───────────────────┬───────────────────────┬───────────────────────╮
│    ascii_thin     │ +---------+---------+ │ +-------------------+ │
│                   │ |    _    |    _    | │ |    ascii_thin     | │
│                   │ +---------+---------+ │ +---------+---------+ │
│                   │ |    _    |    _    | │ |    _    |    _    | │
│                   │ +---------+---------+ │ +---------+---------+ │
│                   │ |    _    |    _    | │ |    _    |    _    | │
│                   │ +---------+---------+ │ +---------+---------+ │
│                   │                       │ |    _    |    _    | │
│                   │                       │ +---------+---------+ │
├───────────────────┼───────────────────────┼───────────────────────┤
│ ascii_thin_double │ +---------+---------+ │ +-------------------+ │
│                   │ |    _    |    _    | │ | ascii_thin_double | │
│                   │ +=========+=========+ │ +---------+---------+ │
│                   │ |    _    |    _    | │ |    _    |    _    | │
│                   │ +---------+---------+ │ +=========+=========+ │
│                   │ |    _    |    _    | │ |    _    |    _    | │
│                   │ +---------+---------+ │ +---------+---------+ │
│                   │                       │ |    _    |    _    | │
│                   │                       │ +---------+---------+ │
├───────────────────┼───────────────────────┼───────────────────────┤
│   ascii_double    │ +=========+=========+ │ +===================+ │
│                   │ ‖    _    ‖    _    ‖ │ ‖   ascii_double    ‖ │
│                   │ +=========+=========+ │ +=========+=========+ │
│                   │ ‖    _    ‖    _    ‖ │ ‖    _    ‖    _    ‖ │
│                   │ +=========+=========+ │ +=========+=========+ │
│                   │ ‖    _    ‖    _    ‖ │ ‖    _    ‖    _    ‖ │
│                   │ +=========+=========+ │ +=========+=========+ │
│                   │                       │ ‖    _    ‖    _    ‖ │
│                   │                       │ +=========+=========+ │
├───────────────────┼───────────────────────┼───────────────────────┤
│ ascii_double_thin │ +=========+=========+ │ +===================+ │
│                   │ ‖    _    ‖    _    ‖ │ ‖ ascii_double_thin ‖ │
│                   │ +---------+---------+ │ +=========+=========+ │
│                   │ ‖    _    ‖    _    ‖ │ ‖    _    ‖    _    ‖ │
│                   │ +=========+=========+ │ +---------+---------+ │
│                   │ ‖    _    ‖    _    ‖ │ ‖    _    ‖    _    ‖ │
│                   │ +=========+=========+ │ +=========+=========+ │
│                   │                       │ ‖    _    ‖    _    ‖ │
│                   │                       │ +=========+=========+ │
├───────────────────┼───────────────────────┼───────────────────────┤
│  ascii_booktabs   │  -------------------  │  -------------------  │
│                   │      _         _      │    ascii_booktabs     │
│                   │  ===================  │  -------------------  │
│                   │      _         _      │      _         _      │
│                   │  -------------------  │  ===================  │
│                   │      _         _      │      _         _      │
│                   │  -------------------  │  -------------------  │
│                   │                       │      _         _      │
│                   │                       │  -------------------  │
├───────────────────┼───────────────────────┼───────────────────────┤
│       thin        │ ┌─────────┬─────────┐ │ ┌───────────────────┐ │
│                   │ │    _    │    _    │ │ │       thin        │ │
│                   │ ├─────────┼─────────┤ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ├─────────┼─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ └─────────┴─────────┘ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ └─────────┴─────────┘ │
├───────────────────┼───────────────────────┼───────────────────────┤
│    thin_thick     │ ┌─────────┬─────────┐ │ ┌───────────────────┐ │
│                   │ │    _    │    _    │ │ │    thin_thick     │ │
│                   │ ┝━━━━━━━━━┿━━━━━━━━━┥ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ┝━━━━━━━━━┿━━━━━━━━━┥ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ └─────────┴─────────┘ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ └─────────┴─────────┘ │
├───────────────────┼───────────────────────┼───────────────────────┤
│    thin_double    │ ┌─────────┬─────────┐ │ ┌───────────────────┐ │
│                   │ │    _    │    _    │ │ │    thin_double    │ │
│                   │ ╞═════════╪═════════╡ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ╞═════════╪═════════╡ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ └─────────┴─────────┘ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ └─────────┴─────────┘ │
├───────────────────┼───────────────────────┼───────────────────────┤
│      rounded      │ ╭─────────┬─────────╮ │ ╭───────────────────╮ │
│                   │ │    _    │    _    │ │ │      rounded      │ │
│                   │ ├─────────┼─────────┤ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ├─────────┼─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ╰─────────┴─────────╯ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ ╰─────────┴─────────╯ │
├───────────────────┼───────────────────────┼───────────────────────┤
│   rounded_thick   │ ╭─────────┬─────────╮ │ ╭───────────────────╮ │
│                   │ │    _    │    _    │ │ │   rounded_thick   │ │
│                   │ ┝━━━━━━━━━┿━━━━━━━━━┥ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ┝━━━━━━━━━┿━━━━━━━━━┥ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ╰─────────┴─────────╯ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ ╰─────────┴─────────╯ │
├───────────────────┼───────────────────────┼───────────────────────┤
│  rounded_double   │ ╭─────────┬─────────╮ │ ╭───────────────────╮ │
│                   │ │    _    │    _    │ │ │  rounded_double   │ │
│                   │ ╞═════════╪═════════╡ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ╞═════════╪═════════╡ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ╰─────────┴─────────╯ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ ╰─────────┴─────────╯ │
├───────────────────┼───────────────────────┼───────────────────────┤
│       thick       │ ┏━━━━━━━━━┳━━━━━━━━━┓ │ ┏━━━━━━━━━━━━━━━━━━━┓ │
│                   │ ┃    _    ┃    _    ┃ │ ┃       thick       ┃ │
│                   │ ┣━━━━━━━━━╋━━━━━━━━━┫ │ ┣━━━━━━━━━┳━━━━━━━━━┫ │
│                   │ ┃    _    ┃    _    ┃ │ ┃    _    ┃    _    ┃ │
│                   │ ┣━━━━━━━━━╋━━━━━━━━━┫ │ ┣━━━━━━━━━╋━━━━━━━━━┫ │
│                   │ ┃    _    ┃    _    ┃ │ ┃    _    ┃    _    ┃ │
│                   │ ┗━━━━━━━━━┻━━━━━━━━━┛ │ ┣━━━━━━━━━╋━━━━━━━━━┫ │
│                   │                       │ ┃    _    ┃    _    ┃ │
│                   │                       │ ┗━━━━━━━━━┻━━━━━━━━━┛ │
├───────────────────┼───────────────────────┼───────────────────────┤
│    thick_thin     │ ┌─────────┬─────────┐ │ ┌───────────────────┐ │
│                   │ │    _    │    _    │ │ │    thick_thin     │ │
│                   │ ┠━━━━━━━━━╂━━━━━━━━━┨ │ ├─────────┬─────────┤ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ ├─────────┼─────────┤ │ ┠━━━━━━━━━╂━━━━━━━━━┨ │
│                   │ │    _    │    _    │ │ │    _    │    _    │ │
│                   │ └─────────┴─────────┘ │ ├─────────┼─────────┤ │
│                   │                       │ │    _    │    _    │ │
│                   │                       │ └─────────┴─────────┘ │
├───────────────────┼───────────────────────┼───────────────────────┤
│      double       │ ╔═════════╦═════════╗ │ ╔═══════════════════╗ │
│                   │ ║    _    ║    _    ║ │ ║      double       ║ │
│                   │ ╠═════════╬═════════╣ │ ╠═════════╦═════════╣ │
│                   │ ║    _    ║    _    ║ │ ║    _    ║    _    ║ │
│                   │ ╠═════════╬═════════╣ │ ╠═════════╬═════════╣ │
│                   │ ║    _    ║    _    ║ │ ║    _    ║    _    ║ │
│                   │ ╚═════════╩═════════╝ │ ╠═════════╬═════════╣ │
│                   │                       │ ║    _    ║    _    ║ │
│                   │                       │ ╚═════════╩═════════╝ │
├───────────────────┼───────────────────────┼───────────────────────┤
│    double_thin    │ ╔═════════╦═════════╗ │ ╔═══════════════════╗ │
│                   │ ║    _    ║    _    ║ │ ║    double_thin    ║ │
│                   │ ╟─────────╫─────────╢ │ ╠═════════╦═════════╣ │
│                   │ ║    _    ║    _    ║ │ ║    _    ║    _    ║ │
│                   │ ╠═════════╬═════════╣ │ ╟─────────╫─────────╢ │
│                   │ ║    _    ║    _    ║ │ ║    _    ║    _    ║ │
│                   │ ╚═════════╩═════════╝ │ ╠═════════╬═════════╣ │
│                   │                       │ ║    _    ║    _    ║ │
│                   │                       │ ╚═════════╩═════════╝ │
├───────────────────┼───────────────────────┼───────────────────────┤
│     booktabs      │  ───────────────────  │  ───────────────────  │
│                   │      _         _      │       booktabs        │
│                   │  ━━━━━━━━━━━━━━━━━━━  │  ───────────────────  │
│                   │      _         _      │      _         _      │
│                   │  ───────────────────  │  ━━━━━━━━━━━━━━━━━━━  │
│                   │      _         _      │      _         _      │
│                   │  ───────────────────  │  ───────────────────  │
│                   │                       │      _         _      │
│                   │                       │  ───────────────────  │
├───────────────────┼───────────────────────┼───────────────────────┤
│     markdown      │ |    _    |    _    | │ |     markdown      | │
│                   │ |---------|---------| │ |    _    |    _    | │
│                   │ |    _    |    _    | │ |---------|---------| │
│                   │ |    _    |    _    | │ |    _    |    _    | │
│                   │                       │ |    _    |    _    | │
╰───────────────────┴───────────────────────┴───────────────────────╯
```
</details>

<details>
<summary>Example</summary>

```pycon
>>> from table2string import BORDERS
>>> table_1 = [("1", "2", "3"), ("qwe", "rty\nuio", "")]
>>> name_1 = "Table Name"
>>> print_table(table_1, border=BORDERS["ascii_thin"])
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, border=BORDERS["ascii_thin"], name=name_1)
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, border=BORDERS["ascii_thin_double"])
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, border=BORDERS["ascii_thin_double"], name=name_1)
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, border=BORDERS["ascii_double"])
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, border=BORDERS["ascii_double"], name=name_1)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, border=BORDERS["ascii_double_thin"])
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, border=BORDERS["ascii_double_thin"], name=name_1)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, border=BORDERS["ascii_booktabs"])
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
>>> print_table(table_1, border=BORDERS["ascii_booktabs"], name=name_1)
 --------------- 
   Table Name    
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
>>> print_table(table_1, border=BORDERS["thin"])
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["thin"], name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["thin_thick"])
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["thin_thick"], name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["thin_double"])
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["thin_double"], name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["rounded"])
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, border=BORDERS["rounded"], name=name_1)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, border=BORDERS["rounded_thick"])
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, border=BORDERS["rounded_thick"], name=name_1)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, border=BORDERS["rounded_double"])
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, border=BORDERS["rounded_double"], name=name_1)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, border=BORDERS["thick"])
┏━━━━━┳━━━━━┳━━━┓
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> print_table(table_1, border=BORDERS["thick"], name=name_1)
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> print_table(table_1, border=BORDERS["thick_thin"])
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┠━━━━━╂━━━━━╂━━━┨
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["thick_thin"], name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┠━━━━━╂━━━━━╂━━━┨
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, border=BORDERS["double"])
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, border=BORDERS["double"], name=name_1)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, border=BORDERS["double_thin"])
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, border=BORDERS["double_thin"], name=name_1)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, border=BORDERS["booktabs"])
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
>>> print_table(table_1, border=BORDERS["booktabs"], name=name_1)
 ─────────────── 
   Table Name    
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
>>> print_table(table_1, border=BORDERS["markdown"])
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |
>>> print_table(table_1, border=BORDERS["markdown"], name=name_1)
|  Table Name   |
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |

```

</details>
