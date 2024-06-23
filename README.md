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

## PyPI

```shell
pip install -U table2string
```

## GitHub

```shell
pip install -U git+https://github.com/EgorKhabarov/table2string.git@master
```

---

# Usage example

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
>>> from io import StringIO
>>> from table2string import Table
>>> Table.from_csv(StringIO('c1,c2,c3\n1,2,3\nqwe,"rty\nuio",'), name="Table Name").print()
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
>>> Table.from_csv(StringIO('c1,c2,c3\n1,2,3\nqwe,"rty\nuio",'), name="Table Name", column_names=False).print()
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> import sqlite3
>>> cursor = sqlite3.connect(":memory:").cursor()
>>> cursor.execute(
...     "CREATE TABLE data (c1 TEXT, c2 TEXT, c3 TEXT);"
... ).executemany(
...     "INSERT INTO data (c1, c2, c3) VALUES (?, ?, ?);",
...     [("1", "2", "3"), ("qwe", "rty\nuio", "")],
... ).execute(
...     "SELECT c1, c2, c3 FROM data;"
... ) and None  # because this method returns a cursor
>>> Table.from_db_cursor(cursor, name="Table Name").print()
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> cursor.execute("SELECT c1, c2, c3 FROM data;") and None
>>> Table.from_db_cursor(cursor, name="Table Name", column_names=True).print()
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

```

## Custom width and height settings

| Width                               | Example        | Description                                                                                                                 |
|-------------------------------------|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| `<width>`                           | `10`           | Setting `width` (`10`) for the whole table                                                                                  |
| `(<width>,)`                        | `(10,)`        | Setting `width_1` (`10`) for all column                                                                                     |
| `(<width_1>, <width_2>)`            | `(10, 20)`     | Setting `width_1` (`10`) for the first column and `width_2` (`20`) for all other columns                                    |
| `(<width_1>, <width_2>, <width_3>)` | `(10, 20, 30)` | Setting `width_1` (`10`) for the first column and `width_2` (`20`) for the second and `width_3` (`30`) for the third column |

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

| Align                                     | Example           | Description                                                                                                                    |
|-------------------------------------------|-------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `"<align>"` or `("<align>",)`             | `"^"` or `("^",)` | Setting `align` (`"^"`) for all columns                                                                                        |
| `("<align_1>", "<align_2>")`              | `("^", "<")`      | Setting `align_1` (`"^"`) for the first column and `align_2` (`"<"`) for all other columns                                     |
| `("<align_1>", "<align_2>", "<align_3>")` | `("^", "<", ">")` | Setting `align_1` (`"^"`) for the first column and `align_2` (`"<"`) for the second and `align_3` (`">"`) for the third column |

### ALLOWED_ALIGNS

|    Align    | Description                                                                                                                                          |
|:-----------:|------------------------------------------------------------------------------------------------------------------------------------------------------|
| `*` or `**` | Alignment depends on the type. If this is a number and there are no line breaks in this cell, then align to the right; otherwise, align to the left. |
| `<` or `<<` | All lines are left aligned                                                                                                                           |
| `^` or `^^` | All lines are center aligned                                                                                                                         |
| `>` or `>>` | All lines are right aligned                                                                                                                          |
|    `<^`     | The first line is left aligned and the remaining lines are centered                                                                                  |
|    `<>`     | The first line is left aligned and the remaining lines are right aligned                                                                             |
|    `^<`     | The first line is aligned to the center, and the remaining lines are aligned to the left of the first line.                                          |
|    `^>`     | The first line is aligned to the center, and the remaining lines are aligned to the right of the first line.                                         |
|    `><`     | The first line is right aligned and the remaining lines are left aligned                                                                             |
|    `>^`     | The first line is right aligned and the remaining lines are centered                                                                                 |

<details>
<summary>Example</summary>

```pycon
>>> kwargs_1 = {
...     "table": [("1", "123456789\nqwerty\nasdfghjklzxcvb")],
...     "name": "Table Name\nName\nNaaaaame",
...     "column_names": ("1", "col 2\nc2"),
...     "max_width": (5, 15),
... }
>>> print_table(**kwargs_1)
+-------------------------+
|       Table Name        |
|          Name           |
|        Naaaaame         |
+-------+-----------------+
|   1   |      col 2      |
|       |       c2        |
+-------+-----------------+
|     1 | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="*", name_align="*", column_names_align="*")  # align="**", name_align="**", column_names_align="**"
+-------------------------+
| Table Name              |
| Name                    |
| Naaaaame                |
+-------+-----------------+
|     1 | col 2           |
|       | c2              |
+-------+-----------------+
|     1 | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="<", name_align="<", column_names_align="<")  # align="<<", name_align="<<", column_names_align="<<"
+-------------------------+
| Table Name              |
| Name                    |
| Naaaaame                |
+-------+-----------------+
| 1     | col 2           |
|       | c2              |
+-------+-----------------+
| 1     | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align=">", name_align=">", column_names_align=">")  # align=">>", name_align=">>", column_names_align=">>"
+-------------------------+
|              Table Name |
|                    Name |
|                Naaaaame |
+-------+-----------------+
|     1 |           col 2 |
|       |              c2 |
+-------+-----------------+
|     1 |       123456789 |
|       |          qwerty |
|       |  asdfghjklzxcvb |
+-------+-----------------+
>>> print_table(**kwargs_1, align="^", name_align="^", column_names_align="^")  # align="^^", name_align="^^", column_names_align="^^"
+-------------------------+
|       Table Name        |
|          Name           |
|        Naaaaame         |
+-------+-----------------+
|   1   |      col 2      |
|       |       c2        |
+-------+-----------------+
|   1   |    123456789    |
|       |     qwerty      |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="^<", name_align="^<", column_names_align="^<")
+-------------------------+
|       Table Name        |
|       Name              |
|       Naaaaame          |
+-------+-----------------+
|   1   |      col 2      |
|       |      c2         |
+-------+-----------------+
|   1   | 123456789       |
|       | qwerty          |
|       | asdfghjklzxcvb  |
+-------+-----------------+
>>> print_table(**kwargs_1, align="^>", name_align="^>", column_names_align="^>")
+-------------------------+
|       Table Name        |
|             Name        |
|         Naaaaame        |
+-------+-----------------+
|   1   |      col 2      |
|       |         c2      |
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

## Separator settings

| Separator              | Description                                |
|------------------------|--------------------------------------------|
| `sep=True`             | All horizontal dividers included           |
| `sep=False`            | All horizontal dividers are disabled       |
| `sep=(1,)`             | Only first delimiter                       |
| `sep=(1, 3, 5)`        | Only first third and fifth separator       |
| `sep=range(1, 100, 5)` | Delimiter every five lines first 100 lines |

<details>
<summary>Example</summary>

```pycon
>>> table_1 = [("qwe", "rty\nuio"), ("123456\n\n789000", "example")]
>>> kwargs = {
...     "max_width": (3, 4),
...     "max_height": 4,
... }
>>> print_table(table_1, **kwargs, sep=True)
+-----+------+
| qwe | rty  |
|     | uio  |
+-----+------+
| 123↩| exam↩|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> print_table(table_1, **kwargs, sep=False)
+-----+------+
| qwe | rty  |
|     | uio  |
| 123↩| exam↩|
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

## Borders

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
>>> from table2string import Themes
>>> table_1 = [("1", "2", "3"), ("qwe", "rty\nuio", "")]
>>> name_1 = "Table Name"
>>> print_table(table_1, theme=Themes.ascii_thin)
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, theme=Themes.ascii_thin, name=name_1)
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, theme=Themes.ascii_thin_double)
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, theme=Themes.ascii_thin_double, name=name_1)
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table(table_1, theme=Themes.ascii_double)
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, theme=Themes.ascii_double, name=name_1)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, theme=Themes.ascii_double_thin)
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, theme=Themes.ascii_double_thin, name=name_1)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> print_table(table_1, theme=Themes.ascii_booktabs)
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
>>> print_table(table_1, theme=Themes.ascii_booktabs, name=name_1)
 --------------- 
   Table Name    
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
>>> print_table(table_1, theme=Themes.thin)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.thin, name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.thin_thick)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.thin_thick, name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.thin_double)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.thin_double, name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.rounded)
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, theme=Themes.rounded, name=name_1)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, theme=Themes.rounded_thick)
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, theme=Themes.rounded_thick, name=name_1)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, theme=Themes.rounded_double)
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, theme=Themes.rounded_double, name=name_1)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> print_table(table_1, theme=Themes.thick)
┏━━━━━┳━━━━━┳━━━┓
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> print_table(table_1, theme=Themes.thick, name=name_1)
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> print_table(table_1, theme=Themes.thick_thin)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┠━━━━━╂━━━━━╂━━━┨
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.thick_thin, name=name_1)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┠━━━━━╂━━━━━╂━━━┨
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> print_table(table_1, theme=Themes.double)
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, theme=Themes.double, name=name_1)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, theme=Themes.double_thin)
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, theme=Themes.double_thin, name=name_1)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> print_table(table_1, theme=Themes.booktabs)
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
>>> print_table(table_1, theme=Themes.booktabs, name=name_1)
 ─────────────── 
   Table Name    
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
>>> print_table(table_1, theme=Themes.markdown)
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |
>>> print_table(table_1, theme=Themes.markdown, name=name_1)
|  Table Name   |
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |

```

</details>

## Emojis

<details>
<summary>Example</summary>

```python
from prettytable import PrettyTable
from table2string import Table

names = ("plain text", "emoji")
table = [
    (
        "text\ntext",
        "👨‍👩‍👧‍👦👨‍👩‍👦‍👦👨‍👩‍👧‍👧\n"
        "👨‍👨‍👧‍👦👨‍👨‍👧‍👧👨‍👩‍👧👩‍❤️‍👨\n"
        "👨‍❤️‍👨👯👩‍🦼👭👨‍👩‍👧‍👦\n"
        "👨‍👨‍👧‍👦👨‍👨‍👦👩‍👩‍👧\n"
        "👨‍👨‍👧‍👧👨‍👩‍👦‍👦",
    ),
]
t = PrettyTable(title="prettytable", field_names=names, align="c")
t.add_rows(table)
print(t)

t = Table(table, name="table2string", column_names=names)
t.print(align="^", sep=(1,))
```

<details>
<summary>Windows Terminal</summary>

![emoji_example_1.png](images/emoji_example_Windows_Terminal.png)
</details>

<details>
<summary>Windows 10</summary>

![emoji_example_windows_10_terminal.png](images/emoji_example_windows_10_terminal.png)
</details>

<details>
<summary>Windows 11</summary>

![emoji_example_windows_11_terminal.png](images/emoji_example_windows_11_terminal.png)
</details>

<details>
<summary>VT100 terminal emulator</summary>

![emoji_example_VT100_terminal_emulator.png](images/emoji_example_VT100_terminal_emulator.png)
</details>
</details>
