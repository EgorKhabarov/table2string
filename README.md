# table2string

[![Tests](https://github.com/EgorKhabarov/table2string/actions/workflows/tests.yml/badge.svg)](https://github.com/EgorKhabarov/table2string/actions/workflows/tests.yml)
[![PyPi Package Version](https://img.shields.io/pypi/v/table2string.svg)](https://pypi.python.org/pypi/table2string)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/table2string.svg)](https://pypi.python.org/pypi/table2string)
[![PyPi status](https://img.shields.io/pypi/status/table2string.svg?style=flat-square)](https://pypi.python.org/pypi/table2string)

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
>>> from io import StringIO
>>> from table2string import print_table
>>> print_table([("1", "2", "3"), ("qwe", "rty\nuio", "")])
+-----+-----+---+
|   1 |   2 | 3 |
+-----+-----+---+
| qwe | rty |   |
|     | uio |   |
+-----+-----+---+
>>> print_table([("123456\n\n789000", "example")], max_width=(3, 4), max_height=4)
+-----+------+
| 123↩| exam↩|
| 456 | ple  |
|     |      |
| 789…|      |
+-----+------+
```
