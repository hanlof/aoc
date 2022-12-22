import re
_b = __builtins__

units = set()
maxcoord = [0, 0, 0]
def parse():
    global maxcoord
    inputlines = open("input18").readlines()
    for line in inputlines:
        unit = tuple(map(int, line.split(",")))
        units.add(unit)
        maxcoord = list(map(_b.max, zip(maxcoord, unit)))

def visualize(coords):
    lines = list()
    for i in range(maxcoord[0]):
        lines.append([' '] * 20)

    for z in range(maxcoord[2]):
        lines = list()
        for i in range(maxcoord[0]):
            lines.append([' '] * 20)
        print("   01234567890123456789")
        for x in range(maxcoord[0]):
            for y in range(maxcoord[1]):
                if (x, y, z) in coords: lines[x][y] = chr(97 + z)
            print("%-2d" % x, end=" ")
            for i in lines[x]:
                print(i, end="")
            print()

def allsurface():
    s =  0
    for u in units:
        if not (u[0] - 1, u[1] + 0, u[2] + 0) in units: s = s + 1
        if not (u[0] + 1, u[1] + 0, u[2] + 0) in units: s = s + 1
        if not (u[0] + 0, u[1] - 1, u[2] + 0) in units: s = s + 1
        if not (u[0] + 0, u[1] + 1, u[2] + 0) in units: s = s + 1
        if not (u[0] + 0, u[1] + 0, u[2] - 1) in units: s = s + 1
        if not (u[0] + 0, u[1] + 0, u[2] + 1) in units: s = s + 1
    return s

# Move from cube to the next one step at a time,
# bounded by coordinates -1..21 in all directions,
# making sure we never revisit a cube.
# This algorithm finds the surface area connected to the
# empty space where it was started,
# regardless of where it was started
def outersurface(queue):
    possiblejumps = \
        [( 1, 0, 0), (0,  1, 0), (0, 0,  1),
         (-1, 0, 0), (0, -1, 0), (0, 0, -1)]
    s = 0
    visited = set()
    while len(queue) > 0:
        coord = queue.pop()
        if coord in visited:
            continue
        visited.add(coord)

        for relcoords in possiblejumps:
            n = tuple(map(sum, zip(relcoords, coord)))
            if n in units:
                s = s + 1
            elif _b.min(*n) >= -1 and _b.max(*n) <= 21 and not n in visited:
                queue.append(n)
    return s

parse()
print("Input size:", len(units))
print("Max x, y, z:", *maxcoord)
print("Part 1:", allsurface())
print("Part 2:", outersurface( [ (1, 1, 1) ] ))


