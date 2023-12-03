import re
lines = open("3").read().splitlines()

class Num():
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val
        self.ispart = False
    def __str__(self):
        return ("<%s: %d %s>" % (str(self.pos), self.val, self.ispart))

tot1 = 0
numbersbypos = dict()
numberslist = list()
partnumbers = list()
adjacent = [(x + y * 1j) for x in [-1, 0, 1] for y in [-1, 0, 1]]

# record all the numbers
for y, l in enumerate(lines):
    for num in re.finditer(r"\d+", l):
        n = Num( num.start() + y * 1j, int(num.group(0)) )
        numberslist.append(n)
        for x in range(*num.span()):
            numbersbypos[ x + y * 1j ] = n
# update all the stored numbers objects with info about being adjacent to a part
for y, l in enumerate(lines):
    for part in re.finditer(r"[^.0123456789]", l):
        for ofs in adjacent:
            num = numbersbypos.get( (part.start() + y * 1j) + ofs )
            if num is not None:
                num.ispart = True
for i in numberslist: # just sum up all the numbers that are part numbers
    if i.ispart:
        tot1 += i.val
tot2 = 0
for y, l in enumerate(lines): # find all the stars
    for part in re.finditer(r"\*", l):
        adjnums = dict()
        for ofs in adjacent: # record all the numbers that are adjacant to this star
            num = numbersbypos.get( (part.start() + y * 1j) + ofs )
            if num:
                adjnums[num.pos] = num.val
        if len(adjnums) == 2: # check the criteria for being a "gear" and update ratio
            ratio = 1
            for val in adjnums.values():
                ratio *= val
            tot2 += ratio


print("Part 1:", tot1)
print("Part 2:", tot2)


# 328174 too low
# 609445 too high

