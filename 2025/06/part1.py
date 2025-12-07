#!/usr/bin/env python3

from sys import argv
from enum import Enum
from typing import Generator

class Op(Enum):
	ADDITION = '+'
	MULTIPLICATION = '*'

	def apply(self, a: int, b: int) -> int:
		if self is Op.ADDITION:
			return a + b
		else:
			return a * b


def parse() -> Generator[list[int]|list[Op]]:
	with open(argv[1], 'r') as file:
		for line in file:
			line = line.split()
			if line[0].isdigit():
				yield [int(i) for i in line]
			else:
				yield [Op(i) for i in line]

if __name__ == '__main__':
	ops, *nums = reversed(list(parse()))
	counts: list[int] = nums[0]
	for line in nums[1:]:
		for i in range(len(line)):
			counts[i] = ops[i].apply(counts[i], line[i])
	print(counts)
	print(sum(counts))
