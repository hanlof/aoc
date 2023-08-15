import aoc
import itertools as I, operator as O

easyinput = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".splitlines()

myinput = open("inputdata/input24").read().splitlines()
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
    def atminute(s, m):
        if s.step[0] == 0:
            y = s.y -1 + s.step[1] * m
            y = 1 + (y % (s.maxy))
            x = s.x
        else:
            x = s.x -1 + s.step[0] * m
            x = 1 + (x % (s.maxx))
            y = s.y
        return (x, y)
    def advance(s):
        s.x += s.step[0]
        s.y += s.step[1]
        s.x = 1 + ((s.x - 1) % (s.maxx))
        s.y = 1 + ((s.y - 1) % (s.maxy))
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
        return "<%d %d %c >" % (s.x, s.y, s.sign)
    def __hash__(s):
        return (s.y << 20) + s.x
    def __lt__(s, o):
        return s.x < o.x

staticblizzards = list()
def parse(inputlines):
    global staticblizzards
    blizzards = list()
    global walls
    walls = set()
    minx, maxx, miny, maxy = 0, 0, 0, 0
    dimensions = (len(inputlines[0]), len(inputlines))
    for y, line in enumerate(inputlines):
        for x, c in enumerate(line):
            if c in "<>v^":
                b = Blizzard(x, y, c, dimensions)
                b2 = Blizzard(x, y, c, dimensions)
                staticblizzards.append(b2)
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

count = 0
blockedposcache = dict()
count = 0
def movementchoices2(i, px, py):
    global walls
    global blizzards
    global count
    count += 1
    if (count % 100) == 0:
        print(px, py, i, count * len(blizzards))
    #bliz = walls | set([b.atminute(i) for b in blizzards])
    bliz = set([b.atminute(i % 700) for b in blizzards])
    for rx, ry in [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]:
        wantedpos = (px + rx, py + ry)
        if wantedpos not in bliz and wantedpos not in walls:
               yield wantedpos

movementcache = dict()
def movementchoices3(minute, px, py):
    bliz = cachedblizzardpositions[minute % 700]
    yield from [p for p in [(px + 1, py), (px, py+1), (px, py), (px-1, py), (px, py-1)] if p not in bliz and p not in walls]

def movementchoices(bliz, px, py):
    global walls
    global movementcache
    for rx, ry in [(0, 1), (1, 0), (0, 0), (-1, 0), (0, -1)]:
        wantedpos = (px + rx, py + ry)
        if wantedpos not in bliz:
               yield wantedpos
        #cachekey = (minutes,) + (wantedpos,)
        #if cachekey in blockedposcache:
        #    blockedpositions = blockedposcache[cachekey]
        #else:
            #blockedpositions =  set([b.atminute((minutes) % 700) for b in blizzardsbycol[wantedpos[0]]])
            #blockedpositions |= set([b.atminute((minutes) % 700) for b in blizzardsbyrow[wantedpos[1]]])
            #blockedposcache[cachekey] = blockedpositions
        #if wantedpos not in blockedpositions and wantedpos not in walls:

# The only unique parameters for a state is minute and x, y position
# because the minute explicitly decides the state of the moving blizards.
# The blizards cycle around to starting position after 700 steps (my input)
# so we can easily pre-cache them all.
# The queue of states to try culls itself because it's held in a set()
# A separate set() of previously tried positions is maintained as well
# so we don't add old processed positions to the queue.
donepositions = set()
highestminute = 0
def mdist(goal, pos):
    return abs(goal[0] - pos[0]) + abs(goal[1] - pos[1])

import heapq
class QueueItem():
    def __init__(s, state, goal, startminute):
        s.state = state
        s.dist = abs(goal[0] - s.state[0]) + abs(goal[1] - s.state[1]) + (s.state[2] - startminute)
    def __lt__(s, o):
        return s.dist < o.dist
    def tup(s):
        return s.state

A = [ 0, 0, 0 ]
def findfastest(startpos, endpos, startminute):
    donepositions = set()
    queue = [ QueueItem( (startpos[0], startpos[1], startminute), endpos, startminute) ]
    while len(queue) > 0:
        curstate = heapq.heappop(queue).state
        if curstate in donepositions: continue
        curx, cury, minutes = curstate
        for choice in [(curx, cury+1), (curx+1, cury), (curx, cury), (curx-1, cury), (curx, cury-1)]:
            if choice in xblizzards[minutes % 100] or choice in yblizzards[minutes % 35] or choice in walls: continue
            if endpos == choice:
                return minutes
            newstate = (choice[0], choice[1], minutes + 1)
            if not newstate in donepositions:
                heapq.heappush( queue, QueueItem(newstate, endpos, startminute) )
        donepositions.add(curstate)

    assert False, "What"

blizzards, walls, startpos, goalpos = parse(myinput)

tim = aoc.Timing("Timing:")

maxx, maxy = 0, 0
for b in blizzards:
    maxx = max(maxx, b.x)
    maxy = max(maxy, b.y)

minx, miny = maxx, maxy
for b in blizzards:
    minx = min(minx, b.x)
    miny = min(miny, b.y)

yblizzards = [set() for l in range(maxy + 3)]
xblizzards = [set() for l in range(maxx + 3)]

print("Part 1:", end=" ", flush=True)
with aoc.Spinner(delay=0.1):
    for m in range(maxy + 3):
        for b in blizzards:
            if b.step[0] == 0:
                yblizzards[m].add(b.atminute(m))
    for m in range(maxx + 3):
        for b in blizzards:
            if b.step[1] == 0:
                xblizzards[m].add(b.atminute(m))
    #for i in range(350):
        #cachedblizzardpositions[i] = xblizzards[i % 100] | yblizzards[i % 35]
    tim.add("Pre-caching done")
    phase1fastest = findfastest( startpos, goalpos, 0)
    tim.add("Phase 1 done")
print(phase1fastest)

print("Part 2:", end=" ", flush=True)
with aoc.Spinner():
    phase2fastest = findfastest( goalpos, startpos, phase1fastest)
    tim.add("Phase 2 done")
    phase3fastest = findfastest( startpos, goalpos, phase2fastest)
    tim.add("Phase 3 done")
print(phase3fastest)
# tim.print()

