import fileinput
from time import sleep
from cursed import Cursed

def creerlesobstacles(tableau) -> list[list[bool]]:
	return [[cell == '#' for cell in row] for row in tableau]

def trouverlamadame(tableau) -> tuple[int, int]:
	for i, row in enumerate(tableau):
		for j, cell in enumerate(row):
			if cell == '^':
				return (i, j)
	raise ValueError("No '^' found in the tableau")

def update(state):
	dir = state['direction']
	obstacles = state['obstacles']
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
	if obstacles[new_x][new_y]:
		dir = directions[(directions.index(dir) + 1) % len(directions)]
	else:
		x, y = new_x, new_y
	return {
		'direction': dir,
		'position': (x, y),
		'size': state['size'],
		'obstacles': obstacles,
	}

def show(state, display):
	s = ''
	for i in range(state['size'][0]):
		for j in range(state['size'][1]):
			if state['obstacles'][i][j]:
				s += '#'
			elif state['position'] == (i, j):
				s += '^'
			else:
				s += '.'
		s += '\n'
	display.print_grid(s, state['position'])
	# display.pp(state)
	sleep(0.1)

with Cursed() as c:
	def print(obj):
		c.pp(obj)
		sleep(0.7)
	tableau: list[list[str]] = []
	#s = ''.join(fileinput.input())

	for line in fileinput.input():
		tableau.append(list(line.strip()))

	state = {
		'direction': 'up',
		'position': trouverlamadame(tableau),
		'obstacles': creerlesobstacles(tableau),
		'size': (len(tableau), len(tableau[0]))
	}

	while True:
		state = update(state)
		show(state, c)

	print(state)



	sleep(100)
