#!/usr/bin/env python3

import fileinput
from pprint import pp
from itertools import groupby, product
import os

print = pp

# The locks are schematics that have the top row
# filled (`#`) and the bottom row empty (`.`);
# the keys have the top row empty and the bottom
# row filled. If you look closely, you'll see
# that each schematic is actually a set of columns
# of various heights, either extending downward
# from the top (for locks) or upward from the
# bottom (for keys).
buffer = []
data = []
def parse(lines: list[str]) -> tuple[str, list[int]]:
	type = "lock" if lines[0][0] == "#" else "key"
	tr = list(zip(*lines[1:-1]))
	return type, [line.count("#") for line in tr]

with open(f"{os.path.dirname(__file__)}/input") as f:
	for line in f:
		if line.strip() == "":
			data.append(parse(buffer))
			buffer = []
		else:
			buffer.append(line.strip())

data.append(parse(buffer))

keys, locks = [], []

for type, heights in data:
	if type == "key":
		keys.append(heights)
	elif type == "lock":
		locks.append(heights)

fitting = 0
for key, lock in product(keys, locks):
	if all([k + l < 6 for k, l in zip(key, lock)]):
		fitting += 1

print(fitting)
