# table2string

[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/EgorKhabarov/table2string/tests.yml?style=flat&logo=GitHub&label=Tests)](https://github.com/EgorKhabarov/table2string/actions/workflows/tests.yml)

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
>>> print(stringify_table([("example",)]), end="")
+---------+
| example |
+---------+

```

## Custom width and height settings

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

```

## Text alignment

```pycon
>>> print_table([("1", "example")], max_width=25, name="Table Name", align="<", name_align="<")
+-----------------------+
| Table Name            |
+-----------+-----------+
| 1         | example   |
+-----------+-----------+
>>> print_table([("1", "example")], max_width=25, name="Table Name", align=">", name_align=">")
+-----------------------+
|            Table Name |
+-----------+-----------+
|         1 |   example |
+-----------+-----------+
>>> print_table([("1", "example")], max_width=25, name="Table Name", align="^", name_align="^")
+-----------------------+
|      Table Name       |
+-----------+-----------+
|     1     |  example  |
+-----------+-----------+
>>> print_table([("1", "example")], max_width=25, name="Table Name", align="*", name_align="*")
+-----------------------+
| Table Name            |
+-----------+-----------+
|         1 | example   |
+-----------+-----------+
>>> print_table([("1", "example")], max_width=25, name="Table Name")
+-----------------------+
|      Table Name       |
+-----------+-----------+
|         1 | example   |
+-----------+-----------+

```

```pycon
>>> table_1 = [("qwe", "rty\nuio"), ("123456\n\n789000", "example")]
>>> kwargs = {
...     "max_width": (3, 4),
...     "max_height": 4,
...     "line_break_symbol": "\\",
...     "cell_break_symbol": "/",
... }
>>> print_table(table_1, **kwargs, sep=True)
+-----+------+
| qwe | rty  |
|     | uio  |
+-----+------+
| 123\| exam\|
| 456 | ple  |
|     |      |
| 789/|      |
+-----+------+
>>> print_table(table_1, **kwargs, sep=False)
+-----+------+
| qwe | rty  |
|     | uio  |
| 123\| exam\|
| 456 | ple  |
|     |      |
| 789/|      |
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
