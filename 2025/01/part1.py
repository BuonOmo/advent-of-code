#!/usr/bin/env python3

from sys import argv

# L <-> -
# R <-> +

# L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82

dial = 50
count = 0

def next(dial, lettre, numero) -> int:
	if lettre == 'L':
		return (dial - numero)# % 100
	else:
		return (dial + numero)# % 100


with open(argv[1], 'r') as file:
	for line in file:
		lettre = line[0]
		numero = int(line.strip()[1:])
		new = next(dial, lettre, numero)
		print(f'{dial} -> {new}')
		dial = new % 100
		if dial == 0:
			count += 1
	print(count)
