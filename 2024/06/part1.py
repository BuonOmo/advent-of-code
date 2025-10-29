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
	if dir == 'up':
		if obstacles[x - 1][y]:
			x, y = x, y + 1
			dir = 'right'
		else:
			x, y = x - 1, y
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
	sleep(0.05)

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
