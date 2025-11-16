from copy import deepcopy
from pprint import pp
from time import sleep

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


def update(state):
	dir = state['direction']
	obstacles = state['obstacles']
	running = state['running']
	count = state['count']
	backup = state['backup']
	x, y = state['position']

	vectors = {
		'up': (-1, 0),
		'right': (0, 1),
		'down': (1, 0),
		'left': (0, -1),
	}
	directions = ['up', 'right', 'down', 'left']
	new_x = x + vectors[dir][0]
	new_y = y + vectors[dir][1]

	# TODO: detecter la boucle.
	# TODO: la faire avancer de 1 une fois le test passé.

	if not (
		0 <= new_x < state['size'][0] and 0 <= new_y < state['size'][1]
	):  # La madame sort
		if backup is None:
			running = False
		else:
			dir = backup['direction']
			x, y = backup['position']
			obstacles = backup['obstacles']
			backup = None
	elif obstacles[new_x][new_y]:  # La madame trouve un obstacle
		if (
			backup is not None
			and (new_x, new_y) == backup['position']
			and dir == backup['direction']
		):  # Ça boucle
			count += 1
			obstacles = backup['obstacles']
			x, y = backup['position']
			backup = None
		else:
			dir = directions[(directions.index(dir) + 1) % len(directions)]
	else:  # La madame peut avancer
		if backup is None:  # On rajoute l'obstacle
			backup = {
				'direction': dir,
				'position': (new_x, new_y),
				'obstacles': deepcopy(obstacles),
			}
			obstacles[new_x][new_y] = True
			dir = directions[(directions.index(dir) + 1) % len(directions)]
		else:
			x, y = new_x, new_y

	return {
		'count': count,
		'running': running,
		'direction': dir,
		'position': (x, y),
		'size': state['size'],
		'obstacles': obstacles,
		'backup': backup,
	}


tableau: list[list[str]] = []

with open('example') as file:
	for line in file:
		tableau.append(list(line.strip()))


state = {
	'count': 0,
	'running': True,
	'direction': 'up',
	'position': trouverlamadame(tableau),
	'obstacles': creerlesobstacles(tableau),
	'size': (len(tableau), len(tableau[0])),
	'backup': None,  # direction, position, obstacles
}


def show(state, display):
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
	display.pp(state['count'])
	sleep(0.1 if state['backup'] is None else 0.01)


with Cursed() as c:
	while state['running']:
		state = update(state)
		show(state, c)


def nwise(iterable, n):
	iterator = iter(iterable)
	l = [next(iterator) for _ in range(n - 1)]
	for x in iterator:
		yield l + [x]
		l = l[1:] + [x]


print(state['count'])
