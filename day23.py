import itertools as I
import operator as O
B = __builtins__

easystring = """..............
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

myinput = open("input23").readlines()
easyinput = easystring.split("\n")

def parseinput(inputlines):
    elfs = set()
    for y, l in enumerate(inputlines):
        for x, c in enumerate(l):
            if c == "#":
                elfs.add(x + y*1j)
    return elfs

N  =  0-1j; S  =  0+1j; W  = -1+0j; E  = +1+0j
NW = -1-1j; NE = +1-1j; SW = -1+1j; SE = +1+1j
surrounding = [N, S, E, W, NW, NE, SW, SE]
directions = [N, S, W, E]
directionsquarestocheck = [
    [NW, N, NE],
    [SW, S, SE],
    [NW, W, SW],
    [NE, E, SE]]

def printfield(elfs):
    for y in range(int(min(elfs, key=lambda a: a.imag).imag), int(max(elfs, key=lambda a: a.imag).imag) + 1):
        for x in range(int(min(elfs, key=lambda a: a.real).real), int(max(elfs, key=lambda a: a.real).real) + 1):
            print("#" if (x+y*1j in elfs) else ".", end="")
        print("")

def relativeoccupied(elf, rellist, elfs):
    for square in rellist:
        if elf + square in elfs:
            return True
    return False

def dance(inputelfs, rounds=None, verbose=0):
    elfs = set(inputelfs)
    directioncounter = I.cycle(range(4))
    for currentround in I.count(1):
        # get elfs that need to move in a separate list
        movable = list()
        for elf in elfs:
            if relativeoccupied(elf, surrounding, elfs):
                movable.append(elf)
        if len(movable) == 0: break
        if verbose: print("Round", i, "movable", len(movable))
        # get list of pairs of where elfs want to move from and to
        proposedmoves = list()
        for elf in movable:
            directioncounter, dirs = I.tee(directioncounter)
            for i in I.islice(dirs, 4):
                if not relativeoccupied(elf, directionsquarestocheck[i], elfs):
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
        for fr, to in proposedmoves:
            if to not in blockedmoves:
                elfs.remove(fr)
                elfs.add(to)
        if verbose: print("  Minmax", min(elfs, key=lambda a: a.imag).imag,\
                          max(elfs, key=lambda a: a.imag).imag,\
                          min(elfs, key=lambda a: a.real).real,\
                          max(elfs, key=lambda a: a.real).real)
        if rounds is not None and currentround >= rounds: break
    return currentround, elfs

def part1analysis(e):
    minx = int(min(e, key=lambda a: a.real).real)
    maxx = int(max(e, key=lambda a: a.real).real)
    miny = int(min(e, key=lambda a: a.imag).imag)
    maxy = int(max(e, key=lambda a: a.imag).imag)
    xsize = maxx - minx + 1
    ysize = maxy - miny + 1
    print("Square", xsize, "*", ysize, "=", xsize * xsize, "empty", xsize * ysize - len(elfs))
    return xsize * ysize - len(e)

elfs = parseinput(myinput)

_, e = dance(elfs, 10, verbose=0)
print("Part 1:", part1analysis(e))

rounds, e = dance(elfs, None, verbose=0)
print("Part 2:", rounds)


