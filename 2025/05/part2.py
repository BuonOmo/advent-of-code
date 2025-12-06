#!/usr/bin/env python3

from sys import argv

def parse() -> list[range]:
	with open(argv[1], 'r') as file:
		ranges = []
		for line in file:
			line = line.strip()
			if not line:
				break
			a, b = line.split('-')
			ranges.append(range(int(a), int(b) + 1))

		return ranges

def union(a: range, b: range) -> range|None:
	assert(a.start <= b.start)

	if a.stop < b.start:
		return None

	return range(a.start, max(a.stop, b.stop))

def united(ranges: list[range]) -> list[range]:
	'''
	>>> united([range(0, 4), range(1, 2), range(6, 8), range(7, 9), range(10, 11)])
	[range(0, 4), range(6, 9), range(10, 11)]
	'''
	ranges = sorted(ranges, key=lambda range: range.start)
	rv = list()
	u = ranges[0]
	for i in range(1, len(ranges)):
		v = union(u, ranges[i])
		if v:
			u = v
			continue
		rv.append(u)
		u = ranges[i]
	rv.append(u)
	return rv

def count(ranges: list[range]) -> int:
	rv = 0
	for range in ranges:
		rv += len(range)
	return rv

if __name__ == '__main__':
	ranges = parse()
	ranges = united(ranges)
	print(count(ranges))
