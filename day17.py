import aoc
import itertools
import sys

class RockGenerator():
    ROCKS = list([
        [ "       ", "       ", "       ", "  #    ", "       "],
        [ "       ", "   #   ", "    #  ", "  #    ", "       "],
        [ "       ", "  ###  ", "    #  ", "  #    ", "  ##   "],
        [ "  #### ", "   #   ", "  ###  ", "  #    ", "  ##   "]])
    def __init__(s):
        s.rocknum = 0
        s.binrocks = dict()
        for r in range(5):
            binrock = 0
            for i in range(4):
                binrock <<= 8
                binrock += int("".join(["1" if c == "#" else "0" for c in s.ROCKS[i][r] + "0"]), 2)
                #binrock <<= 1 # leave empty space in rightmost bit
            s.binrocks[r] = binrock
        s.biniter = itertools.cycle(s.binrocks.values())
    def next(s):
        r = s.rocknum
        s.rocknum = (r + 1) % 5
        return [s.ROCKS[0][r], s.ROCKS[1][r], s.ROCKS[2][r], s.ROCKS[3][r]]
    def nextbin(s):
        return next(s.biniter)

class Piece():
    def __init__(s, lines, yline, binrock):
        s.coords = set()
        s.bin = binrock
        s.binylevel = yline
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
        if (s.bin << 1) & 0x101010100: return False
        if f.binrocks[s.binylevel - 0] & ((s.bin >> 23) & 0xff): return False
        if f.binrocks[s.binylevel - 1] & ((s.bin >> 15) & 0xff): return False
        if f.binrocks[s.binylevel - 2] & ((s.bin >> 7) & 0xff): return False
        if f.binrocks[s.binylevel - 3] & ((s.bin << 1) & 0xff): return False
        s.bin <<= 1
        return True
    def trymoveright(s, f):
        if (s.bin >> 1) & 0x01010101: return False
        if f.binrocks[s.binylevel - 0] & ((s.bin >> 25) & 0xff): return False
        if f.binrocks[s.binylevel - 1] & ((s.bin >> 17) & 0xff): return False
        if f.binrocks[s.binylevel - 2] & ((s.bin >> 9) & 0xff): return False
        if f.binrocks[s.binylevel - 3] & ((s.bin >> 1) & 0xff): return False
        s.bin >>= 1
        return True
    def trymovedown(s, f):
        if f.binrocks[s.binylevel - 1] & ((s.bin >> 24) & 0xff):
            f.stickbin(s)
            return False
        if f.binrocks[s.binylevel - 2] & ((s.bin >> 16) & 0xff):
            f.stickbin(s)
            return False
        if f.binrocks[s.binylevel - 3] & ((s.bin >> 8) & 0xff):
            f.stickbin(s)
            return False
        if f.binrocks[s.binylevel - 4] & ((s.bin >> 0) & 0xff):
            f.stickbin(s)
            return False
        s.binylevel -= 1
        return True
    def move(s, f, movement):
        f.updatebinrocks(s.binylevel)
        if "<" == movement:
            p.trymoveleft(f)
        elif ">" == movement:
            p.trymoveright(f)
        else:
            assert False, "Unknown movement %s" % movement.__repr__()

class Field():
    count = 0
    def __init__(s):
        s.rocks = set( map(lambda x: (x, 0), range(7)) )
        s.binrocks = { 0: 0xff }
        s.rgen = RockGenerator()
        s.highest = 0
    def __str__(s):
        return s.lines
    def updatebinrocks(s, ylevel):
        while not ylevel in s.binrocks:
            s.binrocks[ylevel] = 0
            ylevel -= 1
    def stickbin(s, piece):
        s.binrocks[piece.binylevel - 0] |= (piece.bin >> 24) & 0xff
        s.binrocks[piece.binylevel - 1] |= (piece.bin >> 16) & 0xff
        s.binrocks[piece.binylevel - 2] |= (piece.bin >> 8) & 0xff
        s.binrocks[piece.binylevel - 3] |= (piece.bin >> 0) & 0xff
        while s.binrocks[s.highest + 1] != 0:
            s.highest += 1
    def stick(s, coords):
        s.rocks.update(coords)
        top = 0
        for x, y in coords:
            if y > top: top = y
        if top > s.highest: s.highest = top

# find all lines that can be interacted with from above (by new pieces)
def calcactivelines(f):
    possiblejumps = [( 1, 0), (-1, 0), (0, 1)]
    visited = set()
    finalset = set()
    queue = [ (0, 0) ]
    lowest_y = 0
    count = 0
    while len(queue) > 0:
        coord = queue.pop()
        if coord in visited:
            continue
        visited.add(coord)
        x, y = coord
        for dx, dy in possiblejumps:
            x, y = x + dx, y + dy
            if x < 0: continue
            if x > 6: continue
            if (f.highest - y) < 0: continue
            lowest_y = max(lowest_y, y)
            if (0x80 >> x) & f.binrocks[f.highest - y]:
                pass
            elif not (x, y) in visited:
                count += 1
                queue.append((x, y))
    return lowest_y

tim = aoc.Timing("Timing")
allinput = open("inputdata/input17").readline()


r = RockGenerator()
f = Field()
movements = iter(itertools.cycle(allinput[:-1]))
count = 0
savedstates = dict()
keysforstate = list()
heightforstate = list()
prevmatched = False

#for i in range(2022):
matchesinarow = 0
prevlen = 0
samelencount = 0
highestdelta = 0
P1CYCLE = 2022
p1ans = 0
for i in itertools.count():
    activelines_count = calcactivelines(f)
    hashkey = tuple([r.rocknum] + [f.binrocks[f.highest - j] for j in range(activelines_count)])
    if i == P1CYCLE: p1ans = f.highest
    keysforstate.append(hashkey)
    heightforstate.append(f.highest)
    prevkey = savedstates.get(hashkey)
    savedstates[hashkey] = i
    if prevlen == len(savedstates):
        samelencount += 1
    else:
        samelencount = 0
    if samelencount >= len(savedstates):
        delta = i - prevkey
        highestdelta = max(delta, highestdelta)
        temp = 0
        for j in range(i - highestdelta, i):
            if keysforstate[j] != keysforstate[j - highestdelta]:
                break
            temp += 1
        if temp == highestdelta:
            print("first repeated cycle is at", i, "with len", highestdelta, "height diff", heightforstate[i] - heightforstate[i - highestdelta])
            break

    if samelencount >= len(savedstates):
        pass

    prevlen = len(savedstates)

    p = Piece(r.next(), f.highest + 7, r.nextbin())
    p.move(f, next(movements, None))
    while p.trymovedown(f):
        p.move(f, next(movements, None))

print("Part 1:", p1ans)

tim.add("P1")

longestiters = 1740
i = 3922
longestdelta = 2666
tim.add("Find repetition")
ONE_TRILLION = 1000 * 1000 * 1000 * 1000
times, remaining = divmod(ONE_TRILLION - (i), longestiters)

for i in range(remaining):
    p = Piece(r.next(), f.highest + 7, r.nextbin())
    p.move(f, next(movements, None))
    while p.trymovedown(f):
        p.move(f, next(movements, None))

print("Part 2:", f.highest + times * longestdelta)
tim.add("remain")
tim.print()

print(aoc.htmlanswers())


