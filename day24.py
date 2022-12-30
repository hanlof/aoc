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


dimensions = None
walls = None
def parse(inputlines):
    blizzards = list()
    global walls
    walls = set()
    minx, maxx, miny, maxy = 0, 0, 0, 0
    global dimensions
    dimensions = (len(inputlines[0]), len(inputlines))
    for y, line in enumerate(inputlines):
        print(y, line)
        for x, c in enumerate(line):
            if c in "<>v^":
                b = Blizzard(x, y, c, dimensions)
                blizzards.append(b)
            elif c == "#":
                walls.add( (x, y) )
    return blizzards, walls

playerpos = (1, 0)

def printfield(bli, dim):
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

goalpos = (100, 36)
blizzards, walls = parse(myinput)

#goalpos=(6, 5) # for easy input!
#blizzards, walls = parse(easyinput)

walls.add( (1, -1) )
walls.add( (100, 37) )

print("Initial state")

def movementchoices(bliz, playerpos):
    global  walls
    choices = list()
    px, py = playerpos
    #for rx, ry in [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]:
    for rx, ry in [(0, 0), (0, 1), (1, 0), (-1, 0), (0, -1)]:
        wantedpos = (px + rx, py + ry)
        if Blizzard(px + rx, py + ry, "<", (0,0)) not in bliz and \
           wantedpos not in walls:
               choices.append(wantedpos)
    return choices

#b = list(blizzards)
#for i in range(0):
#    b = [b.nextpos() for b in b]
#    print("\nMinute", 1+i)
#    choices = movementchoices(set(b), playerpos)
#    if len(choices) == 2: playerpos = choices[1]
#    if len(choices) > 3:
#        print("END AT", i + 1)
#        break
#    #printfield((b), dimensions)
#    print(choices)


counter = 0
fastest = 350
def printpotential(qitem):
    dx = (goalpos[0] - qitem[1][0])
    dy = (goalpos[1] - qitem[1][1])
    print("Potential:", dx, dy, dx+dy)

def getpotential(qitem):
    return (goalpos[0] - qitem[1][0])

cachedblizzardpositions = dict()
cachedblizzardpositions[0] = set(blizzards)
def blizzardpositions(blizzards, minute):
    minute = minute % 700
    if minute in cachedblizzardpositions:
        return cachedblizzardpositions[minute]
    newbliz = [b.nextpos() for b in blizzards]
    cachedblizzardpositions[minute] = set(newbliz)
    return newbliz

#bliz = set(blizzards)
pastblizzards = set()
print("Pre-caching blizzard positions")
for i in range(0,700):
    blizzards = blizzardpositions(blizzards, i+1)
    assert type(blizzards) is list or (i + 1) == 700,\
        "Blizzards must be list when building cache " + str(i)

donepositions = set()
queue = set( [((1,0), 0)] )
while len(queue) > 0:
    temp = queue.pop()
    if temp in donepositions:
        continue
    playerpos, minutes = temp
    if minutes > fastest:
        continue
    bl = cachedblizzardpositions[minutes]
    assert type(bl) is set, "Expected type set"
    choices = movementchoices(set(bl), playerpos)
    if goalpos in choices:
        if minutes < fastest:
            fastest = minutes
            print("New solution!", minutes)
        continue
    for choice in choices:
        newplayerpos = tuple(choice)
        newfield = cachedblizzardpositions[minutes + 1]
        queue.add((newplayerpos, minutes + 1))

    donepositions.add( (playerpos, minutes) )

    if (counter % 10000) == 0 or counter < 10:
        print(counter, "f", fastest, minutes, playerpos, len(queue))
    counter += 1
print("Phase 1 done! Fastest (part 1 solution) is ", fastest)

donepositions = set()
queue = set( [((100, 36), fastest)] )
fastest = 2000
goalpos = (1, 0)
while len(queue) > 0:
    temp = queue.pop()
    if temp in donepositions:
        continue
    playerpos, minutes = temp
    if minutes > fastest:
        continue
    bl = cachedblizzardpositions[minutes % 700]
    assert type(bl) is set, "Expected type set"
    choices = movementchoices(set(bl), playerpos)
    if goalpos in choices:
        if minutes < fastest:
            fastest = minutes
            print("New solution!", minutes)
        continue
    for choice in choices:
        newplayerpos = tuple(choice)
        queue.add((newplayerpos, minutes + 1))
    donepositions.add( (playerpos, minutes) )

    if (counter % 10000) == 0 or counter < 10:
        print(counter, "f+", fastest, minutes, playerpos, len(queue))
    counter += 1

print("Reached the start again after", fastest, "moves. Tracing back to end again!")

donepositions = set()
queue = set( [((1, 0), fastest)] )
fastest = 3000
goalpos = (100, 36)
while len(queue) > 0:
    temp = queue.pop()
    if temp in donepositions:
        continue
    playerpos, minutes = temp
    if minutes > fastest:
        continue
    bl = cachedblizzardpositions[minutes % 700]
    assert type(bl) is set, "Expected type set"
    choices = movementchoices(set(bl), playerpos)
    if goalpos in choices:
        if minutes < fastest:
            fastest = minutes
            print("New solution!", minutes)
        continue
    for choice in choices:
        newplayerpos = tuple(choice)
        queue.add((newplayerpos, minutes + 1))
    donepositions.add( (playerpos, minutes) )

    if (counter % 10000) == 0 or counter < 10:
        print(counter, "f+", fastest, minutes, playerpos, len(queue))
    counter += 1

print("Reached the gool again. Phew! Part 2 answer is", fastest)
