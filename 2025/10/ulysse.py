#!/usr/bin/env python3

from sys import argv
from collections import deque
from functools import reduce
from operator import or_

type state = int
type button = list[int]

class Machine:
	def __init__(self, line: str):
		'''
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').final_state
		6
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').buttons
		[[3], [1, 3], [2]]
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').initial_state
		0
		'''
		lights, *buttons, joltage = line.split(' ')
		self.final_state: state = reduce(or_, (1 << i for i, light in enumerate(lights[1:-1]) if light == '#'), 0)
		self.buttons: list[button] = [
			[int(val) for val in button[1:-1].split(',')]
			for button in buttons
		]
		self.initial_state: state = 0


def neighbors(state: state, buttons: list[button]) -> list[state]:
	'''
	>>> neighbors(0b01, [[0], [0, 1], [1]])
	[0, 2, 3]
	'''
	neighbors = []
	for button in buttons:
		new_state = state
		for i in button:
			new_state = new_state ^ (1 << i)
		neighbors.append(new_state)
	return neighbors

def bfs(machine: Machine) -> int:
	queue: deque[tuple[state, int]] = deque([(machine.initial_state, 0)])
	visited: set[state] = {machine.initial_state}

	while queue:
		el, d = queue.popleft()
		if el == machine.final_state:
			return d
		for n in neighbors(el, machine.buttons):
			if n not in visited:
				visited.add(n)
				queue.append((n, d + 1))

	raise ValueError('could not reach final state')





def parse(filename: str | None = None) -> list[Machine]:
	if not filename:
		filename = argv[1]
	with open(filename, 'r') as file:
		return [Machine(line.strip()) for line in file]


if __name__ == '__main__':
	print(sum(bfs(machine) for machine in parse()))
