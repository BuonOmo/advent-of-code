#!/usr/bin/env python3

from sys import argv
from time import time

def splat(s: str) -> str:
	'''
	>>> splat('12345')
	'0..111....22222'
	>>> splat('10' * 11)
	'012345678910'
	'''
	rv = ''
	for i, char in enumerate(s):
		if i%2 == 0: # File
			rv += str(i//2) * int(char)
		else: # Free space
			rv += '.' * int(char)
	return rv

def find_end_index(l: list[str]) -> int:
	'''
	>>> find_end_index('0..1')
	3
	>>> find_end_index('0.1.')
	2
	>>> find_end_index('....')
	Traceback (most recent call last):
	ValueError: Y avait que des points
	'''
	for index in range(len(l) - 1, -1, -1):
		if l[index] != '.':
			return index
	raise ValueError('Y avait que des points')

def fill(s: str) -> str:
	'''
	>>> fill('0..111....22222')
	'022111222......'
	'''
	l = list(s)
	for index, char in enumerate(l):
		if char != '.':
			continue

		end_index = find_end_index(l)
		if end_index < index:
			break
		l[index], l[end_index] = l[end_index], '.'
	return ''.join(l)

def checksum(s: str) -> int:
	'''
	To calculate the checksum, add up the result of multiplying
	each of these blocks' position with the file ID number it
	contains. The leftmost block is in position 0. If a block
	contains free space, skip it instead.
	'''
	sum = 0
	for index, char in enumerate(s):
		if char != '.':
			sum += int(char) * index
	return sum


# 1. parse
#    12345
# 2. splat
#    0..111....22222
# 3. fill
#    0..111....22222
#    02.111....2222.
#    022111....222..
#    0221112...22...
#    02211122..2....
#    022111222......
# 4. checksum
#    ...


def parse() -> str:
	with open(argv[1] if len(argv) > 1 else '2024/09/example', 'r') as file:
		return file.readline().strip()

def bench(method, *args):
	t0 = time()
	r = method(*args)
	t1 = time()
	print(f'{method.__name__} took {(t1 - t0) * 1_000:.3f} ms')
	return r

if __name__ == '__main__':
	# s = '12345'
	s = bench(parse)
	s = bench(splat, s)
	s = bench(fill, s)
	s = bench(checksum, s)
	print(s)

# 89558806610 -> too low
