#!/usr/bin/env python3

from sys import argv
from time import time
from typing import Generator


maybe_int = int|str

def bench(method):
	def fn(*args):
		t0 = time()
		r = method(*args)
		t1 = time()
		print(f'{method.__name__} took {(t1 - t0) * 1_000:.3f} ms')
		return r
	return fn

@bench
def splat(s: str) -> list[maybe_int]:
	'''
	>>> splat('12345')
	[0, '.', '.', 1, 1, 1, '.', '.', '.', '.', 2, 2, 2, 2, 2]
	>>> splat('10' * 11)
	[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	'''
	rv = []
	for i, char in enumerate(s):
		if i%2 == 0: # File
			rv.extend([i//2] * int(char))
		else: # Free space
			rv.extend('.' * int(char))
	return rv

def find_end_group(l: list[maybe_int], end: int|None = None) -> slice|None :
	'''
	>>> find_end_group(['.', 0])
	slice(1, 2, None)
	>>> find_end_group([0, '.', '.', 1])
	slice(3, 4, None)
	>>> find_end_group([0, '.', 1, 2])
	slice(3, 4, None)
	>>> find_end_group([0, '.', 1, 1])
	slice(2, 4, None)
	>>> find_end_group([0, '.', 1, 1], end=2)
	slice(0, 1, None)
	>>> find_end_group('....')
	'''
	if end is None:
		end = len(l)
	# [0, 0], None
	for i in range(end - 1, -1, -1):
		if l[i] != '.':
			for j in range(i, -1, -1):
				if l[j] != l[i]:
					return slice(j + 1, i + 1)
			return slice(0, i + 1)

	return None

def end_groups(l: list[maybe_int]) -> Generator[slice]:
	'''
	>>> list(end_groups('0.11..'))
	[slice(2, 4, None), slice(0, 1, None)]
	'''

	s = find_end_group(l)
	while s is not None:
		yield s
		s = find_end_group(l,s.start)



def find_free_space(l: list[maybe_int], size: int) -> slice[int, int, None]| None:
	'''
	>>> find_free_space('0..2',2)
	slice(1, 3, None)
	>>> find_free_space('0...',3)
	slice(1, 4, None)
	>>> find_free_space('...',3)
	slice(0, 3, None)
	>>> find_free_space('00..1',3)
	>>> find_free_space('123',2)
	'''
	i=0
	while i <= len(l)-size:
		if l[i] == '.':
			run = True
			for j in range(i, i+size):
				if l[j]!='.':
					run = False
					i=j
					break
			# end for
			if run:
				return slice(i,i+size)
		# end if
		i+=1

	return None


# def free_spaces(l: list[maybe_int]) -> Generator[slice]:
# 	'''
# 	>>> list(free_spaces('0..2.3'))
# 	[slice(1, 3, None), slice(4, 5, None)]
# 	>>> list(free_spaces('.0...'))
# 	[slice(0, 1, None), slice(2, 5, None)]
# 	>>> list(free_spaces('...'))
# 	[slice(0, 3, None)]
# 	>>> list(free_spaces('123'))
# 	[]
# 	'''
# 	for i in range(len(l)):
# 		if l[i] == '.':
# 			for j in range(i, len(l)):
# 				if l[j] != '.':
# 					yield slice(i, j)
# 					i = j
# 					break
# 				if j == len(l) - 1:
# 					yield slice(i, len(l))
# 					return

@bench
def fill(l: list[maybe_int]) -> list[maybe_int]:
	'''
	>>> fill([0, '.', 1])
	[0, 1, '.']
	>>> fill(splat('2333133121414131402'))
    '00992111777.44.333....5555.6666.....8888..'
	'''
	for group_slice in end_groups(l): # faudrait faire end_groups par ID décroissant + ça évite qu'on déplace des groupes du débuts sur les espaces vides à la fin
		slice_size = group_slice.stop - group_slice.start
		free_slice = find_free_space(l, slice_size)
		if free_slice:
			l[free_slice], l[group_slice] = l[group_slice], l[free_slice]


	# for index, char in enumerate(l):
	# 	if char != '.':
	# 		continue

	# 	end_index = find_end_group(l)
	# 	if end_index < index:
	# 		break
	# 	l[index], l[end_index] = l[end_index], '.'
	# return l

@bench
def checksum(l: list[maybe_int]) -> int:
	'''
	To calculate the checksum, add up the result of multiplying
	each of these blocks' position with the file ID number it
	contains. The leftmost block is in position 0. If a block
	contains free space, skip it instead.
	'''
	sum = 0
	for index, char in enumerate(l):
		if type(char) is int:
			sum += char * index
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

@bench
def parse() -> str:
	with open(argv[1] if len(argv) > 1 else '2024/09/example', 'r') as file:
		return file.readline().strip()

if __name__ == '__main__':
	# s = '12345'
	# s = parse()
	# l = splat(s)
	# l = fill(l)
	# s = checksum(l)
	# print(s)
	list(free_spaces(list('.0...')))

# 89558806610 -> too low
