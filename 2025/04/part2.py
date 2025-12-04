#!/usr/bin/env python3

from sys import argv
from time import sleep

type matrix = list[list[bool]]

def parse() -> matrix:
	with open(argv[1], 'r') as file:
		return [
			[char == '@' for char in line.strip()]
			for line in file
		]

def is_accessible(matrix: matrix, row: int, col: int) -> bool:
	'''
	>>> is_accessible([[True, True, True], [True, True, True], [True, True, True]], 1, 1)
	False
	>>> is_accessible([[True, True, False], [True, True, False], [False, False, False]], 1, 1)
	True
	'''
	count = 0
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			if i == 0 and j == 0:
				continue
			if not 0 <= row + i < len(matrix):
				continue
			if not 0 <= col + j < len(matrix[0]):
				continue
			if matrix[row + i][col + j]:
				count += 1
	return count < 4

def show(matrix: matrix):
	print('\033[H', end='')
	rows = len(matrix_)
	cols = len(matrix_[0])
	for row in range(rows):
		for col in range(cols):
			if not matrix[row][col]:
				print('.', end='')
			elif is_accessible(matrix, row, col):
				print('x', end='')
			else:
				print('@', end='')
		print()


if __name__ == '__main__':
	matrix_ = parse()
	rows = len(matrix_)
	cols = len(matrix_[0])
	count = 0

	while True:
		to_remove=set()
		for row in range(rows):
			for col in range(cols):
				if matrix_[row][col] and is_accessible(matrix_, row, col):
					count += 1
					to_remove.add((row,col))
		for (row, col) in to_remove:
			matrix_[row][col]=False
		show(matrix_)
		sleep(0.1)
		if not to_remove:
			break

	print(count)
