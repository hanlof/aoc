import aoc

maxy = 0
mapset = set()
for i in aoc.getinput():
    a=[(int(x), int(y)) for x, y in re.findall("(\d+),(\d+)", i)]
    maxy = max(a + [(0, maxy)], key=lambda a: a[1])[1]
    for (x1, y1), (x2, y2) in itertools.pairwise(a):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                mapset.add( (x, y) )

wallset = set(mapset)
fastset = set()
def printmap():
    minx = min(fastset, key=lambda x: x[0])[0]
    maxx = max(fastset, key=lambda x: x[0])[0]
    miny = min(fastset, key=lambda x: x[1])[1]
    #maxy = max(fastset, key=lambda x: x[1])[1]
    for y in range(miny, maxy + 1):
        for x in range(minx - 1, maxx + 2):
            if (x, y) in fastset: print(".", end="")
            elif (x, y) in wallset: print("#", end="")
            elif (x, y) in mapset: print("o", end="")
            else: print(" ", end="")
        print("")

# Part 1: flow sand until one sand falls below lowest wall block
count = 0
done = 0
while not done:
    sx = 500
    sy = 0
    while True:
        sy = sy + 1
        if sy > maxy:
            done = 1
            break
        if (sx, sy) in mapset:
            if (sx - 1, sy) in mapset and (sx + 1, sy) in mapset:
                mapset.add( (sx, sy - 1) )
                count = count + 1
                break
            elif not (sx - 1, sy) in mapset:
                sx = sx - 1
            elif not (sx + 1, sy) in mapset:
                sx = sx + 1
print("Part 1:", count)

# Part 2. Calculate sand spread by letting each line (starting from the top)
# contain sand wherever the previous line has sand AND in the squares to the
# left and right of each of those coordinates except wherever there are walls.
# It works beautifully and runs way faster than placing each sand block!
sandsquares = { 500 }
ylevel = 0
while ylevel < (maxy + 2):
    fastset |= set( [(x, ylevel) for x in sandsquares] )
    for x in list(sandsquares):
        sandsquares |= { x - 1, x, x + 1 }
    ylevel += 1
    wallbricks = set([i for i in range(min(sandsquares), max(sandsquares) + 1) if (i, ylevel) in wallset])
    sandsquares -= wallbricks
print("Part 2:", len(fastset))

# slow solution. moves each sand block one step at a time as in the AoC description
# kept for comparison and nostalgia :-)
mapset = set(wallset)
def slowpart2():
    count = 0
    with aoc.Spinner():
        # Part 2
        done = 0
        while not done:
            sx = 500
            sy = 0
            while True:
                sy = sy + 1
                if sy == (maxy + 3):
                    mapset.add( (sx, sy - 1) )
                    break
                if (sx, sy) in mapset:
                    if (sx - 1, sy) in mapset and (sx + 1, sy) in mapset:
                        mapset.add( (sx, sy - 1) )
                        count = count + 1
                        if sy == 1:
                            done = 1
                        break
                    elif not (sx - 1, sy) in mapset:
                        sx = sx - 1
                    elif not (sx + 1, sy) in mapset:
                        sx = sx + 1
    print("Slow Part 2:", count)
