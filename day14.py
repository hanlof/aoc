import sys
import re

print(__file__)

#inputfile = sys.stdin
inputfile = open("input14")
allinput = inputfile.readlines()

# 64 x 41

minx = 1000
maxx = 0
maxy = 0
rocks = []
for i in allinput:
    a=re.findall("(\d+),(\d+)", i)
    l = map(lambda l: map(int, l), a)
    it = iter(l)
    (px, py) = next(it)
    for (x, y) in it:
        if x > maxx: maxx = x
        if x < minx: minx = x
        if y > maxy: maxy = y
        rocks.append( ((px, x), (py, y)) )
        px = x
        py = y

# Part 2 needs a lot of space
minx = minx - 2
maxx = maxx + 2
minx = 500 - 177
maxx = 500 + 177
maxy = maxy
mapx = [ [" "] * (maxx - minx + 1) for i in range(maxy + 3)]
#for ( (x1, y1), (x2, y2) ) in rocks:
#    print(x1,y1,x2,y2)
#
def printmap(m):
    for i in m:
        print("|", end="")
        for j in i:
            print(j, end="")
        print()

for ( (x1, x2), (y1, y2) ) in rocks:
    if x1 > x2: t = x2; x2 = x1; x1 = t
    if y1 > y2: t = y2; y2 = y1; y1 = t
    if x1 == x2: points = ( [(x1, y) for y in range(y1, y2 + 1) ] )
    if y1 == y2: points = ( [(x, y1) for x in range(x1, x2 + 1) ] )
    for x, y in points:
        mapx[y][x - minx] = '#'

mapx[0][500 - minx] = '+'

for i in range(len(mapx[-1])):
    mapx[-1][i] = "#"

printmap(mapx)
free = lambda x, y: mapx[y][x] == ' '
busy = lambda x, y: mapx[y][x] != ' '

# start flowing sand
count = 0
done = 0
while not done:
    sx = 500 - minx
    sy = 0
    while True:
        sy = sy + 1
        if sy > maxy:
            done = 1
            break
        if busy(sx, sy):
            #            print(maxx, sx)
            if busy(sx - 1, sy) and busy(sx + 1, sy):
                mapx[sy - 1][sx] = 'o'
                count = count + 1
                break
            elif free(sx - 1, sy):
                sx = sx - 1
            elif free(sx + 1, sy):
                sx = sx + 1

p1count = count
# Part 2
done = 0
while not done:
    sx = 500 - minx
    sy = 0
    while True:
        sy = sy + 1
        if busy(sx, sy):
            if busy(sx - 1, sy) and busy(sx + 1, sy):
                mapx[sy - 1][sx] = 'o'
                count = count + 1
                if sy == 1:
                    done = 1
                break
            elif free(sx - 1, sy):
                sx = sx - 1
            elif free(sx + 1, sy):
                sx = sx + 1

#printmap(mapx)
print("Part 1:", p1count)
print("Part 2:", count)
print(minx, maxx, maxy)
print(500-175, 500+175, maxy)
