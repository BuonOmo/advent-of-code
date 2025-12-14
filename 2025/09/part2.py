#!/usr/bin/env python3

from __future__ import annotations

from itertools import pairwise
from sys import argv
from typing import Generator

type Point = tuple[int, int]
print('salut beauté')


class Vertice:
	def __init__(self, a: Point, b: Point):
		self.a, self.b = sorted([a, b])

	def contains(self, x: Point) -> bool:
		a1, a2 = self.a
		b1, b2 = self.b
		x1, x2 = x
		return a1 <= x1 <= b1 and a2 <= x2 <= b2

	def intersects(self, other: Vertice) -> bool:
		match (self.direction(), other.direction()):
			case ('vertical', 'horizontal'):
				vertical, horizontal = self, other
			case ('horizontal', 'vertical'):
				horizontal, vertical = self, other
			case _:
				return False

		return (
			horizontal.a[0] <= vertical.a[0] < horizontal.b[0]
			and vertical.a[1] <= horizontal.a[1] <= vertical.b[1]
		)

	def direction(self) -> str:
		"""
		horizontal -> index 1 doesn't change
		vertical -> index 0 doesn't change

		>>> Vertice((1, 2), (1, 3)).direction()
		'vertical'
		>>> Vertice((0, 3), (1, 3)).direction()
		'horizontal'
		"""
		a1, _a2 = self.a
		b1, _b2 = self.b
		return 'vertical' if a1 == b1 else 'horizontal'


def parse(filename: str | None = None) -> list[tuple[int, int]]:
	if not filename:
		filename = argv[1]
	rv = []
	with open(filename, 'r') as file:
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


def assert_stuff(tiles: list[tuple[int, int]]):
	"""
	This method helps us understand that every
	next vertice is connected to the previous
	one and changes direction, and that no point
	contains 0 as a coordonate.
	"""
	rev = 1 if tiles[0][1] == tiles[1][1] else 0
	for a, b in pairwise(tiles + [tiles[0]]):
		assert a[rev] == b[rev]
		rev = 1 - rev
	for a, b in tiles:
		assert a > 0 and b > 0


def vertices(
	edges: list[tuple[int, int]],
) -> Generator[Vertice]:
	return (Vertice(a, b) for a, b in pairwise(edges + edges[0:1]))


def is_on_boundary(polygon: list[Vertice], point: Point) -> bool:
	"""
	>>> is_on_boundary(test_polygon,(1,2))
	True
	>>> is_on_boundary(test_polygon,(0,7))
	False
	>>> is_on_boundary(list(vertices(parse('example'))),(9,5))
	True
	"""
	return any(vertice.contains(point) for vertice in polygon)
	# for vertice in polygon:
	# 	if vertice.contains(point):
	# 		return True
	# return False


def is_inside(polygon: list[Vertice], point: Point) -> bool:
	"""
	>>> is_inside(test_polygon,(2,2))
	True
	>>> is_inside(test_polygon,(2,7))
	False
	"""
	other = Vertice(point, (point[0], 0))

	nb = 0
	for vertice in polygon:
		if vertice.direction() == 'vertical':
			continue
		else:
			if vertice.intersects(other):
				nb += 1
	return nb % 2 != 0


def consider(polygon: list[Vertice], a: Point, b: Point) -> bool:
	a1, a2 = a
	b1, b2 = b
	c = (a1, b2)
	d = (b1, a2)
	return (is_on_boundary(polygon, c) or is_inside(polygon, c)) and (
		is_on_boundary(polygon, d) or is_inside(polygon, d)
	)


if __name__ == '__main__':
	tiles = parse('input')
	assert_stuff(tiles)
	polygon = list(vertices(tiles))

	largest = 0
	for i, t1 in enumerate(tiles):
		for t2 in tiles[i + 1 :]:
			# print(
			# 	{
			# 		't1': t1,
			# 		't2': t2,
			# 		'consider': consider(polygon, t1, t2),
			# 		'size': size(t1, t2),
			# 	}
			# )
			if consider(polygon, t1, t2):
				area = size(t1, t2)
				if area == 4649416800:
					print(t1, t2)

				if area > largest:
					largest = area
	print(largest)
else:
	test_polygon = list(vertices([(1, 1), (1, 3), (3, 4), (4, 2)]))

# 4649416800 -->trop haut
