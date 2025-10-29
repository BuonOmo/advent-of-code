import fileinput
from pprint import pp

matrix: list[list[str]] = []

for line in fileinput.input():
	matrix.append(list(line.strip()))

def count_xmas_line(matrix: list[list[str]]) -> int:
	somme = 0
	for l in range(len(matrix)):
		for c in range(len(matrix[l])-3):
			if matrix[l][c]=="X" and matrix[l][c+1]=="M" and matrix[l][c+2]=="A" and matrix[l][c+3]=="S":
				somme += 1
			if matrix[l][c]=="S" and matrix[l][c+1]=="A" and matrix[l][c+2]=="M" and matrix[l][c+3]=="X":
				somme += 1
	return somme

def count_xmas_col(matrix: list[list[str]]) -> int:
	somme = 0
	for l in range(len(matrix)-3):
		for c in range(len(matrix[l])):
			if matrix[l][c]=="X" and matrix[l+1][c]=="M" and matrix[l+2][c]=="A" and matrix[l+3][c]=="S":
				somme += 1
			if matrix[l][c]=="S" and matrix[l+1][c]=="A" and matrix[l+2][c]=="M" and matrix[l+3][c]=="X":
				somme += 1
	return somme

def count_xmas_diag(matrix: list[list[str]]) -> int:
	somme = 0
	for l in range(len(matrix)-3):
		for c in range(len(matrix[l])-3):
			if matrix[l][c]=="X" and matrix[l+1][c+1]=="M" and matrix[l+2][c+2]=="A" and matrix[l+3][c+3]=="S":
				somme += 1
			if matrix[l][c]=="S" and matrix[l+1][c+1]=="A" and matrix[l+2][c+2]=="M" and matrix[l+3][c+3]=="X":
				somme += 1
			if matrix[l][c+3]=="X" and matrix[l+1][c+2]=="M" and matrix[l+2][c+1]=="A" and matrix[l+3][c]=="S":
				somme += 1
			if matrix[l][c+3]=="S" and matrix[l+1][c+2]=="A" and matrix[l+2][c+1]=="M" and matrix[l+3][c]=="X":
				somme += 1
	return somme

# pp(matrix)
pp(count_xmas_line(matrix) + count_xmas_col(matrix) + count_xmas_diag(matrix))
