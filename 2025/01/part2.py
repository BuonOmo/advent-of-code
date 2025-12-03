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

# 1 3 5 6 8 10
print('000 -> dial:50')
with open(argv[1], 'r') as file:
	for i, line in enumerate(file):
		numero = int(line.strip()[1:]) # 5
		if line[0] == 'R':
			count += abs((dial + numero) // 100)
			dial = (dial + numero) % 100
		else:
			count += abs((dial - numero) // 100)
			if dial == 0:
				count -= 1
			dial = (dial - numero) % 100
			if dial == 0:
				count += 1
		# print(f'{i + 1:03d} -> line:{line.strip()} dial:{dial:02d} count:{count}')
	print(count)

# 6291 too low
# 7343 too high
# 6295 Yes
