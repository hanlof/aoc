import itertools as I
import operator as O
B = __builtins__

# Dancing elfs. Spreading out points according to specific rules.

easystring = \
"""..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""

myinput = open("inputdata/input23").readlines()
easyinput = easystring.split("\n")

N  =  0-1j; S  =  0+1j; W  = -1+0j; E  = +1+0j
NW = -1-1j; NE = +1-1j; SW = -1+1j; SE = +1+1j
surrounding = [N, S, E, W, NW, NE, SW, SE]
directions = [N, S, W, E]
directionsquarestocheck = [
    [NW, N, NE],
    [SW, S, SE],
    [NW, W, SW],
    [NE, E, SE]]

def parseinput(inputlines):
    elfs = set()
    for y, l in enumerate(inputlines):
        for x, c in enumerate(l):
            if c == "#":
                elfs.add(x + y*1j)
    return elfs

def printfield(elfs):
    for y in range(int(min(elfs, key=lambda a: a.imag).imag), int(max(elfs, key=lambda a: a.imag).imag) + 1):
        for x in range(int(min(elfs, key=lambda a: a.real).real), int(max(elfs, key=lambda a: a.real).real) + 1):
            print("#" if (x + y * 1j in elfs) else ".", end="")
        print("")

def getpossiblemoves(elf, elfs, moveslist, chilling):
    # N = 1 ; S = 2 ; W = 4 ; E = 8
    moves = 0
    if elf + N not in elfs:
        moves |= 1
    elif elf + N in chilling:
        chilling.remove(elf + N)
        getpossiblemoves(elf + N, elfs, moveslist, chilling)
    if elf + S not in elfs:
        moves |= 2
    elif elf + S in chilling:
        chilling.remove(elf + S)
        getpossiblemoves(elf + S, elfs, moveslist, chilling)
    if elf + W not in elfs:
        moves |= 4
    elif elf + W in chilling:
        chilling.remove(elf + W)
        getpossiblemoves(elf + W, elfs, moveslist, chilling)
    if elf + E not in elfs:
        moves |= 8
    elif elf + E in chilling:
        chilling.remove(elf + E)
        getpossiblemoves(elf + E, elfs, moveslist, chilling)
    if moves == 0: return
    if elf + NW in elfs:
        moves &= 2|8
        if elf + NW in chilling:
            chilling.remove(elf + NW)
            getpossiblemoves(elf + NW, elfs, moveslist, chilling)
    if elf + NE in elfs:
        moves &= 2|4
        if elf + NE in chilling:
            chilling.remove(elf + NE)
            getpossiblemoves(elf + NE, elfs, moveslist, chilling)
    if elf + SW in elfs:
        moves &= 1|8
        if elf + SW in chilling:
            chilling.remove(elf + SW)
            getpossiblemoves(elf + SW, elfs, moveslist, chilling)
    if elf + SE in elfs:
        moves &= 1|4
        if elf + SE in chilling:
            chilling.remove(elf + SE)
            getpossiblemoves(elf + SE, elfs, moveslist, chilling)
#    if elf + 2*SE in elfs:
#        moves &= 1|2|4|8
#        if elf + 90000 in chilling:
#            chilling.remove(elf + SE)
#            getpossiblemoves(elf + SE, elfs, moveslist, chilling)
    if moves == 1|2|4|8:
        chilling.add(elf)
        return
    if moves != 0:
        moveslist[elf] = moves
        return

def dance(inputelfs, rounds=None, verbose=0):
    elfs = set(inputelfs)
    directioncounter = I.cycle(range(4))
    chilling = set()
    for currentround in I.count(1):
        # create list elfs of elfs that need to move
        movable = dict()
        for elf in elfs - chilling:
            getpossiblemoves(elf, elfs, movable, chilling)
        if len(movable) == 0: break
        if verbose: print("Round", currentround, "movable", len(movable))
        # create list of pairs of where elfs want to move from and to
        proposedmoves = list()
        for elf, elfdirections in movable.items():
            directioncounter, dirs = I.tee(directioncounter)
            for i in I.islice(dirs, 4):
                if elfdirections & (1 << i):
                    proposedmoves.append( (elf, elf + directions[i]) )
                    break
        next(directioncounter)
        # Add duplicate moves to blockedmoves
        if verbose: print("  Proposed moves:", len(proposedmoves))
        temp = set()
        blockedmoves = set()
        for fr, to in proposedmoves:
            if to in temp: blockedmoves.add(to)
            temp.add(to)
        # Do any movement in proposedmoves that is not also in blocked moves
        if verbose: print("  Blocked moves:", len(blockedmoves))
        newelfs = set()
        for fr, to in proposedmoves:
            if to not in blockedmoves:
                elfs.remove(fr)
                elfs.add(to)
        if verbose: print("  Minmax", min(elfs, key=O.attrgetter("imag")).imag,\
                                      max(elfs, key=O.attrgetter("imag")).imag,\
                                      min(elfs, key=O.attrgetter("real")).real,\
                                      max(elfs, key=O.attrgetter("real")).real)
        if rounds is not None and currentround >= rounds: break
    return currentround, elfs

def part1analysis(e):
    minx = min(map(O.attrgetter("real"), e))
    maxx = max(map(O.attrgetter("real"), e))
    miny = min(map(O.attrgetter("imag"), e))
    maxy = max(map(O.attrgetter("imag"), e))
    xsize = maxx - minx + 1
    ysize = maxy - miny + 1
    return xsize * ysize - len(e)

elfs = parseinput(myinput)

_, e = dance(elfs, 10, verbose=0)
print("Part 1:", part1analysis(e))

rounds, e = dance(elfs, None, verbose=0)
print("Part 2:", rounds)

