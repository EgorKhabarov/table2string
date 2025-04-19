import re

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
    START_COLOR_REGEX = re.compile(rf"^({COLOR_REGEX.pattern})*\x1b\[0m")
    CENTER_COLOR_REGEX = re.compile(rf"({COLOR_REGEX.pattern})*\x1b\[0m(?!$)")

    OSC_LINK_REGEX = re.compile(
        r"(?s)(\x1b]8;;(?P<url>[^\x1b]+)\x1b\\)(?P<text>.*?)(\x1b]8;;\x1b\\)"
    )
    OSC_LINK_OPEN = "\x1b]8;;{url}\x1b\\"
    OSC_LINK_CLOSE = "\x1b]8;;\x1b\\"
    OSC_OPEN_PATTERN = re.compile(r"\x1b]8;;(?P<url>[^\x1b]+)\x1b\\")
    ESCAPE_UNSAFE_ANSI_REGEX = re.compile(r"\x1b(?!\[[0-9;]*m)")

    def __init__(self, escape_unsafe: bool = False):
        self.escape_unsafe = escape_unsafe

    def split_text(
        self,
        text: str,
        width: int | None = None,
        height: int | None = None,
        line_break_symbol: str = "\\",
        cell_break_symbol: str = "…",
    ) -> tuple[list[str], list[str], bool, dict[str, tuple[str, ...]]]:
        if self.escape_unsafe:
            text = self.ESCAPE_UNSAFE_ANSI_REGEX.sub(r"\\x1b", text)

        plain = ""
        events: list[dict] = []
        plain_idx = 0
        i = 0
        while i < len(text):
            mo = self.OSC_OPEN_PATTERN.match(text[i:])
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
                # <-- здесь правка: ставим '<' слева, чтобы не захватывать границу start
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
            line_out = self.START_COLOR_REGEX.sub("", line_out)
            line_out = self.CENTER_COLOR_REGEX.sub("\x1b[0m", line_out)

            restored.append(line_out)
            inherited_color = curr_color

        return restored, symbols, is_subtable, borders


class HtmlTextSplitter(AnsiTextSplitter):
    pass
