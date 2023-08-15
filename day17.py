import aoc

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
            s.binrocks[r] = binrock
        s.biniter = itertools.cycle(s.binrocks.values())
    def nextbin(s):
        return next(s.biniter)

class Piece():
    def __init__(s, yline, binrock):
        s.bin = binrock
        s.binylevel = yline
    def trymovedown(s, f):
        if f.binrocks[s.binylevel - 3] & ((s.bin >> 8) & 0xff):
            f.stickbin(s)
            return False
        if f.binrocks[s.binylevel - 4] & ((s.bin >> 0) & 0xff):
            f.stickbin(s)
            return False
        s.binylevel -= 1
        return True
    def movex(s, f, moveop):
        while len(f.binrocks) < s.binylevel + 1:
            f.binrocks.append(0)
        t = moveop(s.bin)
        if t & 0x101010101: return False
        if f.binrocks[s.binylevel - 0] & ((t >> 24) & 0xff): return False
        if f.binrocks[s.binylevel - 1] & ((t >> 16) & 0xff): return False
        if f.binrocks[s.binylevel - 2] & ((t >> 8) & 0xff): return False
        if f.binrocks[s.binylevel - 3] & ((t >> 0) & 0xff): return False
        s.bin = t

class Field():
    count = 0
    def __init__(s):
        s.rocks = set( map(lambda x: (x, 0), range(7)) )
        s.binrocks = [ 0xfe, 0x00 ]
        s.activelines = dict(enumerate(s.binrocks))
        s.rgen = RockGenerator()
        s.highest = 0
        s.piece = None
    def __str__(s):
        return s.lines
    def stickbin(s, piece):
        s.binrocks[piece.binylevel - 0] |= (piece.bin >> 24) & 0xff
        s.binrocks[piece.binylevel - 1] |= (piece.bin >> 16) & 0xff
        s.binrocks[piece.binylevel - 2] |= (piece.bin >> 8) & 0xff
        s.binrocks[piece.binylevel - 3] |= (piece.bin >> 0) & 0xff
        while s.binrocks[s.highest + 1] != 0:
            s.highest += 1
    def newpiece(s):
        s.piece = Piece(f.highest + 7, s.rgen.nextbin())
        return s.piece

# pass the rocknum just so it can be yielded to the hash function
def yfindit(f, rocknum):
    a = f.binrocks[f.highest - 1] ^ 0xfe
    line = f.highest
    yield rocknum
    for i in range(2):
        if len(f.binrocks) < i: continue
        yield f.binrocks[f.highest - i]
    return
    while a != 0:
        notr = 0xfe ^ f.binrocks[line]
        l = a & notr; r = a & notr
        # do the same thing 4 times without a loop. (unrolled loop is faster)
        l = ((l << 1) | a) & notr; r = ((r >> 1) | a) & notr
        l = ((l << 1) | a) & notr; r = ((r >> 1) | a) & notr
        l = ((l << 1) | a) & notr; r = ((r >> 1) | a) & notr
        l = ((l << 1) | a) & notr; r = ((r >> 1) | a) & notr
        a = l | r
        line -= 1
        yield a

def cmp(keysforstate, highestdelta, i):
    temp = 0
    for j in range(i - highestdelta, i, 1):
        if keysforstate[j] != keysforstate[j - highestdelta]:
            break
        temp += 1
    return temp

# XXX it seems useless to calculate active lines for hashing.
# seems faster to just grab a couple of lines from the top (as little as two?!)
# and then verify that there is a cycle by comparing lines one by one

# XXX maybe don't start hashing two lines until the count for one line has stopped increasing??
def part1(f, movements, movementsx):
    savedstates = dict()
    statekeys = list()
    heightforcycle = list()
    prevlen = 0
    samelencount = 0
    highestdelta = 0
    P1CYCLE = 2022
    p1ans = 0
    for i in itertools.count():
        if i == P1CYCLE: p1ans = f.highest
        #hashkey = hash(tuple(yfindit(f, f.rgen.rocknum)))
        hashkey = hash( tuple( [ f.rgen.rocknum, f.binrocks[f.highest], f.binrocks[f.highest - 1]] ) )
        statekeys.append(hashkey)
        heightforcycle.append(f.highest)
        prevkeypos = savedstates.get(hashkey)
        if savedstates.get(hashkey, None):
            samelencount += 1
        else:
            samelencount = 0
        savedstates[hashkey] = i
        if samelencount >= len(savedstates):
            delta = i - prevkeypos
            highestdelta = max(delta, highestdelta)

            # only runs once
            temp = cmp(statekeys, highestdelta, i)
            if temp == highestdelta:
                print(len(savedstates))
                print("first repeated cycle is at", i, "with len", highestdelta, "height diff", heightforcycle[i] - heightforcycle[i - highestdelta])
                return p1ans, i, highestdelta, heightforcycle[i] - heightforcycle[i - highestdelta]
                break

        p = f.newpiece()
        p.movex(f, next(movementsx, None))
        while p.trymovedown(f):
            p.movex(f, next(movementsx, None))

tim = aoc.Timing("Timing")
allinput = open("inputdata/input17").readline()

f = Field()

movements = iter(itertools.cycle(allinput[:-1]))
movementsx = iter(itertools.cycle(map(lambda c: ((lambda m: m << 1) if c == '<' else (lambda m: m >> 1)), allinput[:-1])))
p1ans, i, longestiters, longestdelta = part1(f, movements, movementsx)
print("Part 1:", p1ans)

first_cycle = 3922 # OR LESS

ONE_TRILLION = 1000 * 1000 * 1000 * 1000
times, remaining = divmod(ONE_TRILLION - (i), longestiters)

for i in range(remaining):
    p = Piece(f.highest + 7, f.rgen.nextbin())
    p.movex(f, next(movementsx, None))
    while p.trymovedown(f):
        p.movex(f, next(movementsx, None))

print("Part 2:", f.highest + times * longestdelta)
tim.add("done")
#tim.print()

print(aoc.htmlanswers())

