#!/usr/bin/env python3

from sys import argv
from pprint import pp
from collections import defaultdict

point = tuple[int, int]

def antinodes(a: point, b: point, size_x: int, size_y: int) -> set[point]:
	'''
	Find all the antinodes as being:
	- on the same line as `a` and `b`
	- within the bounds of the box
	- separated by the distance between `a` and `b`
	- including `a` and `b`

	>>> antinodes((1, 1), (2, 2), 5, 5)
	{(4, 4), (0, 0), (1, 1), (3, 3), (2, 2)}
	>>> antinodes((1, 0), (0, 1), 2, 2)
	{(1, 0), (0, 1)}
	'''
	x1, y1 = a
	x2, y2 = b

	dx = x2 - x1
	dy = y2 - y1

	s = set([])

	px, py = a
	while 0 <= px < size_x and 0 <= py < size_y:
		s.add((px, py))
		px -= dx
		py -= dy

	px, py = b
	while 0 <= px < size_x and 0 <= py < size_y:
		s.add((px, py))
		px += dx
		py += dy

	return s

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
				all_antinodes |= antinodes(value[i], value[j], sx, sy)

	print(sum(1 for (x, y) in all_antinodes))
