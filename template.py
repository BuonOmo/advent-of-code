#!/usr/bin/env python3

import fileinput
from pprint import pp

print = pp

for line in fileinput.input():
    print(line.strip())
