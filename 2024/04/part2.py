import fileinput
from pprint import pp

matrix: list[list[str]] = []

for line in fileinput.input():
	matrix.append(list(line.strip()))



def count_xmas_diag(matrix: list[list[str]]) -> int:
	somme = 0
	for l in range(len(matrix)-2):
		for c in range(len(matrix[l])-2):
			# M.S
			# .A.
			# M.S
			if matrix[l][c]=="M" and matrix[l+1][c+1]=="A" and matrix[l+2][c+2]=="S" and matrix[l][c+2]=="M" and matrix[l+2][c]=="S":
				somme += 1
			# M.M
			# .A.
			# S.S
			if matrix[l][c]=="M" and matrix[l+1][c+1]=="A" and matrix[l+2][c+2]=="S" and matrix[l][c+2]=="S" and matrix[l+2][c]=="M":
				somme += 1
			# S.M
			# .A.
			# S.M
			if matrix[l][c]=="S" and matrix[l+1][c+1]=="A" and matrix[l+2][c+2]=="M" and matrix[l][c+2]=="M" and matrix[l+2][c]=="S":
				somme += 1
			# S.S
			# .A.
			# M.M
			if matrix[l][c]=="S" and matrix[l+1][c+1]=="A" and matrix[l+2][c+2]=="M" and matrix[l][c+2]=="S" and matrix[l+2][c]=="M":
				somme += 1
	return somme

# pp(matrix)
pp(count_xmas_diag(matrix))
