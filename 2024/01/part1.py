#!/usr/bin/env python3

import fileinput

my_list: list[list[int]] = list()

for line in fileinput.input():
    my_list.append(list(map(lambda x: int(x), line.split())))


group_a: list[int] = list()
group_b: list[int] = list()

group_a = [a for (a, _) in my_list]
group_b = [b for (_, b) in my_list]


# print(group_a)
# print(group_b)

group_a = sorted(group_a)
group_b = sorted(group_b)

sum = 0

for i in range(len(group_a)):
    sum += abs(group_a[i] - group_b[i])

print(sum)
