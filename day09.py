import sys
import re
import os
import itertools

print("Day 9: Rope simulations")
allinput = open("input09").readlines()
easyinput = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split("\n")

def update_tail(leader, follower):
    dx = leader.real - follower.real
    signx = (dx > 0) - (dx < 0)
    dy = leader.imag - follower.imag
    signy = 1j * ((dy > 0) - (dy < 0))
    if (abs(dx) > 1) or (abs(dy) > 1):
        follower += signx + signy
    return follower

movements = {"U": -1j, "D": 1j, "L": -1, "R": 1}
def simrope(ropelen, moves):
    positions = set()
    rope = list()
    for i in range(ropelen):
        rope.append( 0 + 0j )
    for move in moves:
        r = re.match("(?P<dir>.) (?P<count>\d+)", move)
        for i in range(int(r['count'])):
            rope[0] += movements[r['dir']]
            for n, p in enumerate(itertools.pairwise(rope)):
                rope[n + 1] = update_tail(*p)
            positions.add(rope[-1])
    return len(positions)

print("Part 1:", simrope(2, allinput))
print("Part 2:", simrope(10, allinput))



