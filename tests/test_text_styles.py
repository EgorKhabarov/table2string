from table2string.text_styles import style, link, Color, BgColor


def test_text_style():
    assert Color.RED == Color("\x1b[31m")
    assert (
        "Link: "
        + link(
            "https://site.com",
            style("Red", fg=(255, 100, 100), bold=True)
            + style("&", underline=True)
            + style("Blue", fg=Color.BLUE, strike=True),
        )
        + " Text "
        + style("Italic", italic=True)
        + "!"
    ) == (
        "Link: "
        "\x1b]8;;https://site.com\x1b\\"
        "\x1b[38;2;255;100;100m\x1b[1mRed\x1b[0m"
        "\x1b[4m&\x1b[0m"
        "\x1b[34m\x1b[9mBlue\x1b[0m"
        "\x1b]8;;\x1b\\"
        " Text \x1b[3mItalic\x1b[0m!"
    )
    assert (
        style("text", bg=BgColor.YELLOW, double_underline=True)
        == "\x1b[43m\x1b[21mtext\x1b[0m"
    )
    assert (
        style("text", bg=(255, 255, 0), inverse=True)
        == "\x1b[48;2;255;255;0m\x1b[7mtext\x1b[0m"
    )
    assert style("text", hidden=True) == "\x1b[8mtext\x1b[0m"

    assert (
        link("example.com", "text")
        == link("https://example.com", "text")
        == "\x1b]8;;https://example.com\x1b\\text\x1b]8;;\x1b\\"
    )
    assert (
        link("example.com")
        == "\x1b]8;;https://example.com\x1b\\example.com\x1b]8;;\x1b\\"
    )
    assert (
        link("https://example.com")
        == "\x1b]8;;https://example.com\x1b\\https://example.com\x1b]8;;\x1b\\"
    )
