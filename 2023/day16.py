import aoc

def parsemap(lines):
    ysize = len(lines)
    xsize = len(lines[0])
    coords = dict()
    for y, line in enumerate(lines):
        assert len(line) == xsize
        for x, c in enumerate(line):
            coords[y * 1j + x] = c
    return ((ysize, xsize), coords)

size, field = parsemap(aoc_inputlines)

directions = (1, 1j, -1, -1j) # right, down, left, up
bouncemap = {
    ('/', 0): 3,  ('/',  1): 2, ('/',  2): 1, ('/',  3): 0,
    ('\\', 0): 1, ('\\', 1): 0, ('\\', 2): 3, ('\\', 3): 2}

def addlight(field, coord, direction):
    if coord not in field:
        field[coord] = set()
    field[coord] |= {direction}

def tracebeam(field, curpos, curdir, outputfield):
    while True:
        if curpos not in field: break
        if curpos in outputfield:
            if curdir in outputfield[curpos]: break
        addlight(outputfield, curpos, curdir)
        match field[curpos]:
            case "/" | "\\":
                curdir = bouncemap[(field[curpos], curdir)]
            case "|":
                tracebeam(field, curpos + 1j, 1, outputfield)
                curdir = 3
            case "-":
                tracebeam(field, curpos + 1, 0, outputfield)
                curdir = 2
        curpos += directions[curdir]


lightmap = dict()
tracebeam(field, (0 + 0j), 0, lightmap)
print("Part 1:", len(lightmap.values()))

maxene = 0
# left edge
for y in range(size[0]):
    lightmap = dict()
    tracebeam(field, (0 + y * 1j), 0, lightmap)
    maxene = max(maxene, len(lightmap))

# right edge
for y in range(size[0]):
    lightmap = dict()
    tracebeam(field, (109 + y * 1j), 2, lightmap)
    maxene = max(maxene, len(lightmap))

# top edge
for x in range(size[1]):
    lightmap = dict()
    tracebeam(field, (x + 0j), 1, lightmap)
    maxene = max(maxene, len(lightmap))

# bottom edge
for x in range(size[1]):
    lightmap = dict()
    tracebeam(field, (x + 109j), 3, lightmap)
    maxene = max(maxene, len(lightmap))

print("Part 2:", maxene)
