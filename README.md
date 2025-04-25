# table2string

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/EgorKhabarov/table2string/tests.yml?style=flat&logo=GitHub&label=Tests)](https://github.com/EgorKhabarov/table2string/actions/workflows/tests.yml)
[![Publish Python Package to PyPI](https://img.shields.io/github/actions/workflow/status/EgorKhabarov/table2string/publish.yml?style=flat&logo=GitHub&label=Publish%20to%20PyPI)](https://github.com/EgorKhabarov/table2string/actions/workflows/publish.yml)
[![Code coverage Status](https://codecov.io/github/EgorKhabarov/table2string/branch/master/graph/badge.svg)](https://codecov.io/github/EgorKhabarov/table2string)

[![PyPi Package Version](https://img.shields.io/pypi/v/table2string.svg?style=flat&logo=pypi)](https://pypi.python.org/pypi/table2string)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/table2string.svg?style=flat&logo=pypi)](https://pypi.python.org/pypi/table2string)
[![PyPi status](https://img.shields.io/pypi/status/table2string.svg?style=flat&logo=pypi)](https://pypi.python.org/pypi/table2string)
[![PyPi downloads](https://img.shields.io/pypi/dm/table2string.svg?style=flat&logo=pypi)](https://pypi.org/project/table2string/)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy checked](https://img.shields.io/badge/mypy-checked-blue)](https://github.com/python/mypy)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


## Convert table to string

While there are several libraries available for converting tables to strings in Python, none seemed to meet my specific requirements.

- **Line Break Support**: Easily include line breaks within cells for enhanced readability.
- **Subtable Support**: Easily include a table within a table for a more flexible presentation.
- **Alignment**: Easily align text in a cell in any direction.
- **Emoji Integration**: Effortlessly incorporate emoji characters into your tables to add visual appeal and context.
- **[New!] ANSI Support**: Use escape sequences for colors, decorations, and hyperlinks.

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
>>> from table2string import Table, Themes, HorizontalAlignment, VerticalAlignment
>>> Table([("1", "2", "3"), ("qwe", "rty\nuio", "")], name="Table Name", column_names=("c1", "c2", "c3")).print()
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
>>> from io import StringIO
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
>>> import sqlite3
>>> cursor = sqlite3.connect(":memory:").cursor().execute(
...     "CREATE TABLE data (c1 TEXT, c2 TEXT, c3 TEXT);"
... ).executemany(
...     "INSERT INTO data (c1, c2, c3) VALUES (?, ?, ?);",
...     [("1", "2", "3"), ("qwe", "rty\nuio", "")],
... ).execute(
...     "SELECT c1, c2, c3 FROM data;"
... )
>>> Table.from_db_cursor(
...     cursor,
...     name="Table Name",
...     column_names=True,
... ).print()
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
>>> Table(
...     [("c1", Table([("1", "2"), ("3", "4")], name="SubTable"))],
...     name="Table Name",
... ).print(v_align=("-",), max_width=(2, 8))
+---------------+
|  Table Name   |
+----+----------+
|    | SubTable |
|    +-----+----+
| c1 |   1 |  2 |
|    +-----+----+
|    |   3 |  4 |
+----+-----+----+

```

## Arguments

| Argument                 | Type                                                                                               | Example                         | Description                                                                                                                                                 |
|:-------------------------|:---------------------------------------------------------------------------------------------------|:--------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `table`                  | `Sequence[Sequence[Any]]`                                                                          | `[("1", "2"), ("3", "4")]`      | A two-dimensional matrix                                                                                                                                    |
| `h_align`                | <code>tuple\[HorizontalAlignment &#x7c; str, ...]</code> &#x7c; `HorizontalAlignment` &#x7c; `str` | `HorizontalAlignment.CENTER`    | Allows you to align text in a cell horizontally                                                                                                             |
| `v_align`                | <code>tuple\[VerticalAlignment &#x7c; str, ...]</code> &#x7c; `VerticalAlignment` &#x7c; `str`     | `VerticalAlignment.MIDDLE`      | Allows you to align text in a cell vertically                                                                                                               |
| `text_spliter`           | `BaseTextSplitter` &#x7c; `tuple[BaseTextSplitter, ...]`                                           | `AnsiTextSplitter()`            | Allows you to customize text formatting, for example, ANSI or HTML                                                                                          |
| `name`                   | `str` &#x7c; `None`                                                                                | `"Table Name"`                  | Table name                                                                                                                                                  |
| `name_h_align`           | `HorizontalAlignment` &#x7c; `str`                                                                 | `HorizontalAlignment.CENTER`    | Allows you to align table name horizontally                                                                                                                 |
| `name_v_align`           | `VerticalAlignment` &#x7c; `str`                                                                   | `VerticalAlignment.MIDDLE`      | Allows you to align table name vertically                                                                                                                   |
| `name_spliter`           | `BaseTextSplitter`                                                                                 | `AnsiTextSplitter()`            | Allows you to customize name formatting, for example, ANSI or HTML                                                                                          |
| `column_names`           | `Sequence[str]` &#x7c; `None`                                                                      | `("c1", "c2", ...column_count)` | Sets the names for the table columns                                                                                                                        |
| `column_names_h_align`   | <code>tuple\[HorizontalAlignment &#x7c; str, ...]</code> &#x7c; `HorizontalAlignment` &#x7c; `str` | `HorizontalAlignment.CENTER`    | Allows you to align column names horizontally                                                                                                               |
| `column_names_v_align`   | <code>tuple\[VerticalAlignment &#x7c; str, ...]</code> &#x7c; `VerticalAlignment` &#x7c; `str`     | `VerticalAlignment.MIDDLE`      | Allows you to align column names vertically                                                                                                                 |
| `column_names_spliter`   | `BaseTextSplitter` &#x7c; `tuple[BaseTextSplitter, ...]`                                           | `AnsiTextSplitter()`            | Allows you to customize column names formatting, for example, ANSI or HTML                                                                                  |
| `max_width`              | `int` &#x7c; `Tuple[int, ...]` &#x7c; `None`                                                       | `120`                           | Allows you to set the width of the entire table or individually for each column                                                                             |
| `max_height`             | `int` &#x7c; `None`                                                                                | `10`                            | Specifies the maximum height for rows                                                                                                                       |
| `maximize_height`        | `bool`                                                                                             | `True`                          | Force height to be taken from max_height                                                                                                                    |
| `line_break_symbol`      | `str`                                                                                              | `"\\"`                          | Line break symbol                                                                                                                                           |
| `cell_break_symbol`      | `str`                                                                                              | `"…"`                           | Symbol indicating the end of text when there is not enough height                                                                                           |
| `sep`                    | `bool` &#x7c; `range` &#x7c; `tuple`                                                               | `(1, 3, 6)`                     | Handles the separators between table rows and can be either a boolean type or possess a `__contains__` method                                               |
| `end`                    | `str` &#x7c; `None`                                                                                | `"\n"`                          | Behaves the same as `print(end=)`                                                                                                                           |
| `file`                   | `TextIOWrapper` &#x7c; `None`                                                                      | `sys.stdout` or `io.StringIO()` | Behaves the same as `print(file=)`                                                                                                                          |
| `theme`                  | `Theme`                                                                                            | `Themes.rounded_thick`          | Allows you to set a specific theme for the table. For example, the border style                                                                             |
| `ignore_width_errors`    | `bool`                                                                                             | `False`                         | Fixes errors in max_width if they exist                                                                                                                     |
| `proportion_coefficient` | `float`                                                                                            | `0.5`                           | Affects the width distribution of the columns. A value of `0.0` corresponds to proportional distribution, `1.0` averages the values, and `2.0` inverts them |

## Text alignment

| Align                                     | Example           | Description                                                                                                                    |
|:------------------------------------------|:------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| `"<align>"` or `("<align>",)`             | `"^"` or `("^",)` | Setting `align` (`"^"`) for all columns                                                                                        |
| `("<align_1>", "<align_2>")`              | `("^", "<")`      | Setting `align_1` (`"^"`) for the first column and `align_2` (`"<"`) for all other columns                                     |
| `("<align_1>", "<align_2>", "<align_3>")` | `("^", "<", ">")` | Setting `align_1` (`"^"`) for the first column and `align_2` (`"<"`) for the second and `align_3` (`">"`) for the third column |

You can also use the corresponding `HorizontalAlignment` or `VerticalAlignment` type

For `name_h_align` and `name_v_align` only the `str` type or the corresponding `HorizontalAlignment` or `VerticalAlignment` type is valid

### HorizontalAlignment

| Align                                      | Description                                                                                                                                          |
|:-------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `AUTO` or `AUTO_AUTO` or `*` or `**`       | Alignment depends on the type. If this is a number and there are no line breaks in this cell, then align to the right; otherwise, align to the left. |
| `LEFT` or `LEFT_LEFT` or `<` or `<<`       | All lines are left aligned                                                                                                                           |
| `CENTER` or `CENTER_CENTER` or `^` or `^^` | All lines are center aligned                                                                                                                         |
| `RIGHT` or `RIGHT_RIGHT` or `>` or `>>`    | All lines are right aligned                                                                                                                          |
| `LEFT_CENTER` or `<^`                      | The first line is left aligned and the remaining lines are centered                                                                                  |
| `LEFT_RIGHT` or `<>`                       | The first line is left aligned and the remaining lines are right aligned                                                                             |
| `CENTER_LEFT` or `^<`                      | The first line is aligned to the center, and the remaining lines are aligned to the left of the first line.                                          |
| `CENTER_RIGHT` or `^>`                     | The first line is aligned to the center, and the remaining lines are aligned to the right of the first line.                                         |
| `RIGHT_LEFT` or `><`                       | The first line is right aligned and the remaining lines are left aligned                                                                             |
| `RIGHT_CENTER` or `>^`                     | The first line is right aligned and the remaining lines are centered                                                                                 |

### VerticalAlignment

| Align           | Description             |
|:----------------|:------------------------|
| `TOP` or `^`    | Text are top aligned    |
| `MIDDLE` or `-` | Text are centered       |
| `BOTTOM` or `_` | Text are bottom aligned |


<details>
<summary>Example</summary>

```pycon
>>> from functools import partial
>>> sub_table_auto_func = partial(Table, [("123", "text",)], max_height=4, maximize_height=True)
>>> sub_table_func = partial(Table, [("first line\ntext",)], max_height=4, maximize_height=True)
>>> Table(
...     [
...         *(
...             [v_align, sub_table_auto_func(h_align="*", v_align=v_align)] + [
...                 sub_table_func(h_align=h_align, v_align=v_align)
...                 for h_align in ("<", ">", "^", "^<", "^>")
...             ]
...             for v_align in ("^", "-", "_")
...         )
...     ],
...     column_names=(" ", "*", "<", ">", "^", "^<", "^>"),
... ).print(max_width=(1, len("first line")+4), v_align=("-",))
+---+----------------+----------------+----------------+----------------+----------------+----------------+
|   |       *        |       <        |       >        |       ^        |       ^<       |       ^>       |
+---+-------+--------+----------------+----------------+----------------+----------------+----------------+
|   |   123 | text   | first line     |     first line |   first line   |   first line   |   first line   |
| ^ |       |        | text           |           text |      text      |   text         |         text   |
|   |       |        |                |                |                |                |                |
|   |       |        |                |                |                |                |                |
+---+-------+--------+----------------+----------------+----------------+----------------+----------------+
|   |       |        |                |                |                |                |                |
| - |   123 | text   | first line     |     first line |   first line   |   first line   |   first line   |
|   |       |        | text           |           text |      text      |   text         |         text   |
|   |       |        |                |                |                |                |                |
+---+-------+--------+----------------+----------------+----------------+----------------+----------------+
|   |       |        |                |                |                |                |                |
| _ |       |        |                |                |                |                |                |
|   |       |        | first line     |     first line |   first line   |   first line   |   first line   |
|   |   123 | text   | text           |           text |      text      |   text         |         text   |
+---+-------+--------+----------------+----------------+----------------+----------------+----------------+

```
</details>

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
>>> Table([(1, 12345, "example")]).print(max_width=30)
+-----+----------+-----------+
|   1 |    12345 | example   |
+-----+----------+-----------+
>>> # Width of each column individually
>>> Table([(1, 12345, "example")]).print(max_width=(10,))
+------------+------------+------------+
|          1 |      12345 | example    |
+------------+------------+------------+
>>> Table([(1, 12345, "example")]).print(max_width=(1, 8, 6))
+---+----------+--------+
| 1 |    12345 | exampl/|
|   |          | e      |
+---+----------+--------+
>>> Table([(1, 12345, "example")]).print(max_width=(1, 5, 7))
+---+-------+---------+
| 1 | 12345 | example |
+---+-------+---------+
>>> Table([("123456\n\n789000", "example")]).print(max_width=(3, 4), max_height=4)
+-----+------+
| 123/| exam/|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> Table([("123456789",)]).print(max_width=(1,), max_height=1)
+---+
| 1…|
+---+
>>> Table([("123\n456\n789",)]).print(
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
>>> Table([("123456789",)]).print(
...     max_width=(3,),
...     max_height=4,
...     maximize_height=True,
... )
+-----+
| 123/|
| 456/|
| 789 |
|     |
+-----+

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
>>> table_1 = Table([("qwe", "rty\nuio"), ("123456\n\n789000", "example")])
>>> kwargs = {
...     "max_width": (3, 4),
...     "max_height": 4,
... }
>>> table_1.print(**kwargs, sep=True)
+-----+------+
| qwe | rty  |
|     | uio  |
+-----+------+
| 123/| exam/|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> table_1.print(**kwargs, sep=False)
+-----+------+
| qwe | rty  |
|     | uio  |
| 123/| exam/|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
>>> table_2 = Table([("1", "2"), ("3", "4")], name="Name")
>>> table_2.print(sep=True)
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
+---+---+
>>> table_2.print(sep=False)
+-------+
| Name  |
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
>>> table_3 = Table([("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")])
>>> table_3.print(sep=(1,))
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> table_3.print(sep=(2,))
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> table_3.print(sep=(1, 3))
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
+---+---+
| 7 | 8 |
+---+---+
>>> table_4 = Table([("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")], name="Name")
>>> table_4.print(sep=(1,))
+-------+
| Name  |
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> table_4.print(sep=(2,))
+-------+
| Name  |
+---+---+
| 1 | 2 |
| 3 | 4 |
+---+---+
| 5 | 6 |
| 7 | 8 |
+---+---+
>>> table_4.print(sep=(1, 3))
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

## Themes

### Borders

A variety of table border styles are available through the `Themes` interface:

- `Themes.ascii_thin`
- `Themes.ascii_thin_double`
- `Themes.ascii_double`
- `Themes.ascii_double_thin`
- `Themes.thin`
- `Themes.thin_thick`
- `Themes.thin_double`
- `Themes.rounded_double`
- `Themes.rounded`
- `Themes.rounded_thick`
- `Themes.thick`
- `Themes.thick_thin`
- `Themes.double`
- `Themes.double_thin`
- `Themes.booktabs`
- `Themes.ascii_booktabs`
- `Themes.markdown`

You can customize the border color using the `set_color` or `set_context_color` method of the border:
```pycon
>>> from table2string import Themes, Color, BgColor
>>> Themes.thin_thick.border.set_color(color=Color.CYAN)
>>> Themes.thin_thick.border.set_color(color=None)
>>> # You can also use a context manager to temporarily set the border color
>>> with Themes.thin_thick.border.set_context_color(color=Color.MAGENTA):
...     pass  # Render tables here

```

Expandable previews below this section illustrate the visual appearance of each border theme.

<details>
<summary>Border types</summary>

```pycon
>>> from table2string import Themes, HorizontalAlignment
>>> table = []
>>> example_table = Table([(" ", " "), (" ", " "), (" ", " ")])
>>> theme_names = (
...     ("ascii_thin", "ascii_thin_double"),
...     ("ascii_double", "ascii_double_thin"),
...     ("thin", "thin_thick"),
...     ("thin_double", "rounded_double"),
...     ("rounded", "rounded_thick"),
...     ("thick", "thick_thin"),
...     ("double", "double_thin"),
...     ("booktabs", "ascii_booktabs"),
...     ("markdown", "None"),
... )
>>> for names in theme_names:
...     table.append([])
...     for name in names:
...         string_table = example_table.stringify(
...             theme=getattr(Themes, name, Themes.ascii_thin)
...         )
...         table[-1].append(f"{name}\n{string_table}")
>>> Table(table).print(theme=Themes.thin, h_align=HorizontalAlignment.CENTER)
┌──────────────┬───────────────────┐
│  ascii_thin  │ ascii_thin_double │
│  +---+---+   │     +---+---+     │
│  |   |   |   │     |   |   |     │
│  +---+---+   │     +===+===+     │
│  |   |   |   │     |   |   |     │
│  +---+---+   │     +---+---+     │
│  |   |   |   │     |   |   |     │
│  +---+---+   │     +---+---+     │
├──────────────┼───────────────────┤
│ ascii_double │ ascii_double_thin │
│  +===+===+   │     +===+===+     │
│  ‖   ‖   ‖   │     ‖   ‖   ‖     │
│  +===+===+   │     +---+---+     │
│  ‖   ‖   ‖   │     ‖   ‖   ‖     │
│  +===+===+   │     +===+===+     │
│  ‖   ‖   ‖   │     ‖   ‖   ‖     │
│  +===+===+   │     +===+===+     │
├──────────────┼───────────────────┤
│     thin     │    thin_thick     │
│  ┌───┬───┐   │     ┌───┬───┐     │
│  │   │   │   │     │   │   │     │
│  ├───┼───┤   │     ┝━━━┿━━━┥     │
│  │   │   │   │     │   │   │     │
│  ├───┼───┤   │     ├───┼───┤     │
│  │   │   │   │     │   │   │     │
│  └───┴───┘   │     └───┴───┘     │
├──────────────┼───────────────────┤
│ thin_double  │  rounded_double   │
│  ┌───┬───┐   │     ╭───┬───╮     │
│  │   │   │   │     │   │   │     │
│  ╞═══╪═══╡   │     ╞═══╪═══╡     │
│  │   │   │   │     │   │   │     │
│  ├───┼───┤   │     ├───┼───┤     │
│  │   │   │   │     │   │   │     │
│  └───┴───┘   │     ╰───┴───╯     │
├──────────────┼───────────────────┤
│   rounded    │   rounded_thick   │
│  ╭───┬───╮   │     ╭───┬───╮     │
│  │   │   │   │     │   │   │     │
│  ├───┼───┤   │     ┝━━━┿━━━┥     │
│  │   │   │   │     │   │   │     │
│  ├───┼───┤   │     ├───┼───┤     │
│  │   │   │   │     │   │   │     │
│  ╰───┴───╯   │     ╰───┴───╯     │
├──────────────┼───────────────────┤
│    thick     │    thick_thin     │
│  ┏━━━┳━━━┓   │     ┏━━━┳━━━┓     │
│  ┃   ┃   ┃   │     ┃   ┃   ┃     │
│  ┣━━━╋━━━┫   │     ┠───╂───┨     │
│  ┃   ┃   ┃   │     ┃   ┃   ┃     │
│  ┣━━━╋━━━┫   │     ┣━━━╋━━━┫     │
│  ┃   ┃   ┃   │     ┃   ┃   ┃     │
│  ┗━━━┻━━━┛   │     ┗━━━┻━━━┛     │
├──────────────┼───────────────────┤
│    double    │    double_thin    │
│  ╔═══╦═══╗   │     ╔═══╦═══╗     │
│  ║   ║   ║   │     ║   ║   ║     │
│  ╠═══╬═══╣   │     ╟───╫───╢     │
│  ║   ║   ║   │     ║   ║   ║     │
│  ╠═══╬═══╣   │     ╠═══╬═══╣     │
│  ║   ║   ║   │     ║   ║   ║     │
│  ╚═══╩═══╝   │     ╚═══╩═══╝     │
├──────────────┼───────────────────┤
│   booktabs   │  ascii_booktabs   │
│   ───────    │      -------      │
│              │                   │
│   ━━━━━━━    │      =======      │
│              │                   │
│   ───────    │      -------      │
│              │                   │
│   ───────    │      -------      │
├──────────────┼───────────────────┤
│   markdown   │       None        │
│  |   |   |   │     +---+---+     │
│  |---|---|   │     |   |   |     │
│  |   |   |   │     +---+---+     │
│  |   |   |   │     |   |   |     │
│              │     +---+---+     │
│              │     |   |   |     │
│              │     +---+---+     │
└──────────────┴───────────────────┘

```
</details>

<details>
<summary>Example</summary>

```pycon
>>> from table2string import Table, Themes
>>> name = "Table Name"
>>> column_names = ("c1", "c2", "3")
>>> table = [("1", "2", "3"), ("qwe", "rty\nuio", "")]
>>> t = Table(table)
>>> t_name = Table(table, name=name)
>>> t_column_names = Table(table, column_names=column_names)
>>> t_name_column_names = Table(table, name=name, column_names=column_names)

```

<details>
<summary>Themes.ascii_thin</summary>

```pycon

>>> t.print(theme=Themes.ascii_thin)
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> t_column_names.print(theme=Themes.ascii_thin)
+-----+-----+---+
| c1  | c2  | 3 |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> t_name.print(theme=Themes.ascii_thin)
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> t_name_column_names.print(theme=Themes.ascii_thin)
+---------------+
|  Table Name   |
+-----+-----+---+
| c1  | c2  | 3 |
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+

```
</details>


<details>
<summary>Themes.ascii_thin_double</summary>

```pycon
>>> t.print(theme=Themes.ascii_thin_double)
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> t_column_names.print(theme=Themes.ascii_thin_double)
+-----+-----+---+
| c1  | c2  | 3 |
+=====+=====+===+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> t_name.print(theme=Themes.ascii_thin_double)
+---------------+
|  Table Name   |
+-----+-----+---+
|   1 |   2 | 3 |
+=====+=====+===+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> t_name_column_names.print(theme=Themes.ascii_thin_double)
+---------------+
|  Table Name   |
+-----+-----+---+
| c1  | c2  | 3 |
+=====+=====+===+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+

```
</details>


<details>
<summary>Themes.ascii_double</summary>

```pycon
>>> t.print(theme=Themes.ascii_double)
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> t_column_names.print(theme=Themes.ascii_double)
+=====+=====+===+
‖ c1  ‖ c2  ‖ 3 ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> t_name.print(theme=Themes.ascii_double)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> t_name_column_names.print(theme=Themes.ascii_double)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖ c1  ‖ c2  ‖ 3 ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+

```
</details>


<details>
<summary>Themes.ascii_double_thin</summary>

```pycon
>>> t.print(theme=Themes.ascii_double_thin)
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> t_column_names.print(theme=Themes.ascii_double_thin)
+=====+=====+===+
‖ c1  ‖ c2  ‖ 3 ‖
+-----+-----+---+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> t_name.print(theme=Themes.ascii_double_thin)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖   1 ‖   2 ‖ 3 ‖
+-----+-----+---+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+
>>> t_name_column_names.print(theme=Themes.ascii_double_thin)
+===============+
‖  Table Name   ‖
+=====+=====+===+
‖ c1  ‖ c2  ‖ 3 ‖
+-----+-----+---+
‖   1 ‖   2 ‖ 3 ‖
+=====+=====+===+
‖ qwe ‖ rty ‖   ‖
‖     ‖ uio ‖   ‖
+=====+=====+===+

```
</details>


<details>
<summary>Themes.ascii_booktabs</summary>

```pycon
>>> t.print(theme=Themes.ascii_booktabs)
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
>>> t_column_names.print(theme=Themes.ascii_booktabs)
 --------------- 
  c1    c2    3  
 =============== 
    1     2   3  
 --------------- 
  qwe   rty      
        uio      
 --------------- 
>>> t_name.print(theme=Themes.ascii_booktabs)
 --------------- 
   Table Name    
 --------------- 
    1     2   3  
 =============== 
  qwe   rty      
        uio      
 --------------- 
>>> t_name_column_names.print(theme=Themes.ascii_booktabs)
 --------------- 
   Table Name    
 --------------- 
  c1    c2    3  
 =============== 
    1     2   3  
 --------------- 
  qwe   rty      
        uio      
 --------------- 

```
</details>


<details>
<summary>Themes.thin</summary>

```pycon
>>> t.print(theme=Themes.thin)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_column_names.print(theme=Themes.thin)
┌─────┬─────┬───┐
│ c1  │ c2  │ 3 │
├─────┼─────┼───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_name.print(theme=Themes.thin)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_name_column_names.print(theme=Themes.thin)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│ c1  │ c2  │ 3 │
├─────┼─────┼───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘

```
</details>


<details>
<summary>Themes.thin_thick</summary>

```pycon
>>> t.print(theme=Themes.thin_thick)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_column_names.print(theme=Themes.thin_thick)
┌─────┬─────┬───┐
│ c1  │ c2  │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_name.print(theme=Themes.thin_thick)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_name_column_names.print(theme=Themes.thin_thick)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│ c1  │ c2  │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘

```
</details>


<details>
<summary>Themes.thin_double</summary>

```pycon
>>> t.print(theme=Themes.thin_double)
┌─────┬─────┬───┐
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_column_names.print(theme=Themes.thin_double)
┌─────┬─────┬───┐
│ c1  │ c2  │ 3 │
╞═════╪═════╪═══╡
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_name.print(theme=Themes.thin_double)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘
>>> t_name_column_names.print(theme=Themes.thin_double)
┌───────────────┐
│  Table Name   │
├─────┬─────┬───┤
│ c1  │ c2  │ 3 │
╞═════╪═════╪═══╡
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
└─────┴─────┴───┘

```
</details>


<details>
<summary>Themes.rounded</summary>

```pycon
>>> t.print(theme=Themes.rounded)
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_column_names.print(theme=Themes.rounded)
╭─────┬─────┬───╮
│ c1  │ c2  │ 3 │
├─────┼─────┼───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_name.print(theme=Themes.rounded)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_name_column_names.print(theme=Themes.rounded)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│ c1  │ c2  │ 3 │
├─────┼─────┼───┤
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯

```
</details>


<details>
<summary>Themes.rounded_thick</summary>

```pycon
>>> t.print(theme=Themes.rounded_thick)
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_column_names.print(theme=Themes.rounded_thick)
╭─────┬─────┬───╮
│ c1  │ c2  │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_name.print(theme=Themes.rounded_thick)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_name_column_names.print(theme=Themes.rounded_thick)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│ c1  │ c2  │ 3 │
┝━━━━━┿━━━━━┿━━━┥
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯

```
</details>


<details>
<summary>Themes.rounded_double</summary>

```pycon
>>> t.print(theme=Themes.rounded_double)
╭─────┬─────┬───╮
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_column_names.print(theme=Themes.rounded_double)
╭─────┬─────┬───╮
│ c1  │ c2  │ 3 │
╞═════╪═════╪═══╡
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_name.print(theme=Themes.rounded_double)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│   1 │   2 │ 3 │
╞═════╪═════╪═══╡
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯
>>> t_name_column_names.print(theme=Themes.rounded_double)
╭───────────────╮
│  Table Name   │
├─────┬─────┬───┤
│ c1  │ c2  │ 3 │
╞═════╪═════╪═══╡
│   1 │   2 │ 3 │
├─────┼─────┼───┤
│ qwe │ rty │   │
│     │ uio │   │
╰─────┴─────┴───╯

```
</details>


<details>
<summary>Themes.thick</summary>

```pycon
>>> t.print(theme=Themes.thick)
┏━━━━━┳━━━━━┳━━━┓
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> t_column_names.print(theme=Themes.thick)
┏━━━━━┳━━━━━┳━━━┓
┃ c1  ┃ c2  ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> t_name.print(theme=Themes.thick)
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> t_name_column_names.print(theme=Themes.thick)
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃ c1  ┃ c2  ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛

```
</details>


<details>
<summary>Themes.thick_thin</summary>

```pycon
>>> t.print(theme=Themes.thick_thin)
┏━━━━━┳━━━━━┳━━━┓
┃   1 ┃   2 ┃ 3 ┃
┠─────╂─────╂───┨
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> t_column_names.print(theme=Themes.thick_thin)
┏━━━━━┳━━━━━┳━━━┓
┃ c1  ┃ c2  ┃ 3 ┃
┠─────╂─────╂───┨
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> t_name.print(theme=Themes.thick_thin)
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃   1 ┃   2 ┃ 3 ┃
┠─────╂─────╂───┨
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛
>>> t_name_column_names.print(theme=Themes.thick_thin)
┏━━━━━━━━━━━━━━━┓
┃  Table Name   ┃
┣━━━━━┳━━━━━┳━━━┫
┃ c1  ┃ c2  ┃ 3 ┃
┠─────╂─────╂───┨
┃   1 ┃   2 ┃ 3 ┃
┣━━━━━╋━━━━━╋━━━┫
┃ qwe ┃ rty ┃   ┃
┃     ┃ uio ┃   ┃
┗━━━━━┻━━━━━┻━━━┛

```
</details>


<details>
<summary>Themes.double</summary>

```pycon
>>> t.print(theme=Themes.double)
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> t_column_names.print(theme=Themes.double)
╔═════╦═════╦═══╗
║ c1  ║ c2  ║ 3 ║
╠═════╬═════╬═══╣
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> t_name.print(theme=Themes.double)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> t_name_column_names.print(theme=Themes.double)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║ c1  ║ c2  ║ 3 ║
╠═════╬═════╬═══╣
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝

```
</details>


<details>
<summary>Themes.double_thin</summary>

```pycon
>>> t.print(theme=Themes.double_thin)
╔═════╦═════╦═══╗
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> t_column_names.print(theme=Themes.double_thin)
╔═════╦═════╦═══╗
║ c1  ║ c2  ║ 3 ║
╟─────╫─────╫───╢
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> t_name.print(theme=Themes.double_thin)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║   1 ║   2 ║ 3 ║
╟─────╫─────╫───╢
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝
>>> t_name_column_names.print(theme=Themes.double_thin)
╔═══════════════╗
║  Table Name   ║
╠═════╦═════╦═══╣
║ c1  ║ c2  ║ 3 ║
╟─────╫─────╫───╢
║   1 ║   2 ║ 3 ║
╠═════╬═════╬═══╣
║ qwe ║ rty ║   ║
║     ║ uio ║   ║
╚═════╩═════╩═══╝

```
</details>


<details>
<summary>Themes.booktabs</summary>

```pycon
>>> t.print(theme=Themes.booktabs)
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
>>> t_column_names.print(theme=Themes.booktabs)
 ─────────────── 
  c1    c2    3  
 ━━━━━━━━━━━━━━━ 
    1     2   3  
 ─────────────── 
  qwe   rty      
        uio      
 ─────────────── 
>>> t_name.print(theme=Themes.booktabs)
 ─────────────── 
   Table Name    
 ─────────────── 
    1     2   3  
 ━━━━━━━━━━━━━━━ 
  qwe   rty      
        uio      
 ─────────────── 
>>> t_name_column_names.print(theme=Themes.booktabs)
 ─────────────── 
   Table Name    
 ─────────────── 
  c1    c2    3  
 ━━━━━━━━━━━━━━━ 
    1     2   3  
 ─────────────── 
  qwe   rty      
        uio      
 ─────────────── 

```
</details>


<details>
<summary>Themes.markdown</summary>

```pycon
>>> t.print(theme=Themes.markdown)
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |
>>> t_column_names.print(theme=Themes.markdown)
| c1  | c2  | 3 |
|-----|-----|---|
|   1 |   2 | 3 |
| qwe | rty |   |
|     | uio |   |
>>> t_name.print(theme=Themes.markdown)
|  Table Name   |
|   1 |   2 | 3 |
|-----|-----|---|
| qwe | rty |   |
|     | uio |   |
>>> t_name_column_names.print(theme=Themes.markdown)
|  Table Name   |
| c1  | c2  | 3 |
|-----|-----|---|
|   1 |   2 | 3 |
| qwe | rty |   |
|     | uio |   |

```
</details>
</details>

### Create your own theme

You can define a completely custom theme:

```pycon
>>> from table2string import Theme, Border
>>> new_theme = Theme(  # doctest: +SKIP
...     name="your_new_theme_name",
...     border=Border(
...         horizontal="-",
...         vertical="|",
...         top_left="+",
...         top_right="+",
...         # other characters
...     ),
...     # Theme to be used for nested tables to ensure proper border merging
...     # Defaults to the parent table's theme
...     custom_sub_table_theme=None,
... )

```

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
t = PrettyTable(title="prettytable", field_names=names, h_align="c")
t.add_rows(table)  # type: ignore
print(t)

t = Table(table, name="table2string", column_names=names)
t.print(h_align="^", sep=(1,))
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

## Subtable

To elegantly display structured data inside table cells, you can embed **subtables**.
These subtables are rendered as full tables within a cell and will seamlessly merge borders with the parent table.
Since a subtable is itself a `Table` instance, **you can nest them recursively** without limit.
Subtables will automatically scale to fit the width of their parent cell.

<details>
<summary>Example</summary>

```pycon
>>> Table(
...     [
...         ("1",),
...         (Table([("2", "3")]),),
...     ]
... ).print()
+-------+
|     1 |
+---+---+
| 2 | 3 |
+---+---+
>>> Table([(
...     Table([(
...         Table([(
...             Table([(
...                 Table([(
...                     Table([(
...                         Table([(
...                             Table(
...                                 [
...                                     ("1",),
...                                     (Table([("2", "3")]),),
...                                 ]
...                             ),
...                         )]),
...                     )]),
...                 )]),
...             )]),
...         )]),
...     )]),
... )]).print()
+-------+
|     1 |
+---+---+
| 2 | 3 |
+---+---+
>>> Table(
...     [
...         (
...             "123",
...             Table(
...                 [
...                     ("456",),
...                     (Table([("789", "101")]),),
...                 ]
...             ),
...         ),
...     ]
... ).print()
+-----+-----------+
| 123 |       456 |
|     +-----+-----+
|     | 789 | 101 |
+-----+-----+-----+

```
</details>

## [New!] Formatting

Formatting is handled by classes from the `text_splitters` module.
All classes inherit from one another in a cascading fashion and ultimately extend `BaseTextSplitter`.

- `BaseTextSplitter` (default in the `stringify` method) – The base class. It provides the `split_text` method, which splits text by width and height to fit it into a cell.
- `AnsiTextSplitterUnsafe` – Inherits from `BaseTextSplitter` and wraps its `split_text` method.
  It wraps ANSI sequences and hyperlinks so they remain functional even when the text is wrapped.
- `AnsiTextSplitter` (default in the `print` method) – Inherits from `AnsiTextSplitterUnsafe` and escapes unsafe sequences (everything except color and hyperlinks).
- `HtmlTextSplitter` – Inherits from `AnsiTextSplitter` and converts specific HTML tags into ANSI sequences.

You can separately configure splitters for the table name and column headers.
It is also possible to set a splitter for the entire table, or for each column individually.

- `name_spliter` – Splitter for the table name. Can be an instance of any `BaseTextSplitter` subclass.
- `column_names_spliter` – Splitter for column names. Can be an instance of a `BaseTextSplitter` subclass, or a `tuple` of instances corresponding to the number of columns.
- `text_spliter` – Splitter for table content. Can be an instance of a `BaseTextSplitter` subclass, or a `tuple` of instances, one for each column.

If the `tuple` has fewer elements than there are columns, the last element of the `tuple` will be used for all remaining columns.

For convenient ANSI formatting, you can use the `text_styles` module.
It provides:
- **Enum** `Color` — predefined foreground colors
- **Enum** `BgColor` — predefined background colors
- **Function** `style(text: str, *, fg: Color | tuple[int, int, int] | None = None, bg: BgColor | tuple[int, int, int] | None = None, **attrs) -> str` — wrap your text in the specified ANSI color/style codes
- **Function** `link(url: str, text: str) -> str` — create an OSC hyperlink around your text

You may also freely use the third-party **Colorama** library for colorizing table input.

> [!IMPORTANT]
> `table2string` does **not** automatically enable ANSI support on the Windows console.
> To turn it on, call `just_fix_windows_console()` from the Colorama package before printing.

### HtmlTextSplitter

You can use HTML formatting inside table cells.
Currently, the following tags are supported: `b`, `i`, `u`, `s`, `span`, `mark`, and `a`.
All other HTML tags will be ignored, but their inner text will still be preserved.

Each tag may include the following attributes:
- `style` — supports `color` and `background-color` in **RGB** or **HEX** formats only
- `class` — can be mapped to ANSI styles via a class-to-color mapping
- `href` — available in `<a>` tags for generating hyperlinks

```pycon
>>> from table2string import Table, HtmlTextSplitter, Color, BgColor
>>> splitter = HtmlTextSplitter(
...     html_classes={"red": Color.RED, "bg-red": BgColor.RED},
... )
>>> Table([(
...     """
... text
... <span class="red">red text<span style="color:#000" class="bg-red">black & bg red text</span></span>
... """,
... )]).print(text_spliter=splitter)
+-----------------------------+
| text                        |
| [31mred text[41m[38;2;0;0;0mblack & bg red text[0m |
+-----------------------------+

```

This allows you to use familiar HTML/CSS markup for styling text while maintaining full support for ANSI rendering.

### Create your own formatting

You can create your own **custom splitter formatter** (e.g. for Markdown or other markup languages)
by subclassing `AnsiTextSplitter` or `BaseTextSplitter` and overriding the `split_text` and `clear_formatting` methods.

- `split_text` – Called for each cell. Should split the text so it fits within the cell.
- `clear_formatting` – Called when calculating the width of a cell.

This method should remove all formatting, leaving only visible characters and ANSI sequences.
For example, with HTML formatting, it should strip all tags and leave only the visible text.

```pycon
>>> from table2string import style, Color
>>> from table2string import BaseTextSplitter, HtmlTextSplitter, AnsiTextSplitter
>>> # Same as Table([("q\x1b[31mwe\nr\x1b[0mty",)]).print()
>>> red_text = style("we\nr", fg=Color.RED)
>>> Table([(f"q{red_text}ty",)]).print()  # AnsiTextSplitter by default
+-----+
| q[31mwe[0m |
| [31mr[0mty |
+-----+
>>> Table(
...     [
...         (
...             '<b style="color:rgb(255,170,0)">Bold Gold '
...             '<i style="color:#fff">Bold & Italic White</i></b> '
...             '<u>Underline</u> '
...             '<a href="example.com"><s style="color:#55FF55">Strikethrough Green Link</s></a>',
...         ),
...     ],
... ).print(
...     max_width=25,
...     theme=Themes.thin,
...     text_spliter=HtmlTextSplitter(),
... )
┌───────────────────────┐
│ [1m[38;2;255;170;0mBold Gold [3m[38;2;255;255;255mBold & Ital[0m/│
│ [1m[38;2;255;170;0m[3m[38;2;255;255;255mic White[0m [4mUnderline[0m ]8;;https://example.com\[9m[38;2;85;255;85mSt]8;;\[0m/│
│ [9m[38;2;85;255;85m]8;;https://example.com\rikethrough Green Lin]8;;\[0m/│
│ [9m[38;2;85;255;85m]8;;https://example.com\k]8;;\[0m                     │
└───────────────────────┘
>>> Table(
...     [
...         (
...             "t\x1b[31mex\x1b[0mt",
...             "plain text",
...             "123<b>456</b>789",
...         ),
...     ],
...     name='<span style="color:#f00">Table</span>',
...     column_names=(
...         "qwoef<b>qd&lt;f</b> qld",
...         "1oijf\x1b[32m1iofj\x1b[0m1woejf",
...         "w1\x1b[32m23",
...     ),
... ).print(
...     name_spliter=HtmlTextSplitter(),
...     column_names_spliter=(
...         HtmlTextSplitter(),
...         AnsiTextSplitter(),  # AnsiTextSplitter for all remaining columns
...     ),
...     text_spliter=(
...         AnsiTextSplitter(),
...         BaseTextSplitter(),
...         HtmlTextSplitter(),
...     ),
... )
+----------------------------------------------+
|                    [38;2;255;0;0mTable[0m                     |
+---------------+------------------+-----------+
| qwoef[1mqd<f[0m qld | 1oijf[32m1iofj[0m1woejf |   w1[32m23[0m    |
+---------------+------------------+-----------+
| t[31mex[0mt          | plain text       | 123[1m456[0m789 |
+---------------+------------------+-----------+

```
