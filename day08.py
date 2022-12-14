import sys
import re
import os

print(__file__)

#inputfile = sys.stdin
inputfile = open("input08")
allinput = inputfile.readlines()

map = [ ]

for i in allinput:
    map.append(list(i[0:-1]))

vismap = []
vismap = [[0] * len(map[0]) for i in range(len(map))]

for y in range(len(map)):
    # check from the left
    visheight = 0
    for x in range(len(map[y])):
        height = int(map[y][x])
        if height >= visheight:
            vismap[y][x] = 1
            visheight = height + 1
    # check from the right
    visheight = 0
    for x in reversed(range(len(map[y]))):
        height = int(map[y][x])
        if height >= visheight:
            vismap[y][x] = 1
            visheight = height + 1

for x in range(len(map[0])):
    # check from the top
    visheight = 0
    for y in range(len(map)):
        height = int(map[y][x])
        if height >= visheight:
            vismap[y][x] = 1
            visheight = height + 1
    # check from the right
    visheight = 0
    for y in reversed(range(len(map))):
        height = int(map[y][x])
        if height >= visheight:
            vismap[y][x] = 1
            visheight = height + 1

count = 0
for i in vismap:
    for j in i:
        if j != 0: count = count + 1

print("Part 1:", count)

#for i in vismap:
#    print(i)

#map = [ [ 3, 0, 3, 7, 3],
#        [ 2, 5, 5, 1, 2],
#        [ 6, 5, 3, 3, 2],
#        [ 3, 3, 5, 4, 9],
#        [ 3, 5, 3, 9, 0] ]

#vismap = [[0] * len(map[0]) for i in range(len(map))]

def scenic_score(x, y):
    originheight = map[y][x]
    # count up
    visu = 0
    visd = 0
    visl = 0
    visr = 0
    ty = y - 1
    while ty >= 0:
        visu = visu + 1
        if map[ty][x] >= originheight:
            break
        ty = ty - 1
    # count down
    ty = y + 1
    while ty < len(map):
        visd = visd + 1
        if map[ty][x] >= originheight:
            break
        ty = ty + 1
    # count left
    tx = x - 1
    while tx >= 0:
        visl = visl + 1
        if map[y][tx] >= originheight:
            break
        tx = tx - 1
    # count right
    tx = x + 1
    while tx < len(map[0]):
        visr = visr + 1
        if map[y][tx] >= originheight:
            break
        tx = tx + 1
    return (visu , visd , visl , visr)

vismax = 0
for y in range(len(map)):
    for x in range(len(map[y])):
        vistmp = scenic_score(x, y)
        vismap[y][x] = vistmp
        visscore = (vistmp[0] * vistmp[1] * vistmp[2] * vistmp[3])
        if visscore > vismax:
            vismax = visscore

#for i in map:
#    print(i)
#print()
#for i in vismap:
#    print(i)

print("Part 2:", vismax)
# 5764801 too high
# 6000099 too high



