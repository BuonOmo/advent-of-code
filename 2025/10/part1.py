#!/usr/bin/env python3

from collections import deque
from pprint import pp
from sys import argv

type state = list[bool]
type button = list[int]


class Machine:
	def __init__(self, line: str):
		"""
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').final_state
		[False, True, True, False]
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').buttons
		[[3], [1, 3], [2]]
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').initial_state
		[False, False, False, False]
		"""
		lights, *buttons, joltage = line.split(' ')
		self.final_state: state = [light == '#' for light in lights[1:-1]]
		self.buttons: list[button] = [
			[int(val) for val in button[1:-1].split(',')] for button in buttons
		]
		self.initial_state: state = [False] * len(self.final_state)


def joli(state: state) -> str:
	return ''.join('#' if a else '.' for a in state)


def neighbors(state: state, buttons: list[button]) -> list[state]:
	"""
	>>> neighbors([False, True], [[0], [0, 1], [0, 1]])
	[[True, True], [True, False], [True, False]]
	"""
	neighbors = []
	for button in buttons:
		new_state = state[:]
		for i in button:
			new_state[i] = not state[i]
		neighbors.append(new_state)
	return neighbors


def bfs(machine: Machine) -> dict:
	q = deque()
	visited = {joli(machine.initial_state)}
	q.append(machine.initial_state)
	parents = {}
	while q:
		v = q.popleft()
		if v == machine.final_state:
			return parents
		for w in neighbors(v, machine.buttons):
			jw = joli(w)
			if jw not in visited:
				visited.add(jw)
				parents[jw] = joli(v)
				q.append(w)
	raise ValueError('Final state not accessible')


def genealogy(machine: Machine, parents: dict[str, str]) -> int:
	state = joli(machine.final_state)
	rv = 0
	while state in parents:
		state = parents[state]
		rv += 1
	return rv


def parse(filename: str | None = None) -> list[Machine]:
	if not filename:
		filename = argv[1]
	with open(filename, 'r') as file:
		return [Machine(line.strip()) for line in file]


if __name__ == '__main__':
	machines = parse('example')
	print(sum(genealogy(machine, bfs(machine)) for machine in machines))
