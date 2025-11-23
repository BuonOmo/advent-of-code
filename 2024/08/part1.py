#!/usr/bin/env python3

from sys import argv
from pprint import pp
from collections import defaultdict

point = tuple[int, int]

def antinodes(a: point, b: point) -> tuple[point, point]:
	'''
	Find two antinodes as being:
	- on the same line as `a` and `b`
	- one point is twice as far from `a` than `b`
	- the other is twice as far as `b` than `a`

	>>> antinodes((1, 1), (2, 2))
	((0, 0), (3, 3))
	>>> antinodes((1, 2), (2, 1))
	((0, 3), (3, 0))
	'''
	x1, y1 = a
	x2, y2 = b

	dx = x2 - x1
	dy = y2 - y1

	return (
		(x1 - dx, y1 - dy),
		(x2 + dx, y2 + dy)
	)

def parse() -> tuple[tuple[int, int], dict[str, list[point]]]:
	data: dict[str, list[point]] = defaultdict(list)
	sx, sy = 0, 0
	with open(argv[1], 'r') as file:
		for x, line in enumerate(file):
			sx += 1
			sy = len(line.strip())
			for y, char in enumerate(line.strip()):
				if char == '.':
					continue
				data[char].append((x, y))
	return (sx, sy), data

if __name__ == '__main__':
	(sx, sy), data = parse()
	all_antinodes: set[point] = set()

	for value in data.values():
		for i in range(len(value) - 1):
			for j in range(i + 1, len(value)):
				all_antinodes.update(antinodes(value[i], value[j]))

	print(sum(1 for (x, y) in all_antinodes if 0 <= x < sx and 0 <= y < sy))
