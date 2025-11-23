# !1 = 1
# !2 = 1*2 =2*!1
# !3 = 1*2*3 = 3*!2
# !4 = 1*2*3*4
#

def factoriel (n: int) -> int:
	if n==0:
		return 1

	return n*factoriel(n-1)

print(factoriel(8))
