#!/usr/bin/env python3

from sys import argv

def parse(filename: str | None = None) -> ...:
	if not filename:
		filename = argv[1]
	with open(filename, 'r') as file:
		for line in file:
			return line.strip()
