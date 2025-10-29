import fileinput
from pprint import pp
from collections import defaultdict

ordre: dict[int, list[int]] = defaultdict(list)

def inorder(mylist: list) -> bool:
	for i in range(len(mylist)):
		mylist[i] = int(mylist[i])
		if mylist[i] not in ordre:
			continue
		for j in range(i):
			if mylist[j] in ordre[mylist[i]]:
				return False
	return True

def reorder(mylist: list[int]) -> None:
	for i in range(len(mylist)):
		mylist[i] = int(mylist[i])
		if mylist[i] not in ordre:
			continue
		for j in range(i):
			if mylist[j] in ordre[mylist[i]]:
				mylist[j], mylist[i] = mylist[i], mylist[j]

with fileinput.input() as input:
	for line in input:
		if line =='\n':
			break
		a, b = line.strip().split('|')
		# if int(a) not in ordre:
		# 	ordre[int(a)] = []
		ordre[int(a)].append(int(b))

	sum = 0
	for line in input:
		mylist = line.strip().split(',')
		if inorder(mylist):
			continue
		reorder(mylist)
		sum += mylist[len(mylist)//2]

	pp(sum)
