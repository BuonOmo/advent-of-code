#!/usr/bin/env python3

from pprint import pp
from sys import argv

def test(result: int, op: list[int]) -> bool:
	if len(op) == 1:
		return result == op[0]
	a, b, *rest = op
	return test(result, [a * b, *rest]) or test(result, [a + b, *rest])


with open(argv[1], "r") as f:
	count=0
	for line in f:
		a, b = line.strip().split(': ')
		a = int(a)
		b = [int(x) for x in b.split(' ')]
		# a, *b = [int(x) for x in re.split(r'[^\d]+', line.strip())]
		print(repr(a),repr(b))
		if test(a,b):
			count += a
	print(count)
