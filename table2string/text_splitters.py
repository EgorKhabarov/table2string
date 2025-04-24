import re
import html
from html.parser import HTMLParser

from table2string.utils import get_text_width_in_console


class BaseTextSplitter:
    def split_text(
        self,
        text: str,
        width: int | None = None,
        height: int | None = None,
        line_break_symbol: str = "\\",
        cell_break_symbol: str = "…",
    ) -> tuple[list[str], list[str], bool, dict[str, tuple[str, ...]]]:
        """
        Splits text to the desired width and height

        :param text: Text
        :param width: Width
        :param height: Height
        :param line_break_symbol: "\\" or "↩" or chr(8617) or "\\U000021a9"
        :param cell_break_symbol: "…" or chr(8230) or "\\U00002026"
        :return: Split text by width and height
        lines, symbols, is_subtable, borders
        """
        lines = text.split("\n")

        if width is None:
            width = len(max(lines))

        result_lines: list[str] = []
        result_symbols: list[str] = []

        for line in lines:
            if get_text_width_in_console(line) == 0:
                result_lines.append("")
                result_symbols.append(" ")
            else:
                while line:
                    if get_text_width_in_console(line) <= width:
                        result_lines.append(line)
                        result_symbols.append(" ")
                        line = ""
                    else:
                        w = 0
                        assert width >= 1, width
                        while get_text_width_in_console(line[:w]) <= width - 1:
                            w += 1
                        result_lines.append(line[:w])
                        result_symbols.append(line_break_symbol)
                        line = line[w:]

        if height and len(result_lines) > height:
            result_lines = result_lines[:height]
            result_symbols = result_symbols[:height]
            result_symbols[-1] = cell_break_symbol

        is_subtable = False
        borders: dict[str, tuple[str, ...]] = {}
        return result_lines, result_symbols, is_subtable, borders


class AnsiTextSplitter(BaseTextSplitter):
    COLOR_REGEX = re.compile(r"\x1b\[[0-9;]*m")
    OSC_LINK_OPEN_REGEX = re.compile(r"\x1b]8;;(?P<url>[^\x1b]+)\x1b\\")
    OSC_LINK_CLOSE = "\x1b]8;;\x1b\\"

    REDUNDANT_COLOR_ANSI_REGEX_1 = re.compile(rf"^({COLOR_REGEX.pattern})*\x1b\[0m")
    REDUNDANT_COLOR_ANSI_REGEX_2 = re.compile(rf"({COLOR_REGEX.pattern})*\x1b\[0m(?!$)")

    def split_text(
        self,
        text: str,
        width: int | None = None,
        height: int | None = None,
        line_break_symbol: str = "\\",
        cell_break_symbol: str = "…",
    ) -> tuple[list[str], list[str], bool, dict[str, tuple[str, ...]]]:
        plain = ""
        events: list[dict] = []
        plain_idx = 0
        i = 0
        while i < len(text):
            mo = self.OSC_LINK_OPEN_REGEX.match(text[i:])
            if mo:
                tok = mo.group(0)
                url = mo.group("url")
                events.append(
                    {
                        "type": "link_open",
                        "plain_pos": plain_idx,
                        "token": tok,
                        "url": url,
                    }
                )
                i += len(tok)
                continue
            if text.startswith(self.OSC_LINK_CLOSE, i):
                events.append(
                    {
                        "type": "link_close",
                        "plain_pos": plain_idx,
                        "token": self.OSC_LINK_CLOSE,
                    }
                )
                i += len(self.OSC_LINK_CLOSE)
                continue
            mc = self.COLOR_REGEX.match(text, i)
            if mc:
                tok = mc.group(0)
                events.append({"type": "color", "plain_pos": plain_idx, "token": tok})
                i += len(tok)
                continue
            ch = text[i]
            plain += ch
            if ch != "\n":
                plain_idx += 1
            i += 1

        lines, symbols, is_subtable, borders = super().split_text(
            text=plain,
            width=width,
            height=height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
        )

        boundaries = []
        off = 0
        for ln in lines:
            boundaries.append((off, off + len(ln)))
            off += len(ln)

        # Собираем link spans по парам open/close
        opens = [e for e in events if e["type"] == "link_open"]
        closes = [e for e in events if e["type"] == "link_close"]
        links = [
            {
                "url": op["url"],
                "plain_start": op["plain_pos"],
                "plain_end": cl["plain_pos"],
            }
            for op, cl in zip(opens, closes)
        ]

        # Приоритет вставки (закрытие сначала)
        priority = {"link_close": 0, "link_open": 1, "color": 2}

        # Восстанавливаем по строкам
        restored: list[str] = []
        inherited_color = ""
        for (start, end), ln in zip(boundaries, lines):
            # Ссылки, остающиеся открытыми через границу сверху
            active = [
                link
                for link in links
                if link["plain_start"] < start < link["plain_end"]
            ]
            prefix = inherited_color + "".join(
                f"\x1b]8;;{link['url']}\x1b\\" for link in active
            )
            out = [prefix]
            last = 0

            # События в этой строке
            evs: list[dict] = []
            for e in events:
                if e["type"] == "color" and start <= e["plain_pos"] < end:
                    evs.append(e)
            for link in links:
                if start <= link["plain_start"] < end:
                    evs.append(
                        {
                            "type": "link_open",
                            "plain_pos": link["plain_start"],
                            "token": f"\x1b]8;;{link['url']}\x1b\\",
                        }
                    )
                # <-- здесь правка: ставим "<" слева, чтобы не захватывать границу start
                if start < link["plain_end"] <= end:
                    evs.append(
                        {
                            "type": "link_close",
                            "plain_pos": link["plain_end"],
                            "token": self.OSC_LINK_CLOSE,
                        }
                    )

            # Сортируем и вставляем
            evs.sort(key=lambda e: (e["plain_pos"], priority[e["type"]]))
            curr_color = inherited_color
            for e in evs:
                rel = e["plain_pos"] - start
                if rel > last:
                    out.append(ln[last:rel])
                out.append(e["token"])
                if e["type"] == "color":
                    curr_color = (
                        "" if e["token"] == "\x1b[0m" else curr_color + e["token"]
                    )
                last = rel
            out.append(ln[last:])

            # Закрываем ссылки, выходящие за конец строки
            for link in links:
                if link["plain_start"] < end < link["plain_end"]:
                    out.append(self.OSC_LINK_CLOSE)

            # Закрываем цвет, если он активен
            if curr_color:
                out.append("\x1b[0m")

            # Убираем лишние сбросы
            line_out = "".join(out)
            line_out = self.REDUNDANT_COLOR_ANSI_REGEX_1.sub("", line_out)
            line_out = self.REDUNDANT_COLOR_ANSI_REGEX_2.sub("\x1b[0m", line_out)

            restored.append(line_out)
            inherited_color = curr_color

        return restored, symbols, is_subtable, borders


class AnsiTextSplitterEscapeUnsafe(AnsiTextSplitter):
    ESCAPE_UNSAFE_ANSI_REGEX = re.compile(
        r"\x1b(?!\[[0-9;]*m|]8;;|\\)"
        r"|[\x00-\x09\x0b-\x1a\x1c-\x1f\x7f-\x9f\u200b-\u200d\uFEFF]"
    )

    def split_text(
        self,
        text: str,
        width: int | None = None,
        height: int | None = None,
        line_break_symbol: str = "\\",
        cell_break_symbol: str = "…",
    ) -> tuple[list[str], list[str], bool, dict[str, tuple[str, ...]]]:
        text = self.ESCAPE_UNSAFE_ANSI_REGEX.sub(
            lambda m: repr(m[0])[1:-1],
            text,
        )
        return super().split_text(
            text=text,
            width=width,
            height=height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
        )


class HtmlTextSplitter(AnsiTextSplitterEscapeUnsafe):
    def split_text(
        self,
        text: str,
        width: int | None = None,
        height: int | None = None,
        line_break_symbol: str = "\\",
        cell_break_symbol: str = "…",
    ) -> tuple[list[str], list[str], bool, dict[str, tuple[str, ...]]]:
        text = text.replace("\x1b", "\\x1b")
        parser = _HTML2ANSIParser()
        parser.feed(text)
        text = parser.get_text()
        return super().split_text(
            text=text,
            width=width,
            height=height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
        )


class MarkdownTextSplitter(HtmlTextSplitter):
    def split_text(
        self,
        text: str,
        width: int | None = None,
        height: int | None = None,
        line_break_symbol: str = "\\",
        cell_break_symbol: str = "…",
    ) -> tuple[list[str], list[str], bool, dict[str, tuple[str, ...]]]:
        # Будущая реализация
        return super().split_text(
            text=text,
            width=width,
            height=height,
            line_break_symbol=line_break_symbol,
            cell_break_symbol=cell_break_symbol,
        )


class _HTML2ANSIParser(HTMLParser):
    RGB_REGEX = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")
    ESCAPE_N_REGEX = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")

    def __init__(self):
        super().__init__()
        self.result = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "p":
            self.result.append("\n")
        elif tag == "br":
            self.result.append("\n")
        elif tag == "b":
            self.result.append("\x1b[1m")
        elif tag == "i":
            self.result.append("\x1b[3m")
        elif tag == "u":
            self.result.append("\x1b[4m")
        elif tag == "s":
            self.result.append("\x1b[9m")
        elif tag == "mark":
            # Жёлтый фон ANSI
            self.result.append("\x1b[48;2;255;255;0m")
        elif tag == "a" and "href" in attrs:
            url = attrs["href"]
            self.result.append(f"\x1b]8;;{url}\x1b\\")

        if tag in ("b", "i", "u", "s", "span", "mark", "a") and "style" in attrs:
            style = attrs["style"]
            for part in style.split(";"):
                key, sep, value = part.partition(":")
                if key.strip() == "color" and value:
                    val = value.strip()
                    if val.startswith("#") and len(val) == 7:
                        r = int(val[1:3], 16)
                        g = int(val[3:5], 16)
                        b = int(val[5:7], 16)
                    else:
                        m = self.RGB_REGEX.search(val)
                        if m:
                            r, g, b = map(int, m.groups())
                        else:
                            continue
                    self.result.append(f"\x1b[38;2;{r};{g};{b}m")
                if key.strip() == "background-color" and value:
                    val = value.strip()
                    if val.startswith("#") and len(val) == 7:
                        r = int(val[1:3], 16)
                        g = int(val[3:5], 16)
                        b = int(val[5:7], 16)
                    else:
                        m = self.RGB_REGEX.search(val)
                        if m:
                            r, g, b = map(int, m.groups())
                        else:
                            continue
                    self.result.append(f"\x1b[48;2;{r};{g};{b}m")

    def handle_endtag(self, tag):
        if tag == "p":
            self.result.append("\n")
        elif tag == "a":
            self.result.append("\x1b]8;;\x1b\\")

        if tag in ("b", "i", "u", "s", "span", "mark", "a"):
            self.result.append("\x1b[0m")

    def handle_data(self, data):
        self.result.append(html.unescape(data))

    def get_text(self):
        text = "".join(self.result)
        result = self.ESCAPE_N_REGEX.sub("\n\n", text.strip())
        return result
