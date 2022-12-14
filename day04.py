import sys
import re

print(__file__)

#inputfile = sys.stdin
inputfile = open("input04")
allinput = inputfile.readlines()

ans = 0
for i in allinput:
    r = re.search("(\d+)-(\d+),(\d+)-(\d+)", i)
    s1 = int(r[1])
    e1 = int(r[2])
    s2 = int(r[3])
    e2 = int(r[4])
    if (s1 >= s2 and e1 <= e2): score = 1
    elif (s2 >= s1 and e2 <= e1): score = 1
    else: score = 0
    ans = ans + score
    print(s1, e1, s2, e2, score)

print("Part 1:", ans)

ans = 0
for i in allinput:
    r = re.search("(\d+)-(\d+),(\d+)-(\d+)", i)
    s1 = int(r[1])
    e1 = int(r[2])
    s2 = int(r[3])
    e2 = int(r[4])
    if len(set(range(s1, e1+1)) & set(range(s2, e2+1))) > 0: score = 1
    else: score = 0
    ans = ans + score
    print(s1, e1, s2, e2, score)

print("Part2:", ans)
