#!/usr/bin/env python3

from sys import argv
from pprint import pp
from collections import defaultdict

point = tuple[int, int]

data: dict[str, list[point]] = defaultdict(list)

with open(argv[1], "r") as file:
	for x, line in enumerate(file):
		for y, char in enumerate(line.strip()):
			if char == '.':
				continue
			data[char].append((x, y))


pp(data)
