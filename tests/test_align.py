from table2string import Table


def test_v_align():
    table = Table(
        [
            ("text",),
        ]
    )
    kwargs1 = {
        "max_width": 30,
        "max_height": 6,
        "maximize_height": True,
    }
    kwargs2 = {
        "max_width": 30,
        "max_height": 7,
        "maximize_height": True,
    }
    assert (
        table.stringify(**kwargs1)
        == table.stringify(**kwargs1, v_align="^")
        == """
+----------------------------+
| text                       |
|                            |
|                            |
|                            |
|                            |
|                            |
+----------------------------+
""".strip()
    )
    assert (
        table.stringify(**kwargs2)
        == table.stringify(**kwargs2, v_align="^")
        == """
+----------------------------+
| text                       |
|                            |
|                            |
|                            |
|                            |
|                            |
|                            |
+----------------------------+
""".strip()
    )
    assert (
        table.stringify(**kwargs1, v_align="-")
        == """
+----------------------------+
|                            |
|                            |
| text                       |
|                            |
|                            |
|                            |
+----------------------------+
""".strip()
    )
    assert (
        table.stringify(**kwargs2, v_align="-")
        == """
+----------------------------+
|                            |
|                            |
|                            |
| text                       |
|                            |
|                            |
|                            |
+----------------------------+
""".strip()
    )
    assert (
        table.stringify(**kwargs1, v_align="_")
        == """
+----------------------------+
|                            |
|                            |
|                            |
|                            |
|                            |
| text                       |
+----------------------------+
""".strip()
    )
    assert (
        table.stringify(**kwargs2, v_align="_")
        == """
+----------------------------+
|                            |
|                            |
|                            |
|                            |
|                            |
|                            |
| text                       |
+----------------------------+
""".strip()
    )


def test_align_together():
    table = Table(
        [
            (
                "text\nex",
                "ex\ntext",
            ),
        ]
    )
    assert (
        table.stringify(
            h_align="^",
            v_align="^",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|    text    |     ex     |
|     ex     |    text    |
|            |            |
|            |            |
|            |            |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align="^",
            v_align="-",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|            |            |
|    text    |     ex     |
|     ex     |    text    |
|            |            |
|            |            |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align="^",
            v_align="_",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|            |            |
|            |            |
|            |            |
|    text    |     ex     |
|     ex     |    text    |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align="<",
            v_align="^",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
| text       | ex         |
| ex         | text       |
|            |            |
|            |            |
|            |            |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align="<",
            v_align="-",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|            |            |
| text       | ex         |
| ex         | text       |
|            |            |
|            |            |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align="<",
            v_align="_",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|            |            |
|            |            |
|            |            |
| text       | ex         |
| ex         | text       |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align=">",
            v_align="^",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|       text |         ex |
|         ex |       text |
|            |            |
|            |            |
|            |            |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align=">",
            v_align="-",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|            |            |
|       text |         ex |
|         ex |       text |
|            |            |
|            |            |
+------------+------------+
""".strip()
    )
    assert (
        table.stringify(
            h_align=">",
            v_align="_",
            max_width=(10,),
            max_height=5,
            maximize_height=True,
        )
        == """
+------------+------------+
|            |            |
|            |            |
|            |            |
|       text |         ex |
|         ex |       text |
+------------+------------+
""".strip()
    )
