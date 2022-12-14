import sys
import re
import os

print(__file__)

#inputfile = sys.stdin

x = 1
cycle = 1

long = \
"""addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".split("\n")

short = \
"""noop
addx 3
addx -5""".split("\n")

inputfile = open("input10")
allinput = inputfile.readlines()

#allinput = long
queue = list()

def draw(cycle, x):
    xpos = (cycle % 40) - 1 # why -1?? :O
    if x == xpos or (x - 1) == (xpos) or (x + 1) == (xpos):
        print("#", end="")
    else:
        print(".", end="")

def processqueue(s):
    global cycle, queue, x
    update = 0
    if len(queue) > 0:
        queue[-1][1] = queue[-1][1] - 1
        if queue[-1][1] == 0:
            update = queue.pop()[0]

    ret = 0
    draw(cycle, x)
    if (cycle % 40) == 20:
        ret = cycle * x
        #print(s, cycle, x)
    if (cycle % 40) == 0:
        print()
    x = x + update
    cycle = cycle + 1
    return ret

signalstrength = 0
for i in allinput:
    r = re.match("(\w+) ?(-?\d+)?", i)
    instr = r[1]
    if r[2]:
        num = int(r[2])
        queue.insert(0, [num, 2])
    else:
        queue.insert(0, [0, 1])
    signalstrength = signalstrength + processqueue("%")

while len(queue) > 0:
    signalstrength = signalstrength + processqueue(">")

print("Part 1:", signalstrength)

print("Part 2:", signalstrength)

