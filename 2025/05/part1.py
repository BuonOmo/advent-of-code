#!/usr/bin/env python3

from sys import argv
from pprint import pp

def parse() -> tuple[list[range], list[int]]:
	with open(argv[1], 'r') as file:
		ranges = []
		for line in file:
			line = line.strip()
			if not line:
				break
			a, b = line.split('-')
			ranges.append(range(int(a), int(b) + 1))

		ids = [int(line) for line in file]
		return (ranges, ids)

def is_fresh(ranges: list[range], id: int) -> bool:
	for range in ranges:
		if id in range:
			return True
	return False

if __name__ == '__main__':
	ranges, ids = parse()
	pp(sum(1 for id in ids if is_fresh(ranges, id)))
