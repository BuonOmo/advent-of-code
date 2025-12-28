#!/usr/bin/env python3

from math import sqrt
from pprint import pp
from sys import argv

type Boite = tuple[int, int, int]


def parse() -> list[Boite]:
	with open(argv[1], 'r') as file:
		boites = []
		for line in file:
			a, b, c = line.split(',')
			boites.append([int(a), int(b), int(c)])
		return boites


def distance(B1: Boite, B2: Boite) -> int:
	"""
	>>> distance([162,817,812], [425,690,689])
	317
	"""
	return round(
		sqrt((B1[0] - B2[0]) ** 2 + (B1[1] - B2[1]) ** 2 + (B1[2] - B2[2]) ** 2)
	)


def pairs_distance(boites: list[Boite]) -> dict:
	distances = {}
	for i in range(len(boites) - 1):
		for b2 in boites[i + 1 :]:
			d = distance(boites[i], b2)
			distances[d] = [boites[i], b2]
	return distances


if __name__ == '__main__':
	boites = parse()
	distances = pairs_distance(boites)
	s = sorted(distances)
	circuits = [[]]
	for i in range(10):
		clé = s[i]
		for j in range(len(circuits)):
			if distances[clé][0] in circuits[j] and distances[clé][1] in circuits[j]:
				# print('1er if', circuits)
				break
			if (
				distances[clé][0] in circuits[j]
				and distances[clé][1] not in circuits[j]
			):
				circuits[j].append(distances[clé][1])
				# print('2eme if', circuits)
				break
			if (
				distances[clé][0] not in circuits[j]
				and distances[clé][1] in circuits[j]
			):
				# print('3eme if', circuits)
				circuits[j].append(distances[clé][0])
				break
		circuits.append([distances[clé][0], distances[clé][1]])
		# print('fin de boucle', circuits)
		i += 1
	sizes = []
	for circuit in circuits:
		if len(circuit) not in sizes:
			sizes.append(len(circuit))
	# l = sorted(sizes)
	s = sorted(sizes, reverse=True)
	pp(circuits)
	pp(s)
	pp(s[0] * s[1] * s[2])
