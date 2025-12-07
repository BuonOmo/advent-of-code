#!/usr/bin/env python3

from sys import argv
from enum import Enum
from typing import Any
from functools import reduce

class Op(Enum):
	ADDITION = '+'
	MULTIPLICATION = '*'

	def apply(self, a: int, b: int) -> int:
		if self is Op.ADDITION:
			return a + b
		else:
			return a * b


# 123 328
#  45 64
#   6 98
# *   +

def parse(filename: str|None = None) -> tuple[list[str], list[Op]]:
	if not filename:
		filename = argv[1]
	with open(filename, 'r') as file:
		lines: list[str] = []
		ops: list[Op]|None = None
		for line in file:
			if line[0] in Op:
				ops = [Op(i) for i in line.split()]
			else:
				lines.append(line.rstrip('\n'))
		assert(ops)
		return (lines, ops)


# 123 328
#  45 64
#   6 98

def transpose(m: list[list[Any]]) -> list[list[Any]]:
	'''
	>>> transpose(['13', ' 1'])
	[['1', ' '], ['3', '1']]
	>>> transpose([[1, 4], [2, 5], [3, 6]])
	[[1, 2, 3], [4, 5, 6]]
	'''
	x = len(m[0])
	y = len(m)
	t: list[list[Any]] = [[None]*y for _ in range(x)]
	for i in range(y):
		for j in range(x):
			t[j][i] = m[i][j]
	return t

# 1
# 24
# 356
#
# 369
# 248
# 8
def transform(t: list[list[str]]) -> list[list[int]]:
	'''
	>>> transform([['1', '2'], ['4', ' '], [' ', ' '], [' ', '1']])
	[[12, 4], [1]]
	'''
	nums = []
	i = 0
	for line in t:
		nb = ''.join(line).strip()
		if nb.isdigit():
			if i >= len(nums):
				nums.append([])
			nums[i].append(int(nb))
		else:
			i += 1
	return nums

if __name__ == '__main__':
	lines, ops = parse()
	numss = transform(transpose(lines))
	assert(len(numss) == len(ops))
	print(sum(
		reduce(op.apply, nums) for (nums, op) in zip(numss, ops)
	))



	# for i in range(len(numss)):
	# 	ops[i]
	# 	numss[i]
