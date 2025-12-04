#!/usr/bin/env python3

from sys import argv
from pprint import pp

def parse() -> list[list[int]]:
	with open(argv[1], 'r') as file:
		return [[int(c) for c in line.strip()] for line in file]

def find_joltage(bank: list[int]) -> int:
	'''
	>>> find_joltage([int(i) for i in '987654321111111'])
	98
	>>> find_joltage([int(i) for i in '811111111111119'])
	89
	>>> find_joltage([int(i) for i in '234234234234278'])
	78
	>>> find_joltage([int(i) for i in '818181911112111'])
	92
	'''
	decimal = -1
	position = -1
	for i in range(len(bank) - 1):
		if bank[i] > decimal:
			decimal = bank[i]
			position = i

	unit = -1
	for i in range(position + 1, len(bank)):
		if bank[i] > unit:
			unit = bank[i]

	return decimal * 10 + unit

if __name__ == '__main__':
	print(sum(find_joltage(bank) for bank in parse()))
