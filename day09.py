import sys
import re
import os

print(__file__)

#inputfile = sys.stdin
inputfile = open("input09")
allinput = inputfile.readlines()

# allinput = """R 4
# U 4
# L 3
# D 1
# R 4
# D 1
# L 5
# R 2""".split("\n")

x = 0
y = 0
tx = 0
ty = 0
positions = set()

positions.add( (tx, ty) )
def update_tail():
    global x, y, tx, ty
    if x > (tx + 1):
        tx = tx + 1
        ty = y
    if x < (tx - 1):
        tx = tx - 1
        ty = y
    if y > (ty + 1):
        ty = ty + 1
        tx = x
    if y < (ty - 1):
        ty = ty - 1
        tx = x

for i in allinput:
    r = re.match("(.) (\d+)", i)
    direc = r[1]
    count = int(r[2])

    dx = 0
    dy = 0
    if direc == "U": dy = -1
    elif direc == "D": dy = 1
    elif direc == "L": dx = -1
    elif direc == "R": dx = 1
    for i in range(count):
        x = x + dx
        y = y + dy
        update_tail()
        positions.add( (tx, ty) )

print("Part 1:", len(positions))

class XY():
    def __init__(this, x, y):
        this.x = x
        this.y = y
    def __str__(this):
        return "%d %d" % (this.x, this.y)

rope = list()
positions = set()
positions.add( (0, 0) )

for i in range(10):
    rope.append( XY(0, 0) )

def update_tail_x(leader, follower):
    dx = leader.x - follower.x
    signx = (dx > 0) - (dx < 0)
    dy = leader.y - follower.y
    signy = (dy > 0) - (dy < 0)
    if (abs(dx) > 1) or (abs(dy) > 1):
        follower.x = follower.x + signx
        follower.y = follower.y + signy

for i in allinput:
    r = re.match("(.) (\d+)", i)
    direc = r[1]
    count = int(r[2])

    dx = 0
    dy = 0
    if direc == "U": dy = -1
    elif direc == "D": dy = 1
    elif direc == "L": dx = -1
    elif direc == "R": dx = 1
    for i in range(count):
        rope[0].x = rope[0].x + dx
        rope[0].y = rope[0].y + dy
        update_tail_x(rope[0], rope[1])
        update_tail_x(rope[1], rope[2])
        update_tail_x(rope[2], rope[3])
        update_tail_x(rope[3], rope[4])
        update_tail_x(rope[4], rope[5])
        update_tail_x(rope[5], rope[6])
        update_tail_x(rope[6], rope[7])
        update_tail_x(rope[7], rope[8])
        update_tail_x(rope[8], rope[9])
        positions.add( (rope[9].x, rope[9].y) )

print("Part 2:", len(positions))

