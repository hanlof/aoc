import sys
import re

print("Day 4: Camp Cleanup")
allinput = open("input04").readlines()

p1ans, p2ans = 0, 0
for i in allinput:
    r = re.search("(\d+)-(\d+),(\d+)-(\d+)", i)
    s1, e1, s2, e2 = map(int, r.groups())
    # part 1: if one range is completely within the other
    if (s1 >= s2 and e1 <= e2) or (s2 >= s1 and e2 <= e1): p1ans += 1
    # part 2: if the ranges overlaps at all (using set() is inefficient but fun :)
    if len(set(range(s1, e1+1)) & set(range(s2, e2+1))) > 0: p2ans += 1

print("Part 1:", p1ans)
print("Part 2:", p2ans)
