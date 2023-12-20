import aoc

def checkmirror(n1, n2, p):
    r = range(len(p))
    for i in itertools.count(1):
        if n1 - i not in r or n2 + i not in r:
            return True
        if p[n1 - i] != p[n2 + i]:
            return False
    return True

def findmirror(p):
    for (n1, l1), (n2, l2) in itertools.pairwise(enumerate(p)):
        if l1 == l2:
            if checkmirror(n1, n2, p): return n2

ans1 = 0
for pattern in aoc_sections:
    v = findmirror(pattern)
    h = findmirror(list(zip(*pattern)))
    if v: ans1 += v * 100
    if h: ans1 += h

print("Part 1:", ans1)

def checkalmost(n1, n2, p, mismatch):
    r = range(len(p))
    for i in itertools.count(1):
        if n1 - i not in r or n2 + i not in r:
            return mismatch == 1
        mismatch += sum([c1 != c2 for c1, c2 in zip(p[n1 - i], p[n2 + i])])
        if mismatch > 1: return False
    return mismatch == 1

def findalmost(p):
    mismatch = 0
    for (n1, l1), (n2, l2) in itertools.pairwise(enumerate(p)):
        mismatch = sum([c1 != c2 for c1, c2 in zip(l1, l2)])
        if mismatch <= 1:
            if checkalmost(n1, n2, p, mismatch):
                print(n2)
                for apa in p:
                    print(apa)
                return n2
ans2 = 0
for pattern in aoc_sections:
    v = findalmost(pattern)
    h = findalmost(list(zip(*pattern)))
    if v: ans2 += v * 100
    if h: ans2 += h

print(ans2)
# 36358 too high
