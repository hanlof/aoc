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
p2str = aoc.bigletterstostring(picture)

print("Part 1:", signalstrength)
print("Part 2:", p2str)

