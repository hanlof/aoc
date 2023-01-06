import sys
import re

inputfile = open("inputdata/input05")
allinput = inputfile.readlines()

p1stacks = [ [], [], [], [], [], [], [], [], [], [] ]
p2stacks = [ [], [], [], [], [], [], [], [], [], [] ]
for line in allinput:
    if line.startswith("["):
        for n in range(1, len(line), 4):
            if line[n] != ' ':
                d = n // 4
                p1stacks[d].insert(0, line[n])
                p2stacks[d].insert(0, line[n])
    elif line.startswith("move"):
        r = re.search("move (?P<howmany>\d+) from (?P<from>\d+) to (?P<to>\d+)", line)
        n, src, dst = int(r['howmany']), int(r['from']) - 1, int(r['to']) - 1
        p1stacks[dst].extend(reversed(p1stacks[src][-n:]))
        del(p1stacks[src][-n:])
        p2stacks[dst].extend(p2stacks[src][-n:])
        del(p2stacks[src][-n:])
print("Part 1:", "".join([s[-1] for s in p1stacks if len(s) > 0]))
print("Part 2:", "".join([s[-1] for s in p2stacks if len(s) > 0]))

