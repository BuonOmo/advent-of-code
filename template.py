#!/usr/bin/env python3

from sys import argv

def parse() -> ...:
	with open(argv[1], 'r') as file:
		for line in file:
			return line.strip()
