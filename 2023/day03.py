import re

class Num():
    def __init__(self, pos, val): self.pos, self.val, self.ispart = pos, val, False
    def __str__(self): return ("<%s: %d %s>" % (str(self.pos), self.val, self.ispart))

lines = open("3").read().splitlines()
adjacent = {(x + y * 1j) for x in [-1, 0, 1] for y in [-1, 0, 1]} - { (0j) }
numbersbypos, numberslist, partnumbers, ans1, ans2 = dict(), list(), list(), 0, 0

for y, l in enumerate(lines): # record all the numbers
    for num in re.finditer(r"\d+", l):
        n = Num( num.start() + y * 1j, int(num.group(0)) )
        numberslist.append(n)
        for x in range(*num.span()):
            numbersbypos[ x + y * 1j ] = n

for y, l in enumerate(lines): # update numbers adjacency info
    for part in re.finditer(r"[^.0123456789]", l):
        for ofs in adjacent:
            num = numbersbypos.get( (part.start() + y * 1j) + ofs )
            if num and not num.ispart:
                num.ispart = True
                ans1 += num.val

for y, l in enumerate(lines): # find all the gears
    for part in re.finditer(r"\*", l):
        adjnums = dict()
        for ofs in adjacent: # record all the numbers that are adjacant to this star
            num = numbersbypos.get( (part.start() + y * 1j) + ofs )
            if num: adjnums[num.pos] = num.val
        if len(adjnums) == 2: # check the criteria for being a "gear" and update ratio
            ratio = 1
            for val in adjnums.values():
                ratio *= val
            ans2 += ratio

print("Part 1:", ans1)
print("Part 2:", ans2)

# Part 1: 549908
# Part 2: 81166799
