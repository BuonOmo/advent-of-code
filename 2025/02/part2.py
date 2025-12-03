#!/usr/bin/env python3

from sys import argv
from pprint import pp
from itertools import pairwise

def input() -> str:
	with open(argv[1], 'r') as file:
		for line in file:
			return line.strip()

def parse(input: str) -> list[range]:
	'''
	>>> parse('1-3,5-7')
	[range(1, 4), range(5, 8)]
	'''
	def to_range(group):
		a, b = group.split('-')
		return range(int(a), int(b) + 1)

	return [to_range(group) for group in input.split(',')]

def is_valid(id: int) -> bool:
	'''
	>>> is_valid(221221)
	False
	>>> is_valid(22122)
	True
	>>> is_valid(221222)
	True
	>>> is_valid(222)
	False
	>>> is_valid(212121)
	False
	'''
	id = str(id)
	length = len(id)

	for i in range(1, length // 2 + 1):
		if length % i != 0:
			continue
		same = True
		for j, k in pairwise(range(0, length, i)):
			if id[j:j+i] != id[k:k+i]:
				same = False
				break
		if same:
			return False # invalid
	return True # valid

if __name__ == '__main__':
	input_data = input()
	parsed = parse(input_data)
	count = sum(id
		for r in parsed
		for id in r
		if not is_valid(id))
	# for r in parsed:
	# 	for id in r:
	# 		if not is_valid(id):
	# 			count += id
	pp(count)
