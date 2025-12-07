#!/usr/bin/env python3

from sys import argv

def parse() -> tuple[int, list[list[int]]]:
	with open(argv[1], 'r') as file:
		beam = next(file).index('S')
		splitters = [
			[i for i in range(len(line)) if line[i] == '^']
			for line in file
		]
		return beam, splitters

def explore(splitterss: list[list[int]], beam: int, depth: int, mem: dict) -> int:
	if depth == len(splitterss):
		return 1
	key = (beam, depth)
	if key in mem:
		return mem[key]

	rv = 0
	if beam in splitterss[depth]:
		rv = explore(splitterss, beam - 1, depth + 1, mem) + explore(splitterss, beam + 1, depth + 1, mem)
	else:
		rv = explore(splitterss, beam, depth + 1, mem)

	mem[key] = rv
	return rv



if __name__ == '__main__':
	beam, splitterss = parse()
	mem = dict()
	print(explore(splitterss, beam, 0, mem))
