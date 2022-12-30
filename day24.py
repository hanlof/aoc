import sys, itertools as I, re, copy, os, operator as O
B = __builtins__

easyinput = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".splitlines()

myinput = open("input24").read().splitlines()
signstomovement = {
    ">": ( 1,  0),
    "<": (-1,  0),
    "v": ( 0,  1),
    "^": ( 0, -1) }

class Blizzard:
    def __init__(s, x, y, sign, dim):
        s.maxx = dim[0] - 2
        s.maxy = dim[1] - 2
        s.x = x
        s.y = y
        s.sign = sign
        s.step = signstomovement[sign]
    def advance(s):
        s.x += s.step[0]
        s.y += s.step[1]
        if s.x == 0: s.x = s.maxx
        if s.x > s.maxx: s.x = 1
        if s.y == 0: s.y = s.maxy
        if s.y > s.maxy: s.y = 1
    def nextpos(s):
        x = s.x + s.step[0]
        y = s.y + s.step[1]
        if x == 0: x = s.maxx
        if x > s.maxx: x = 1
        if y == 0: y = s.maxy
        if y > s.maxy: y = 1
        return Blizzard(x, y, s.sign, (s.maxx + 2, s.maxy + 2))
    def toxytuple(s):
        return (s.x, s.y)
    def __eq__(s, tup):
        if type(tup) is Blizzard:
            return tup.x == s.x and tup.y == s.y
        if type(tup) is tuple:
            return tup[0] == s.x and tup[1] == s.y
        assert False
    def __neq__(s, x):
        return not s.__eq__(x)
    def __repr__(s):
        return s.__str__()
    def __str__(s):
        return "<%d %d>" % (s.x, s.y)
    def __hash__(s):
        return (s.y << 20) + s.x
    def __lt__(s, o):
        return s.x < o.x

def parse(inputlines):
    blizzards = list()
    global walls
    walls = set()
    minx, maxx, miny, maxy = 0, 0, 0, 0
    dimensions = (len(inputlines[0]), len(inputlines))
    for y, line in enumerate(inputlines):
        for x, c in enumerate(line):
            if c in "<>v^":
                b = Blizzard(x, y, c, dimensions)
                blizzards.append(b)
            elif c == "#":
                walls.add( (x, y) )
            elif y == 0 and c == ".":
                walls.add( (x, y - 1) )
                startpos = (x, y)
            elif y == dimensions[1] - 1 and c == ".":
                walls.add( (x, y + 1) )
                endpos = (x, y)
    return blizzards, walls, startpos, endpos

def printfield(bli, dim, playerpos):
    for y in range(dim[1]):
        for x in range(dim[0]):
            i = bli.count((x, y)) if type(bli) is list else None
            if False: pass
            elif (x, y) == playerpos: print("P", end="")
            elif (x, y) in walls: print("#", end="")
            elif i == 1: print(bli[bli.index( (x,y) )].sign, end="")
            elif i is not None and i > 1: print(i, end="")
            elif Blizzard(x, y, "<", (0,0)) in bli: print(".", end="")
            elif (x, y) == goalpos: print("G", end="")
            else: print(" ", end="")
        print("")

def movementchoices(bliz, px, py):
    global  walls
    choices = list()
    for rx, ry in [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]:
        wantedpos = (px + rx, py + ry)
        if wantedpos not in bliz and \
           wantedpos not in walls:
               yield wantedpos

def findfastest(startpos, endpos, startminute):
    global cachedblizzardpositions
    counter = 0
    fastest = None
    donepositions = set()
    queue = set()
    queue.add ( (startpos[0], startpos[1], startminute) )
    while len(queue) > 0:
        curx, cury, minutes = queue.pop()
        if fastest is not None:
            if minutes > fastest:
                continue
        blockedpositions = cachedblizzardpositions[minutes % 700]
        for choice in movementchoices(blockedpositions, curx, cury):
            if endpos == choice:
                if fastest is None:
                    fastest = minutes
                    continue
                if minutes < fastest:
                    fastest = minutes
                    continue
            temp = (choice[0], choice[1], minutes + 1)
            if not temp in donepositions:
                queue.add(temp)
        donepositions.add( (curx, cury, minutes) )
        if (counter % 20000) == 10000:
            print("Working... cycle is", counter, "minutes is", minutes, "queue-length is", len(queue))
        counter += 1
    print("Done! Fastest trip from %s to %s starting at minude %d is %d" % (startpos, endpos, startminute, fastest))
    return fastest

blizzards, walls, playerpos, goalpos = parse(myinput)

print("Pre-caching blizzard positions. Assuming the blizzards cycle at 700, have not verified for other inputs than my own... ", end="")
sys.stdout.flush()

cachedblizzardpositions = dict()
for i in range(0,700):
    #print("\x1b[40D\x1b[31C""%d/700" % (i + 1), end="")
    #sys.stdout.flush()
    cachedblizzardpositions[i] = set([b.toxytuple() for b in blizzards])
    for b in blizzards:
        b.advance()

print("")
phase1fastest = findfastest( (1, 0), goalpos, 0)
phase2fastest = findfastest( goalpos, (1, 0), phase1fastest)
phase3fastest = findfastest( (1, 0), goalpos, phase2fastest)

print("Part 1:", phase1fastest)
print("Part 2:", phase3fastest)
