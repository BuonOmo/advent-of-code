# fib(0): 1
# fib(1): 1
# fib(2): 2
# fib(3): 3 -> 2 + 1 -> fib(2) + fib(1)
# 1 1 2 3 5 8 13 21 34 55 89
# definition: la somme des deux derniers élements
#
# fib(n) = fib(n - 1) + fib(n - 2)

def fib(n: int) -> int:
	if n == 0:
		return 1
	if n == 1:
		return 1

	return fib(n - 1) + fib(n - 2)

print(fib(4))
