import curses
import time
from pprint import pformat
from typing import Any

from curses_formatter import CursesFormatter

from pygments import highlight
from pygments.lexers import PythonLexer


def dbg(*args):
    from pprint import pp

    pp(*args, stream=open("debug.log", "a"))


class Cursed:
	"""
	Use me with a context manager. then you can
	use the `print_grid` method to print a grid of
	text centered to the guard. And the `pp` method
	to debug your code. example:
	```
	with Cursed() as c:
		c.pp({'a': 1, 'b': 2})
		c.print_grid('.#\\n..\\n', (10, 10))
	```
	This library assumes you will handle pauses yourself
	with `time.sleep`.
	"""
	def __init__(self):
		self.stdscr = curses.initscr()
		self.pad = None
		self.pad_pos = 0
		y, x = self.stdscr.getmaxyx()
		self.grid_window = curses.newwin(y, x // 2 - 10, 0, 0)
		curses.noecho()
		curses.curs_set(0)

	def __del__(self):
		self.close()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	def close(self):
		curses.curs_set(1)
		curses.echo()
		curses.endwin()

	def pp(self, obj: Any):
		y, x = self.stdscr.getmaxyx()
		_wy, wx = self.grid_window.getmaxyx()
		str = pformat(obj, width=x - wx)
		split = str.splitlines()
		nlines = len(split)
		ncols = max(len(line) for line in split)
		if self.pad:
			self.pad.clear()
			self.pad.refresh(0, 0, 0, wx, y - 1, x - 1)
		self.pad = curses.newpad(nlines + 1, ncols + 1)
		self.pad_pos = 0
		highlight(str, PythonLexer(), CursesFormatter(), self.pad)
		self.pad.refresh(self.pad_pos, 0, 0, wx, y - 1, x - 1)

	def print_grid(self, text: str, center: tuple[int, int] = (0, 0)):
		height, width = self.grid_window.getmaxyx()

		# Box
		height -= 2
		width -= 2

		lines = text.splitlines()
		# Determine text dimensions
		n_rows = len(lines)
		n_cols = len(lines[0])

		# Compute view size (cannot exceed terminal or text size)
		view_h = min(height, n_rows)
		view_w = min(width, n_cols)

		# Center within the text (center is guaranteed in bounds)
		center_row, center_col = center

		# Compute top-left of the view in text coordinates, then clamp
		top = center_row - view_h // 2
		left = center_col - view_w // 2
		top = max(0, min(top, n_rows - view_h))
		left = max(0, min(left, n_cols - view_w))

		# Extract view lines, padding as necessary
		view_lines = []
		for r in range(top, top + view_h):
			line = lines[r] if r < n_rows else ""
			# ensure line has at least left characters
			if len(line) < left:
				line = line.ljust(left)
			segment = line[left : left + view_w]
			if len(segment) < view_w:
				segment = segment.ljust(view_w)
			if len(segment) > width:
				segment = segment[:width]
			view_lines.append(segment)

		self.grid_window.clear()
		for i, line in enumerate(view_lines):
			self.grid_window.addstr(i + 1, 1, line)
		self.grid_window.box()
		self.grid_window.refresh()

	# def wait(self) -> None:
	# 	time.sleep(0.1)
	# 	if not self.pad:
	# 		return
	# 	self.pad.nodelay(True)  # self.pad.timeout(0)
	# 	cmd = self.pad.getch()
	# 	if cmd == curses.KEY_MOUSE:
	# 		dbg(f"cmd: {cmd} pad_pos: {self.pad_pos}")
	# 		# self.pad_pos = max(self.pad_pos - 1, 0)
 #        # elif cmd == curses.KEY_UP:
 #        # self.pad_pos += 1
 #        else:
 #            return
 #        y, x = self.stdscr.getmaxyx()
 #        _wy, wx = self.grid_window.getmaxyx()
 #        self.pad.refresh(self.pad_pos, 0, 0, wx, y - 1, x - 1)

	def __getattr__(self, name):
		return getattr(self.stdscr, name)


if __name__ == "__main__":
    with Cursed() as cursed, open("input", "r") as file:
        curses.start_color()
        curses.use_default_colors()
        curses.mousemask(curses.ALL_MOUSE_EVENTS)
        cursed.pp(
            [
                "Hello, long long long long long long long long long long long long long long World!",
                "This is a test.",
                "Another line.\n",
                {"response": 42},
                list(range(100)),
            ]
        )
        str = file.read()
        for i in range(100):
            cursed.print_grid(str, (i, i))
            cursed.pp((i, i))
            time.sleep(0.1)
            # cursed.wait()
