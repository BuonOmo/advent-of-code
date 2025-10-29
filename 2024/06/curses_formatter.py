# https://pygments.org/docs/formatterdevelopment/
"""
Formatter for 256-color terminal output using curses.
"""

from pygments.formatter import Formatter
from pygments.style import ansicolors
import curses


__all__ = ["CursesFormatter"]


class CursesFormatter(Formatter):
    """
    Options accepted:

    `style`
        The style to use, can be a string or a Style subclass (default:
        ``'default'``).

    `linenos`
        Set to ``True`` to have line numbers on the terminal output as well
        (default: ``False`` = no line numbers).
    """

    name = "Curses"
    aliases = ["curses"]
    filenames = []

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        if self.encoding:
            raise ValueError("Encoding is not supported")

        curses.start_color()
        curses.use_default_colors()

        self.xterm_colors = []
        self.best_match = {}
        self.style_pair = {}

        self.usebold = "nobold" not in options
        self.useunderline = "nounderline" not in options
        self.useitalic = "noitalic" not in options

        self._build_color_table()  # build an RGB-to-256 color conversion table
        self._setup_styles()  # convert selected style's colors to term. colors

        self.linenos = options.get("linenos", False)
        self._lineno = 0

    def _build_color_table(self):
        # colors 0..15: 16 basic colors

        self.xterm_colors.append((0x00, 0x00, 0x00))  # 0
        self.xterm_colors.append((0xCD, 0x00, 0x00))  # 1
        self.xterm_colors.append((0x00, 0xCD, 0x00))  # 2
        self.xterm_colors.append((0xCD, 0xCD, 0x00))  # 3
        self.xterm_colors.append((0x00, 0x00, 0xEE))  # 4
        self.xterm_colors.append((0xCD, 0x00, 0xCD))  # 5
        self.xterm_colors.append((0x00, 0xCD, 0xCD))  # 6
        self.xterm_colors.append((0xE5, 0xE5, 0xE5))  # 7
        self.xterm_colors.append((0x7F, 0x7F, 0x7F))  # 8
        self.xterm_colors.append((0xFF, 0x00, 0x00))  # 9
        self.xterm_colors.append((0x00, 0xFF, 0x00))  # 10
        self.xterm_colors.append((0xFF, 0xFF, 0x00))  # 11
        self.xterm_colors.append((0x5C, 0x5C, 0xFF))  # 12
        self.xterm_colors.append((0xFF, 0x00, 0xFF))  # 13
        self.xterm_colors.append((0x00, 0xFF, 0xFF))  # 14
        self.xterm_colors.append((0xFF, 0xFF, 0xFF))  # 15

        # colors 16..232: the 6x6x6 color cube

        valuerange = (0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF)

        for i in range(217):
            r = valuerange[(i // 36) % 6]
            g = valuerange[(i // 6) % 6]
            b = valuerange[i % 6]
            self.xterm_colors.append((r, g, b))

        # colors 233..253: grayscale

        for i in range(1, 22):
            v = 8 + i * 10
            self.xterm_colors.append((v, v, v))

    def _closest_color(self, r, g, b):
        distance = 257 * 257 * 3  # "infinity" (>distance from #000000 to #ffffff)
        match = 0

        for i in range(0, 254):
            values = self.xterm_colors[i]

            rd = r - values[0]
            gd = g - values[1]
            bd = b - values[2]
            d = rd * rd + gd * gd + bd * bd

            if d < distance:
                match = i
                distance = d
        return match

    def _color_index(self, color):
        index = self.best_match.get(color, None)
        if color in ansicolors:
            # strip the `ansi/#ansi` part and look up code
            index = color
            self.best_match[color] = index
        if index is None:
            try:
                rgb = int(str(color), 16)
            except ValueError:
                rgb = 0

            r = (rgb >> 16) & 0xFF
            g = (rgb >> 8) & 0xFF
            b = rgb & 0xFF
            index = self._closest_color(r, g, b)
            self.best_match[color] = index
        return index

    def _setup_styles(self):
        pair_index = 1
        for ttype, ndef in self.style:
            # get foreground from ansicolor if set
            color = -1
            bg = -1
            attrs = 0
            if ndef["ansicolor"]:
                color = self._color_index(ndef["ansicolor"])
            elif ndef["color"]:
                color = self._color_index(ndef["color"])

            if ndef["bgansicolor"]:
                bg = self._color_index(ndef["bgansicolor"])
            elif ndef["bgcolor"]:
                bg = self._color_index(ndef["bgcolor"])

            if self.usebold and ndef["bold"]:
                attrs |= curses.A_BOLD
            if self.useunderline and ndef["underline"]:
                attrs |= curses.A_UNDERLINE
            if self.useitalic and ndef["italic"]:
                attrs |= curses.A_ITALIC
            curses.init_pair(pair_index, color, bg)
            self.style_pair[str(ttype)] = curses.color_pair(pair_index) | attrs
            pair_index += 1

    def _write_lineno(self, outfile):
        self._lineno += 1
        outfile.addstr("%s%04d: " % (self._lineno != 1 and "\n" or "", self._lineno))

    def format(self, tokensource, outfile):
        if self.linenos:
            self._write_lineno(outfile)

        for ttype, value in tokensource:
            not_found = True
            while ttype and not_found:
                try:
                    pair = self.style_pair[str(ttype)]

                    # Like TerminalFormatter, add "reset colors" escape sequence
                    # on newline.
                    spl = value.split("\n")
                    for line in spl[:-1]:
                        if line:
                            outfile.addstr(line + "\n", pair)
                        if self.linenos:
                            self._write_lineno(outfile)
                        else:
                            outfile.addstr("\n")

                    if spl[-1]:
                        outfile.addstr(spl[-1], pair)

                    not_found = False

                except KeyError:
                    ttype = ttype.parent

            if not_found:
                outfile.addstr(value)

        if self.linenos:
            outfile.addstr("\n")


if __name__ == "__main__":
    from pygments import highlight
    from pygments.lexers import PythonLexer

    def main(stdscr):
        curses.start_color()
        curses.use_default_colors()

        str = """
# this should be a comment
print("Hello World")
async def function(a,b,c, *d, **kwarg:Bool)->Bool:
    pass
    return 123, 0xb3e3

"""

        highlight(str, PythonLexer(), CursesFormatter(), stdscr)
        stdscr.getch()
        highlight(str, PythonLexer(), CursesFormatter(linenos=True), stdscr)
        stdscr.getch()

    curses.wrapper(main)
