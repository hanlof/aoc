import sys
import re

print(__file__)

#inputfile = sys.stdin
inputfile = open("input05")
allinput = inputfile.readlines()

stacks = [ [], [], [], [], [], [], [], [], [], [] ]
ans = 0
for i in allinput:
    if i.startswith("["):
        for n in range(1,len(i), 4):
            if i[n] != ' ':
                ans = ans + 1
                d = n // 4
                stacks[d + 1].insert(0, i[n])
    elif i.startswith("move"):
        r = re.search("move (\d+) from (\d+) to (\d+)", i)
        n = int(r[1])
        f = stacks[int(r[2])]
        t = stacks[int(r[3])]
        for slask in range(0, n):
            t.append(f.pop())

for i in stacks:
    if len(i) > 0:
        print(i[-1])

stacks = [ [], [], [], [], [], [], [], [], [], [] ]
ans = 0
for i in allinput:
    if i.startswith("["):
        for n in range(1,len(i), 4):
            if i[n] != ' ':
                ans = ans + 1
                d = n // 4
                stacks[d + 1].insert(0, i[n])
    elif i.startswith("move"):
        r = re.search("move (\d+) from (\d+) to (\d+)", i)
        n = int(r[1])
        f = stacks[int(r[2])]
        t = stacks[int(r[3])]
        tmp = []
        for slask in range(0, n):
            tmp.insert(0, f.pop())
        for tmp2 in tmp:
            t.append(tmp2)
print("----")
for i in stacks:
    if len(i) > 0:
        print(i[-1])

