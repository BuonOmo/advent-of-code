from pprint import pp


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

def find_suspect(visited: list[tuple[int, int]]) -> tuple[int, int] | None:
	if len(visited) < 3:
		return None

	a, b, c = visited[-3:]

	if a[0] == b[0]:
		return (c[0], a[1])
	else:
		return (a[0], c[1])


def detect_obstacle(
	a: tuple[int, int], b: tuple[int, int], obstacles: list[list[bool]]
) -> bool:
	if a[0] == b[0]:
		for i in range(min(a[1], b[1]), max(a[1], b[1])):
			if obstacles[a[0]][i]:
				return True
	else:
		for i in range(min(a[0], b[0]), max(a[0], b[0])):
			if obstacles[i][a[1]]:
				return True
	return False


def update(state):
	dir = state['direction']
	obstacles = state['obstacles']
	running = state['running']
	visited = state['visited']
	count = state['count']
	x, y = state['position']

	suspect = find_suspect(state['visited'])

	if (x, y) == suspect and not detect_obstacle(suspect, visited[-3], obstacles):
		count += 1
		pp(suspect)

	vectors = {
		'up': (-1, 0),
		'right': (0, 1),
		'down': (1, 0),
		'left': (0, -1),
	}
	directions = ['up', 'right', 'down', 'left']
	new_x = x + vectors[dir][0]
	new_y = y + vectors[dir][1]
	if not (0 <= new_x < state['size'][0] and 0 <= new_y < state['size'][1]):
		running = False
	elif obstacles[new_x][new_y]:
		dir = directions[(directions.index(dir) + 1) % len(directions)]
		visited.append((x, y))
	else:
		x, y = new_x, new_y
	return {
		'count': count,
		'running': running,
		'direction': dir,
		'position': (x, y),
		'size': state['size'],
		'obstacles': obstacles,
		'visited': visited,
	}

tableau: list[list[str]] = []

with open('example') as file:
	for line in file:
		tableau.append(list(line.strip()))

first_x, first_y = trouverlamadame(tableau)
obstacles = creerlesobstacles(tableau)
visited = []
if obstacles[first_x][first_y - 1]:
	visited.append((first_x, first_y))

state = {
	'count': 0,
	'running': True,
	'direction': 'up',
	'position': (first_x, first_y),
	'obstacles': obstacles,
	'size': (len(tableau), len(tableau[0])),
	'visited': visited,
}

while state['running']:
	state = update(state)


def nwise(iterable, n):
	iterator = iter(iterable)
	l = [next(iterator) for _ in range(n - 1)]
	for x in iterator:
		yield l + [x]
		l = l[1:] + [x]


# pp(state)
# count = 0
# size = state['size']
# pp(list(nwise(state['visited'], 3)))
# for a,b,c in nwise(state['visited'], 3):
# 	def check(x):
# 		return a[x] == b[x] or b[x] == c[x]

# 	if check(0) and check(1):

# 		count += 1


print(state['count'])
