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

sum = 0

internal_sums: dict[int, int] = {}

for i in range(len(group_a)):
    num = group_a[i]
    if num not in internal_sums:
        internal_sums[num] = group_b.count(num)
    sum += num * internal_sums[num]

print(sum)
