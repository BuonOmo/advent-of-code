# fib(0): 1
# fib(1): 1
# fib(2): 2
# fib(3): 3 -> 2 + 1 -> fib(2) + fib(1)
# 1 1 2 3 5 8 13 21 34 55 89
# definition: la somme des deux derniers élements
#
# fib(n) = fib(n - 1) + fib(n - 2)

import time
from typing import Callable


def badfib(n: int):
	if n == 1 or n == 0:
		return 1

	return badfib(n-1) + badfib(n-2)

def betterfib(n: int, mem: dict[int, int] = {1: 1, 0: 1}) -> int:
	if n in mem:
		return mem[n]

	mem[n] = betterfib(n - 1) + betterfib(n - 2)
	return mem[n]

def bestfib(n: int) -> int:
	a, b = 1, 1

	for _ in range(n - 2):
		a, b = b, a + b

	return b

def bench(n: int, fn: Callable[[int], int]):
	t0 = time.time()
	_result = fn(n)
	t1 = time.time()
	print(f'{fn.__name__} took {t1 - t0:3f} seconds')

bench(35, badfib)
bench(35, betterfib)
bench(35, bestfib)
