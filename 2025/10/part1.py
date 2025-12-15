#!/usr/bin/env python3

from sys import argv

type state = list[bool]
type button = list[int]

class Machine:
	def __init__(self, line: str):
		'''
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').final_state
		[False, True, True, False]
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').buttons
		[[3], [1, 3], [2]]
		>>> Machine('[.##.] (3) (1,3) (2) {3,5,4,7}').initial_state
		[False, False, False, False]
		'''
		lights, *buttons, joltage = line.split(' ')
		self.final_state: state = [light == '#' for light in lights[1:-1]]
		self.buttons: list[button] = [
			[int(val) for val in button[1:-1].split(',')]
			for button in buttons
		]
		self.initial_state: state = [False] * len(self.final_state)


def neighbors(state: state, buttons: button) -> list[state]:
	'''
	>>> neighbors([False, True], [[0], [0, 1], [0, 1]])
	[[True, True], [True, False], [True, False]]
	'''
	neighbors = []
	for button in buttons:
		new_state = state[:]
		for i in button:
			new_state[i] = not state[i]
		neighbors.append(new_state)
	return neighbors

def explore(machine: Machine, state: state, mem: dict[state, int] = {}) -> int:
	if state == machine.final_state:
		return 0
	if state in mem:
		return mem[state]

	mem[state] = min(
		explore(machine, neighbor, mem) + 1
		for neighbor in neighbors(state, machine.buttons)
	)
	return mem[]




def parse(filename: str | None = None) -> list[Machine]:
	if not filename:
		filename = argv[1]
	with open(filename, 'r') as file:
		return [Machine(line.strip()) for line in file]


if __name__ == '__main__':
	machines = parse()
	for machine in machines:
		explore(machine, machine.initial_state)
