import itertools as I
import operator as O
B = __builtins__
import re, io
import sys, tty, termios
import select, copy

width, height = 0, 0
minx, maxx, miny, maxy = list(), list(), list(), list()

def parse(inputlines):
    global height, width
    global minx, maxx, miny, maxy
    m = list()
    it = iter(inputlines)
    # read input and create horizontal lines
    for line in I.takewhile(lambda l: l != "", it):
        height += 1
        m.append(line)
    # fill in missing spaces so that all squares are accessible
    maxlen = max(B.map(len, m))
    width = maxlen
    miny = [height] * width
    maxy = [0] * width
    minx = [maxlen] * height
    maxx = [0] * height
    outputmap = list()
    for y, line in enumerate(m):
        if len(line) < maxlen:
            line = line + " " * (maxlen - len(line))
        outputmap.append(line)
        leftedge, rightedge = maxlen, 0
        topedge, botedge = height, 0
        # find the wrap-around coordinates
        for x, c in enumerate(line):
            if c != ' ':
                if x <= minx[y]: minx[y] = x
                if x >= maxx[y]: maxx[y] = x
                if y <= miny[x]: miny[x] = y
                if y >= maxy[x]: maxy[x] = y

    return outputmap, next(it)


easyinput = """\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".splitlines()

myinput = open("input22").read().splitlines()

map, moves = parse(myinput)

R = 0
D = 1
L = 2
U = 3

def part1moves():
    ypos = 0
    xpos = minx[0]
    direction = 0
    for m in iter(re.split("(R|L)", moves)):
        if m.isdigit():
            for i in range(int(m)):
                wantedy = ypos
                wantedx = xpos
                if direction == R:
                    wantedx += 1
                    if wantedx > maxx[ypos]: wantedx = minx[ypos]
                elif direction == D:
                    wantedy += 1
                    if wantedy > maxy[xpos]: wantedy = miny[xpos]
                elif direction == L:
                    wantedx -= 1
                    if wantedx < minx[ypos]: wantedx = maxx[ypos]
                elif direction == U:
                    wantedy -= 1
                    if wantedy < miny[xpos]: wantedy = maxy[xpos]
                if map[wantedy][wantedx] == '#': break
                xpos = wantedx
                ypos = wantedy
        elif m == 'L':
            direction -= 1
            direction %= 4
        elif m == 'R':
            direction += 1
            direction %= 4
        else:
            raise Exception("WHAAAAAAAA")
    return (xpos, ypos, direction)

# handle all the wrap-arounds and direction changing in part2
def edgemovement(x, y, d):
    if 0 <= y <= 49: # square 1 and 2
        if 50 <= x <= 99: # square 1
            if d == L: # into 5 facing right
                return (0, 149 - y, R)
            if d == U: # into 6 facing right
                return (0, 150 + (x - 50), R)
        if 100 <= x <= 149: # square 2
            if d == R: # RIGHT to 4
                return (99, 149 - y, L)
            if d == U: # UP to 6
                return (x - 100, 199, U)
            if d == D: # DOWN to 3
                return (99, 50 + x - 100, L)
    if 50 <= y <= 99: # square 3
        if 50 <= x <= 99: # square 3
            if d == L: # LEFT to 5
                return (y - 50, 100, D)
            if d == R: # RIGHT to 2
                return (100 + y - 50, 49, U)
    if 100 <= y <= 149: # square 5 and 4
        if 0 <= x <= 49: # square 5
            if d == L: # LEFT to 1
                return (50, 49 - (y - 100), R)
            if d == U: # UP to 3
                return (50, 50 + x, R)
        if 50 <= x <= 99: # square 4
            if d == R:
                return (149, 49 - (y - 100), L)
            if d == D:
                return (49, 150 + x - 50, L)
    if 150 <= y <= 199: # square 6
        if 0 <= x <= 49: # square 6
            if d == L:
                return (50 + y - 150, 0, D)
            if d == R:
                return (50 + y - 150, 149, U)
            if d == D:
                return (100 + x, 0, D)
    raise Exception(x, y, d)

def part2moves(printat=None):
    ypos = 0
    xpos = minx[0]
    direction = R
    tracemap = copy.deepcopy(map)
    counter = 0
    for m in iter(re.split("(R|L)", moves)):
        if m.isdigit():
            for i in range(int(m)):
                wantedy = ypos
                wantedx = xpos
                wanteddir = direction
                if   direction == R:
                    wantedx += 1
                    if wantedx > maxx[ypos]:
                        wantedx, wantedy, wanteddir = edgemovement(xpos, ypos, direction)
                elif direction == D:
                    wantedy += 1
                    if wantedy > maxy[xpos]:
                        wantedx, wantedy, wanteddir = edgemovement(xpos, ypos, direction)
                elif direction == L:
                    wantedx -= 1
                    if wantedx < minx[ypos]:
                        wantedx, wantedy, wanteddir = edgemovement(xpos, ypos, direction)
                elif direction == U:
                    wantedy -= 1
                    if wantedy < miny[xpos]:
                        wantedx, wantedy, wanteddir = edgemovement(xpos, ypos, direction)
                if map[wantedy][wantedx] == '#':
                    break
                xpos = wantedx
                ypos = wantedy
                direction = wanteddir
                counter += 1
                line = tracemap[ypos]
                #line = line[:xpos] + chr(0x30 + (counter % 10)) + line[
                # move 222 suspicious
                if printat is not None:
                    whatline = printat
                    if whatline < counter < whatline + 30:
                        command = m
                        traceline = ypos
                        tracemap[ypos] = tracemap[ypos][:xpos] + chr(0x30 + (counter % 10)) + tracemap[ypos][xpos+1:]
                    if counter == whatline + 29:
                        print( (xpos, ypos, direction) )
            continue
        elif m == 'L':
            direction -= 1
            direction %= 4
        elif m == 'R':
            direction += 1
            direction %= 4
        else:
            raise Exception("WHAAAAAAAA")
    if printat is not None:
        for l in tracemap[:traceline + 40]:
            print(l)
        print(command)
    return (xpos, ypos, direction)

def computepassword(x, y, d):
    return 1000 * (y + 1) + 4 * (x + 1) + direction

xpos, ypos, direction = part1moves()
print("Part 1:", computepassword(xpos, ypos, direction))
xpos, ypos, direction = part2moves()
print("Part 2:", computepassword(xpos, ypos, direction))

def ttyinput():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    inp = bytes()
    try:
        tty.setraw(sys.stdin.fileno())
        stdin=io.open(sys.stdin.fileno(), 'rb', closefd=False, buffering=False)

        p = select.poll()
        p.register(stdin)
        select.select([stdin, ], [], [])
        inp = bytes()
        while select.POLLIN & p.poll()[0][1]:
            inp += stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return inp

# interactive stepping. enable by changing while False to while True
printat = 2438
while False:
    inp = ttyinput()
    if inp == bytes(b'\x1b[A'):
        print("UP")
        printat -= 10
    if inp == bytes(b'\x1b[D'):
        printat -= 1
        print("LEFT")
    if inp == bytes(b'\x1b[B'):
        print("DOWN")
        printat += 10
    if inp == bytes(b'\x1b[C'):
        print("RIGHT")
        printat += 1
    if ord('q') in inp: break
    xpos, ypos, direction = part2moves(printat=printat)
    print(printat)

# 142228 is correct
# 127050 too low
