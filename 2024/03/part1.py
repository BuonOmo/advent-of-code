import fileinput
import re

somme = 0
regex = r"mul\((\d{1,3}),(\d{1,3})\)"

str = ""
for line in fileinput.input():
    print(repr(line))
    str += line.strip()
    print(repr(line.strip()))

matches = re.findall(regex, str)
for a, b in matches:
    somme += int(a) * int(b)

print(somme)

# solution > 28113672
