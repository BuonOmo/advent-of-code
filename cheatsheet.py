# Tableau

tab = [1, 2, 3, 4]
print(tab[1])  # Affiche le deuxième élément du tableau

tab = [[1, 2, 3, 4], [5, 6, 7, 8]]
print(tab[1][1])

def print_table(table):
	for i in range(len(table)):
		print(table[i])
	# ou
	for row in table:
		print(row)

hello = 'Hello'
list_hello = list(hello) # ['H', 'e', 'l', 'l', 'o']

obj = 1
my_list = []
my_list.append(obj)
my_list.push(obj)
print(my_list) # [1, 1]


my=dict()
yours={}
yours == my
my["caca"] = 1
my["prout"] = []
my["prout"].append("foo")
my[yours] = "je sais plus ce que c'est"

# Enclosing scope is a scope that exists only for nested
# functions and is defined by the outer or enclosing
# function. This scope contains the names that you define
# within the enclosing function. The names in the enclosing
# scope are visible from the code of the inner and outer
# functions.
def generate_multiplier(x: int) -> function:
	print(x)
	def inner_function(y: int) -> int:
		print(x, y)
		return x * y
	# print(y) -> NOPE
	return inner_function

times_two = generate_multiplier(2)
times_four = generate_multiplier(4)

print(times_two(3))
print(generate_multiplier(2)(3))


# for (i = 0; i < 10; i++)
for i in range(10):
	if i % 2 == 0:
		continue
	elif i == 5:
		break
	print(i)

# for (i = a; i < b; i+= c)
for i in range(a, b, c):
	print(i)

## Sets

my_set = set()
help(my_set)
help(my_set.add)
my_set.add("foo")
my_set.add("foo")
print(my_set) # {'foo'}


## List comprehension

squares = [x**2 for x in range(10) if x % 2 == 0] # [0, 4, 16, 36, 64]
[i for x in ['foo', 'bar'] for i in x] # ['f', 'o', 'o', 'b', 'a', 'r']

## Enumerate

list(range(len(["foo", "bar"]))) # [0, 1]
list(enumerate(["foo", "bar"])) # [(0, 'foo'), (1, 'bar')]

## String methods

'foo.bar'.split('.') # => ['foo', 'bar']
'.foo.bar'.index('.') # => 0
'.foo.bar'.rindex('.') # => 4
' '.join(['a', 'b']) # => 'a b'


## Slices

tab = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(tab[2:5])  # [2, 3, 4]
print(tab[:5])   # [0, 1, 2, 3, 4]
print(tab[5:])   # [5, 6, 7, 8, 9]
print(tab[-3:])  # [7, 8, 9]
print(tab[:-3])  # [0, 1, 2, 3, 4, 5, 6]
print(tab[::2])  # [0, 2, 4, 6, 8]
print(tab[::-1]) # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


## Math

2 ** 5 # 32
