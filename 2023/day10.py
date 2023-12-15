import aoc

# 140 x 140
pipesbycoord = dict()
startcoord = 0
pipeexits = { '-': [ -1, 1],  '|': [-1j, 1j],  '7': [ -1, 1j],
              'F': [  1, 1j], 'J': [ -1, -1j], 'L': [  1, -1j] }
# in the direction of pipeexits, clockwise = 1, ccw = -1
pipeturns = { '-': 0, '|': 0, '7': 1, 'F': -1, 'J': -1, 'L': 1 }
dir2posdelta = { 0: -1j, 1: 1, 2: 1j, 3: -1 }
posdelta2dir = dict([[v, k] for k, v in dir2posdelta.items()])

for y, l in enumerate(aoc_inputlines):
    for x, c in enumerate(l):
        pipesbycoord[x + y * 1j] = c
        if c == "S":
            startcoord = x + y * 1j

# insert the correct pipe into starting position
startingexits = set()
for a in [1, -1, 1j, -1j]:
    for e in pipeexits[pipesbycoord[startcoord + a]]:
        if startcoord + a + e == startcoord:
            startingexits |= {a}
for shape, exits in pipeexits.items():
    if set(exits) == startingexits:
        pipesbycoord[startcoord] = shape

distances = { startcoord: 0 }
pipes = [ startcoord ]
# iterate both directions at the same time
while pipes:
    coord = pipes.pop()
    shape = pipesbycoord[coord]
    for posdelta in pipeexits[shape]:
        newcoord = coord + posdelta
        if newcoord not in distances:
            distances[newcoord] = distances[coord] + 1
            pipes.insert(0, newcoord)

print("Part 1:", max(distances.values()))

# this loop finds the looping direction of the path around the circular pipe in
# the direction going towards startcoords first exit. CW or CCW
TRAVERSEDIR = 0 # select exit 0 or 1 to start traversing from the starting coordinate
prevcoord = startcoord + pipeexits[pipesbycoord[startcoord]][TRAVERSEDIR]
startdir = posdelta2dir[pipeexits[pipesbycoord[startcoord]][TRAVERSEDIR]]
startdir = (startdir + 2) % 4 # startdir is oposite the direction from start to prev
curcoord = startcoord
curdir = startdir
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
insideturndirection = (curdir - startdir) // abs(curdir - startdir)

# the direction of the inside relative to the traversing direction is determined
# now traverse the pipe again and mark all squares on this side as inside squares
prevcoord = startcoord + pipeexits[pipesbycoord[startcoord]][TRAVERSEDIR]
startdir = posdelta2dir[pipeexits[pipesbycoord[startcoord]][TRAVERSEDIR]]
startdir = (startdir + 2) % 4 # startdir is oposite the direction of exit 1
curcoord = startcoord
curdir = startdir
inside = set()
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
    for c in curcoord, prevcoord:
        insidecoord = c + dir2posdelta[(curdir + insideturndirection) % 4]
        if insidecoord not in distances:
            inside |= { insidecoord }
    prevcoord = curcoord
    curcoord = nextcoord
    curdir += dirdelta
    if curcoord == startcoord: break

def floodfill(collection, limit):
    newset = set()
    for c in collection:
        for posdelta in [ -1j, 1j, -1, 1 ]:
            trycoord = c + posdelta
            if trycoord not in collection and trycoord not in limit:
                newset |= { c + posdelta }
    collection |= newset
    return len(newset)

while floodfill(inside, distances) > 0: pass
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
            elif coord in distances:
                col = "\x1b[33m"
            print(col, pipesbycoord[coord], "\x1b[0m", sep="", end="")
        print()
coloredprint()
