#!/usr/bin/env python3
from copy import deepcopy
from pprint import pp
from time import sleep
import sys

from cursed import Cursed


def interact():
	import code

	code.InteractiveConsole(locals=globals()).interact()


def creerlesobstacles(tableau) -> list[list[bool]]:
	return [[cell == '#' for cell in row] for row in tableau]


def trouverlamadame(tableau) -> tuple[int, int]:
	"""
	Trouve la madame dans le tableau et retourne sa position
	"""
	for i, row in enumerate(tableau):
		for j, cell in enumerate(row):
			if cell == '^':
				return (i, j)
			elif cell not in ['#', '.']:
				raise ValueError(f"Unknown character '{cell}'")
	raise ValueError("No '^' found in the tableau")


# (6,4)(6,6)(7,6)(8,2)(8,4)(8,7)


def reset(state):
	x, y = state['backup']['position']
	state['obstacles'][x][y] = False
	return state | {
		'direction': state['backup']['direction'],
		'position': (x, y),
		'backup': None,
		'deja_vue': set(),
	}



def update(state):
	dir = state['direction']
	obstacles = state['obstacles']
	running = state['running']
	backup = state['backup']
	x, y = state['position']
	deja_vue = state['deja_vue']

	vectors = {
		'up': (-1, 0),
		'right': (0, 1),
		'down': (1, 0),
		'left': (0, -1),
	}
	directions = ['up', 'right', 'down', 'left']
	new_x = x + vectors[dir][0]
	new_y = y + vectors[dir][1]

	if not (
		0 <= new_x < state['size'][0] and 0 <= new_y < state['size'][1]
	):  # La madame sort
		if backup is None:
			running = False
		else: # Simulation
			return reset(state)
	elif obstacles[new_x][new_y]:  # La madame trouve un obstacle
		if backup is not None: # Simulation
			if (x, y, dir) in deja_vue: # Ça boucle peut-être
				state['looping'].add(state['backup']['position'])
				return reset(state)
			else:
				deja_vue.add((x, y, dir))
				dir = directions[(directions.index(dir) + 1) % len(directions)]
		else:
			dir = directions[(directions.index(dir) + 1) % len(directions)]
	else:  # La madame peut avancer
		if backup is None and (new_x, new_y) not in state['visited']:  # On rajoute l'obstacle
			backup = {
				'direction': dir,
				'position': (new_x, new_y),
			}
			obstacles[new_x][new_y] = True
			state['visited'].add((new_x, new_y))
			dir = directions[(directions.index(dir) + 1) % len(directions)]
		else: # Simulation
			x, y = new_x, new_y

	return state | {
		'running': running,
		'direction': dir,
		'position': (x, y),
		'obstacles': obstacles,
		'backup': backup,
		'deja_vue': deja_vue,
	}


tableau: list[list[str]] = []

with open(sys.argv[1] if len(sys.argv) > 1 else 'input') as file:
	for line in file:
		tableau.append(list(line.strip()))

pos = trouverlamadame(tableau)
state = {
	'looping': set(),
	'running': True,
	'direction': 'up',
	'position': pos,
	'obstacles': creerlesobstacles(tableau),
	'size': (len(tableau), len(tableau[0])),
	'backup': None,  # direction, position, obstacles
	'deja_vue': set(),
	'visited': set([pos]),
}

should_show = {
	'enabled': False,
	'quit': False,
	'current': None
}

def show(state, display):
	global should_show
	if not should_show['enabled']:
		if state['backup'] is None:
			return
		if  should_show['quit'] and should_show['current'] == state['backup']['position']:
			return
		a = state['backup']['position'] == (86, 21) and state['backup']['direction'] != 'right'
		b = state['backup']['position'] == (86, 35) and state['backup']['direction'] != 'right'
		if not (a or b):
			return
		should_show['current'] = state['backup']['position']
		should_show['enabled'] = True

	s = ''
	for i in range(state['size'][0]):
		for j in range(state['size'][1]):
			if state['obstacles'][i][j]:
				s += '#'
			elif state['position'] == (i, j):
				s += {'up': '^', 'right': '>', 'down': 'v', 'left': '<'}[
					state['direction']
				]
			else:
				s += '.'
		s += '\n'
	display.print_grid(s, state['position'])
	display.pp(state | {'looping': len(state['looping']), 'obstacles': '...', 'visited': '...'})
	if display.getch() == 113: # q
		should_show['quit'] = True
	# sleep(1 if state['backup'] is None else 0.1)


#with Cursed() as c:
total_steps = 6024
steps = 0
prout = True
while state['running']:
	if state['backup'] is None:
		steps += 1
	# print(f"Progress: {100 * steps / total_steps:.2f}% ({steps})\r", end='')
	# c.pp(f"Progress: {100 * steps / total_steps:.2f}% ({steps})")
	state = update(state)
	# c.pp({ 'looping': state['looping'], 'deja_vue': state['deja_vue'], 'sim': state['backup'] is not None })
	# show(state, c)


def nwise(iterable, n):
	iterator = iter(iterable)
	l = [next(iterator) for _ in range(n - 1)]
	for x in iterator:
		yield l + [x]
		l = l[1:] + [x]

print()
# print(state['looping'])
print(len(state['looping']))
