import aoc

# 140 x 140
pipesbycoord = dict()
startcoord = 0
adjacent = {(x + y * 1j) for x in [-1, 0, 1] for y in [-1, 0, 1]} - { (0j) }
pipeexits = {
    '-': [ -1, 1],
    '|': [-1j, 1j],
    '7': [ -1, 1j],
    'F': [  1, 1j],
    'J': [ -1, -1j],
    'L': [  1, -1j] }

pipeturns = { # in the direction of pipeexits, clockwise = 1, ccw = -1
    '-': 0,
    '|': 0,
    '7': 1,
    'F': -1,
    'J': -1,
    'L': 1 }

dir2posdelta = { 0: -1j, 1: 1, 2: 1j, 3: -1 }
posdelta2dir = dict([[v, k] for k, v in dir2posdelta.items()])

for y, l in enumerate(aoc_inputlines):
    for x, c in enumerate(l):
        pipesbycoord[x + y * 1j] = c
        if c == "S":
            startcoord = x + y * 1j

# insert the correct pipe into starting position
matchingdirections = list()
for a in adjacent:
    e = pipesbycoord[startcoord + a]
    if startcoord + a + pipeexits[e][0] == startcoord:
        matchingdirections.append(a)
    if startcoord + a + pipeexits[e][1] == startcoord:
        matchingdirections.append(a)

for k, e in pipeexits.items():
    if set(e) == set(matchingdirections):
        pipesbycoord[startcoord] = k

distance = { startcoord: 0 }
pipes = [ startcoord ]
maxdist = 0
# iterate both directions at the same time
while pipes:
    coord = pipes.pop()
    shape = pipesbycoord[coord]
    for direction in pipeexits[shape]:
        newcoord = coord + direction
        if newcoord not in distance:
            newdist = distance[coord] + 1
            maxdist = max(maxdist, newdist)
            distance[newcoord] = newdist
            pipes.insert(0, newcoord)

print("Part 1:", maxdist)

DIRECTION = 0
prevcoord = startcoord + pipeexits[pipesbycoord[startcoord]][DIRECTION]
startdir = posdelta2dir[pipeexits[pipesbycoord[startcoord]][DIRECTION]]
startdir = (startdir + 2) % 4 # startdir is oposite the direction of exit 1
curcoord = startcoord
curdir = startdir

# this loop finds the looping direction of the path around the circular pipe in
# the direction going towards startcoords first exit. CW or CCW
while True:
    shape = pipesbycoord[curcoord]
    for posdelta in pipeexits[shape]:
        if posdelta + curcoord != prevcoord:
            nextcoord = posdelta + curcoord
            break
    if posdelta == pipeexits[shape][0]:
        dirdelta = -pipeturns[shape]
    else:
        dirdelta = pipeturns[shape]
    prevcoord = curcoord
    curcoord = nextcoord
    curdir += dirdelta
    if curcoord == startcoord: break

insidedir = (curdir - startdir) // abs(curdir - startdir)

# the direction of the inside relative to the traversing direction is determined
# now traverse the pipe again and mark all squares on the inside side as inside
prevcoord = startcoord + pipeexits[pipesbycoord[startcoord]][DIRECTION]
startdir = posdelta2dir[pipeexits[pipesbycoord[startcoord]][DIRECTION]]
startdir = (startdir + 2) % 4 # startdir is oposite the direction of exit 1
curcoord = startcoord
curdir = startdir
inside = set()


# XXX Currently this loop also finds all inside squares assuming
# that "inside" is to the right of every square in the pipe loop
# XXX needs to be tidied up ok thanks!

while True:
    shape = pipesbycoord[curcoord]
    for posdelta in pipeexits[shape]:
        if posdelta + curcoord != prevcoord:
            nextcoord = posdelta + curcoord
            break
    if posdelta == pipeexits[shape][0]:
        dirdelta = -pipeturns[shape]
    else:
        dirdelta = pipeturns[shape]
    totheright = curcoord + dir2posdelta[(curdir + insidedir) % 4]
    if totheright not in distance:
        inside |= { totheright }
    totheright = prevcoord + dir2posdelta[(curdir + insidedir) % 4]
    if totheright not in distance:
        inside |= { totheright }

    prevcoord = curcoord
    curcoord = nextcoord
    curdir += dirdelta
    if curcoord == startcoord: break

def floodfill(collection):
    filled = 0
    newset = set()
    for c in collection:
        for posdelta in [ -1j, 1j, -1, 1 ]:
            trycoord = c + posdelta
            if trycoord not in collection and trycoord not in distance:
                filled += 1
                newset |= { c + posdelta }
    collection |= newset
    return len(newset)

while floodfill(inside) > 0: pass
print("Part 2:", len(inside))

def coloredprint():
    for y in range(140):
        for x in range(140):
            coord =  y * 1j + x
            col = "\x1b[0m"
            if coord == startcoord:
                col = "\x1b[1;31m"
            elif coord in inside:
                col = "\x1b[0;35m"
            elif coord in distance:
                col = "\x1b[33m"
            print(col, pipesbycoord[coord], "\x1b[0m", sep="", end="")
        print()
#coloredprint()
