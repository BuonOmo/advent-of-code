#!/usr/bin/env python3

from sys import argv
from pprint import pp

def parse() -> tuple[int, list[list[int]]]:
	with open(argv[1], 'r') as file:
		beam = next(file).index('S')
		splitters = [
			[i for i in range(len(line)) if line[i] == '^']
			for line in file
		]
		return beam, splitters

def apply(beams: set[int], splitters: list[int]) -> tuple[set[int], int]:
	'''
	>>> apply([1],[1])
	{0, 2}
	>>> apply([1,3], [1,3])
	{0, 2, 4}
	>>> apply([1], [2])
	{1}
	'''
	new_beams = set()
	count = 0
	for beam in beams:
		if beam in splitters:
			new_beams.update([beam - 1, beam + 1])
			count += 1
		else:
			new_beams.add(beam)
	return new_beams, count

if __name__ == '__main__':
	beam, splitterss = parse()
	beams = {beam}
	sum = 0
	for splitters in splitterss:
		beams, count = apply(beams, splitters)
		sum += count
	pp(sum)
