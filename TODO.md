# TODO

## v_align

Setting up vertical alignment
```pycon
>>> from table2string import Table, Themes
>>> table = [
...     ("11111", "22222"),
...     ("33333", "44444"),
... ]
>>> kwargs = {
...     "align": "^",
...     "theme": Themes.thin,
...     "max_width": (9,),
...     "max_height": 3,
...     "maximize_height": True,
... }
>>> Table(table).print(**kwargs)
┌───────────┬───────────┐
│   11111   │   22222   │
│           │           │
│           │           │
├───────────┼───────────┤
│   33333   │   44444   │
│           │           │
│           │           │
└───────────┴───────────┘
>>> # v_align in ("^", "-", "_")
>>> Table(table).print(**kwargs, v_align="-")  # doctest: +SKIP
┌───────────┬───────────┐
│           │           │
│   11111   │   22222   │
│           │           │
├───────────┼───────────┤
│           │           │
│   33333   │   44444   │
│           │           │
└───────────┴───────────┘

```
