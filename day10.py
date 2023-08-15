import aoc


allinput = aoc.getinput()
short = aoc_codeblocks[0]
long = aoc_codeblocks[1]
# allinput = long

x = 1
cycle = 1
queue = list()
picture = [ [] ]
def draw(cycle, x):
    xpos = (cycle % 40) - 1 # why -1?? :O
    if x == xpos or (x - 1) == (xpos) or (x + 1) == (xpos):
        picture[-1].append(1)
    else:
        picture[-1].append(0)

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
        picture.append(list())
    x = x + update
    cycle = cycle + 1
    return ret

for i in allinput:
    r = re.match("(\w+) ?(-?\d+)?", i)
    instr = r[1]
    if r[2]:
        num = int(r[2])
        queue.insert(0, [num, 2])
    else:
        queue.insert(0, [0, 1])

signalstrength = 0
while len(queue) > 0:
    signalstrength = signalstrength + processqueue(">")

del(picture[-1])
print("Part 1:", signalstrength)

LETTERS={
'P': """\
###.
#  #
#  #
###.
#  .
#   """,
'L': """\
#  .
#  .
#  .
#  .
#  .
####""",
'G': """\
 ##.
#  #
#  .
# ##
#  #
 ###""",
'F': """\
####
#  .
###.
#  .
#  .
#  .""",
'K': """\
#  #
# #.
## .
# #.
# #.
#  #""",
'A': """\
 ##.
#  #
#  #
####
#  #
#  #""",
'Z': """\
####
   #
  #.
 # .
#  .
####"""
}

import numpy
pic = numpy.array(picture)
r=numpy.rot90(pic, -1)
o=r.reshape(8,5,6)
letters = dict()
for l, raster in LETTERS.items():
    s = list()
    for y, row in enumerate(raster.splitlines()):
        for x, c in enumerate(row):
            if c == "#": s.append( (y, x) )
    letters[tuple(sorted(s))] = l

print("Part 2: ", end="")
for i in numpy.rot90(o, axes=(1, 2)):
    s = list()
    i = i[:,0:4]
    for y, row in enumerate(i):
        for x, n in enumerate(row):
            if n == 1: s.append( (y, x) )
    print(letters[tuple(sorted(s))], end="")
print("")



#print(pic[:, 0:5])

