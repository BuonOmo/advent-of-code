#!/usr/bin/env python3

from sys import argv

# 50


def parse() -> list[tuple[int, int]]:
	rv = []
	with open(argv[1], 'r') as file:
		for line in file:
			a, b = line.split(',')
			rv.append((int(a), int(b)))
		return rv


def size(a: tuple[int, int], b: tuple[int, int]) -> int:
	"""
	>>> size((3, 2), (1, 1))
	6
	"""
	a1, a2 = a
	b1, b2 = b
	return (abs(b1 - a1) + 1) * (abs(b2 - a2) + 1)


if __name__ == '__main__':
	tiles = parse()
	largest = 0
	for i, t1 in enumerate(tiles):
		for t2 in tiles[i + 1 :]:
			area = size(t1, t2)
			if area > largest:
				largest = area
	print(largest)
