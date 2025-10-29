import fileinput
from pprint import pp
from collections import defaultdict

ordre: dict[int, list[int]] = defaultdict(list)

def inorder(mylist: list) -> int:
	for i in range(len(mylist)):
		mylist[i] = int(mylist[i])
		if mylist[i] not in ordre:
			continue
		for j in range(i):
			if mylist[j] in ordre[mylist[i]]:
				return 0
	return mylist[len(mylist)//2]

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
		sum +=inorder(mylist)
	pp(sum)
