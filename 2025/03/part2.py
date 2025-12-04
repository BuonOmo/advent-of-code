#!/usr/bin/env python3

from sys import argv
from pprint import pp

def parse() -> list[list[int]]:
	with open(argv[1], 'r') as file:
		return [[int(c) for c in line.strip()] for line in file]

def find_joltage(bank: list[int]) -> int:
	'''
	>>> find_joltage([int(i) for i in '987654321111111'])
	987654321111
	>>> find_joltage([int(i) for i in '811111111111119'])
	811111111119
	>>> find_joltage([int(i) for i in '234234234234278'])
	434234234278
	>>> find_joltage([int(i) for i in '818181911112111'])
	888911112111
	'''
	rv = 0
	position = -1
	for i in range(11, -1, -1):
		max = -1
		for j in range(position + 1, len(bank) - i):
			if bank[j] > max:
				max = bank[j]
				position = j
		rv += max * 10 ** i
	return rv

	# return centinal * 100 + decimal * 10 + unit * 1

if __name__ == '__main__':
	print(sum(find_joltage(bank) for bank in parse()))
