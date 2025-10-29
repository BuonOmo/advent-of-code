import fileinput
import re

regex = r"(?P<op>mul|do|don't)\((?P<a>(\d{1,3}),(?P<b>\d{1,3}))?\)"
somme = 0
status = True
for line in fileinput.input():
    matches = re.findall(regex, line)
    print(matches)
    continue
    for a, b, do, dont in matches:
        if do == "do":
            status = True
        elif dont == "don't":
            status = False
        elif status:
            somme += int(a) * int(b)
print(somme)

# solution > 28113672
