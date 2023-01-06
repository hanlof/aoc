class RockGenerator():
    ROCKS = list([
        [ "       ", "       ", "       ", "  #    ", "       "],
        [ "       ", "   #   ", "    #  ", "  #    ", "       "],
        [ "       ", "  ###  ", "    #  ", "  #    ", "  ##   "],
        [ "  #### ", "   #   ", "  ###  ", "  #    ", "  ##   "]])
    def __init__(s):
        s.rocknum = 0
    def next(s):
        r = s.rocknum
        s.rocknum = (r + 1) % 5
        return [s.ROCKS[0][r], s.ROCKS[1][r], s.ROCKS[2][r], s.ROCKS[3][r]]

class Piece():
    def __init__(s, lines, yline):
        s.coords = set()
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                if lines[y][x] == "#": s.coords.add( (x, yline - y) )
    def movedleft(s):
        return set([(x - 1, y) for x, y in s.coords])
    def movedright(s):
        return set([(x + 1, y) for x, y in s.coords])
    def moveddown(s):
        return set([(x, y - 1) for x, y in s.coords])
    def trymoveleft(s, f):
        newcoord = s.movedleft()
        if min(next(zip(*newcoord))) < 0:
            return False
        for c in newcoord:
            if c in f.rocks: return False
        s.coords = newcoord
        return True
    def trymoveright(s, f):
        newcoord = s.movedright()
        if max(next(zip(*newcoord))) > 6:
            return False
        for c in newcoord:
            if c in f.rocks: return False
        s.coords = newcoord
        return True
    def trymovedown(s, f):
        newcoord = s.moveddown()
        for c in newcoord:
            if c in f.rocks:
                f.stick(s.coords)
                return False
        s.coords = newcoord
        return True
    def move(s, f, movement):
        if "<" == movement:
            p.trymoveleft(f)
        elif ">" == movement:
            p.trymoveright(f)
        else:
            assert False, "Unknown movement %s" % movement.__repr__()

class Field():
    def __init__(s):
        s.rocks = set( map(lambda x: (x, 0), range(7)) )
        s.rgen = RockGenerator()
        s.highest = 0
    def __str__(s):
        return s.lines
    def stick(s, coords):
        s.rocks.update(coords)
        top = 0
        for x, y in coords:
            if y > top: top = y
        if top > s.highest: s.highest = top

def prune(queue):
    possiblejumps = \
        [( 1, 0), (-1, 0), (0, 1)]
    s = 0
    visited = set()
    finalset = set()
    while len(queue) > 0:
        coord = queue.pop()
        if coord in visited:
            continue
        visited.add(coord)
        x = coord[0]
        y = coord[1]
        for trycoord in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if trycoord in f.rocks:
                finalset.add(trycoord)
            elif trycoord[0] >= 0 and trycoord[0] <= 6 \
                    and trycoord[1] <= (f.highest + 1) and not trycoord in visited:
                queue.append(trycoord)
    f.rocks = finalset

allinput = open("inputdata/input17").readline()

import itertools

r = RockGenerator()
f = Field()
movements = iter(itertools.cycle(allinput[:-1]))
for i in range(2022):
    p = Piece(r.next(), f.highest + 7)
    p.move(f, next(movements, None))
    while p.trymovedown(f):
        p.move(f, next(movements, None))
    prune( [ (0, f.highest + 1) ] )

print("Part 1:", f.highest)

r = RockGenerator()
f = Field()
a = dict()
longestdelta = 0
longestiters = 0
movements = iter(itertools.cycle(allinput[:-1]))

INITIALPIECES = 10000
for i in range(INITIALPIECES):
    #    if (i % (len(allinput) - 1)) == 0:
    #        print(len(f.rocks), end=" ")
    #        prune( [ (0, f.highest + 1) ] )
    #        #print(i, f.highest / (i+1), len(f.rocks))
    #        newcombo = (len(f.rocks), r.rocknum)
    #        if newcombo in a:
    #            print("COOL--------------------------", end="")
    #        print(len(f.rocks), r.rocknum)
    #        a[newcombo] = "haoeu"
    prune( [ (0, f.highest + 1) ] )
    newset = tuple(sorted([(x, y - f.highest) for x, y in f.rocks], key=lambda x: x[0] + x[1] * 19001))
    newset = newset + (r.rocknum,)
    if newset not in a:
        if len(newset) < 10:
            print(i, len(a), newset)
        a[newset] = (f.highest, i)
    else:
        height, count = a[newset]
        if i > 3000:
            if f.highest - height > longestdelta: longestdelta = f.highest - height
            if i - count > longestiters: longestiters = i - count
        a[newset] = (f.highest, i)
    p = Piece(r.next(), f.highest + 7)
    p.move(f, next(movements, None))
    while p.trymovedown(f):
        p.move(f, next(movements, None))

ONE_TRILLION = 1000 * 1000 * 1000 * 1000
print(longestiters, longestdelta)
times, remaining = divmod(ONE_TRILLION - INITIALPIECES, longestiters)

for i in range(remaining):
    p = Piece(r.next(), f.highest + 7)
    p.move(f, next(movements, None))
    while p.trymovedown(f):
        p.move(f, next(movements, None))

print("Part 2:", f.highest + times * longestdelta)


