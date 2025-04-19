from enum import Enum


class Color(Enum):
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"
    BRIGHT_BLACK = "\x1b[90m"
    BRIGHT_RED = "\x1b[91m"
    BRIGHT_GREEN = "\x1b[92m"
    BRIGHT_YELLOW = "\x1b[93m"
    BRIGHT_BLUE = "\x1b[94m"
    BRIGHT_MAGENTA = "\x1b[95m"
    BRIGHT_CYAN = "\x1b[96m"
    BRIGHT_WHITE = "\x1b[97m"


class BgColor(Enum):
    BLACK = "\x1b[40m"
    RED = "\x1b[41m"
    GREEN = "\x1b[42m"
    YELLOW = "\x1b[43m"
    BLUE = "\x1b[44m"
    MAGENTA = "\x1b[45m"
    CYAN = "\x1b[46m"
    WHITE = "\x1b[47m"
    BRIGHT_BLACK = "\x1b[100m"
    BRIGHT_RED = "\x1b[101m"
    BRIGHT_GREEN = "\x1b[102m"
    BRIGHT_YELLOW = "\x1b[103m"
    BRIGHT_BLUE = "\x1b[104m"
    BRIGHT_MAGENTA = "\x1b[105m"
    BRIGHT_CYAN = "\x1b[106m"
    BRIGHT_WHITE = "\x1b[107m"


def style(
    text: str,
    *,
    fg: Color | tuple[int, int, int] | None = None,
    bg: BgColor | tuple[int, int, int] | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    strike: bool = False,
    double_underline: bool = False,
    inverse: bool = False,
    hidden: bool = False,
) -> str:
    ansi_parts = []

    if isinstance(fg, tuple) and len(fg) == 3:
        r, g, b = fg
        ansi_parts.append(f"\x1b[38;2;{r};{g};{b}m")
    elif isinstance(fg, Color):
        ansi_parts.append(fg.value)

    if isinstance(bg, tuple) and len(bg) == 3:
        r, g, b = bg
        ansi_parts.append(f"\x1b[48;2;{r};{g};{b}m")
    elif isinstance(bg, BgColor):
        ansi_parts.append(bg.value)

    if bold:
        ansi_parts.append("\x1b[1m")
    if italic:
        ansi_parts.append("\x1b[3m")
    if underline:
        ansi_parts.append("\x1b[4m")
    if strike:
        ansi_parts.append("\x1b[9m")
    if double_underline:
        ansi_parts.append("\x1b[21m")
    if inverse:
        ansi_parts.append("\x1b[7m")
    if hidden:
        ansi_parts.append("\x1b[8m")

    start = "".join(ansi_parts)
    reset = "\x1b[0m"
    text = text.replace(reset, f"{reset}{start}")
    return f"{start}{text}{reset}"


def link(url: str, text: str | None = None) -> str:
    if text is None:
        text = url
    return f"\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\"
