import aoc

#aoc_inputlines = \
"""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()

BOARDSIZE = len(aoc_inputlines[3]) - 1

heatlossmap = list()
for y, line in enumerate(aoc_inputlines):
    row = list()
    for x, c in enumerate(line):
        row.append(int(c))
    heatlossmap.append(row)

XPOS, YPOS, XSPEED, YSPEED, STEPSLEFT, HEATLOSS = range(6)
stepsleft = 2
heatloss = 0

queue = { (1, 0, 1, 0, stepsleft): (heatloss),
          (0, 1, 0, 1, stepsleft): (heatloss) }
visited = dict()
lowesthl = None
#lowesthl = 3800

def check(s, heatloss):
    global visited
    global queue
    dist = (BOARDSIZE - s[XPOS])
    dist += (BOARDSIZE - s[YPOS])
    if lowesthl and (heatloss + dist) >= lowesthl: return False
    if s[XPOS] < 0: return False
    if s[YPOS] < 0: return False
    if s[XPOS] > BOARDSIZE: return False
    if s[YPOS] > BOARDSIZE: return False
    if s in queue:
        return queue[s] > heatloss + heatlossmap[s[YPOS]][s[XPOS]] > heatlossmap[s[YPOS]][s[XPOS]]


    if (s[XPOS], s[YPOS], s[XSPEED], s[YSPEED], s[STEPSLEFT]) in visited:
        return visited[s] > heatloss + heatlossmap[s[YPOS]][s[XPOS]]
    return True

count = 0
while len(queue) > 0:
    s, heatloss = queue.popitem()
    if not check(s, heatloss): continue
    xpos, ypos, xspeed, yspeed, stepsleft = s
    heatloss += heatlossmap[ypos][xpos]
    visited[ (xpos, ypos, xspeed, yspeed, stepsleft) ] = heatloss
    if xpos == BOARDSIZE and ypos == BOARDSIZE:
        print("DONE", count, len(queue), s, heatloss)
        #print(path)
        if lowesthl == None: lowesthl = heatloss
        if heatloss < lowesthl: lowesthl = heatloss
        continue


    dirchanges = [1j, -1j]
    if stepsleft > 0: dirchanges += [1]
    speed = yspeed * 1j + xspeed
    for diff in dirchanges:
        posdelta = speed * diff
        pos = ypos * 1j + xpos
        pos += posdelta
        _ypos = int(pos.imag)
        _xpos = int(pos.real)
        if diff == 1:
            ts = stepsleft - 1
        else:
            ts = 2
        s2 = (_xpos, _ypos, int(posdelta.real), int(posdelta.imag), ts)
        if not check(s2, heatloss):
            continue
        if len(queue) > 390 * 1000:
            #print("XXX", s2)
            pass
            #exit(0)
        if posdelta.real > 0 or posdelta.imag > 0:
            #queue.append(s2)
            if s2 in queue and queue[s2] <= heatloss + heatlossmap[_ypos][_xpos]:
                continue
            assert (xpos, ypos) != (_xpos, _ypos), [xpos, ypos, _xpos, _ypos, diff, posdelta, pos, ts]
            queue[s2] = heatloss
        else:
            if s2 in queue and queue[s2] <= heatloss + heatlossmap[_ypos][_xpos]:
                continue
            assert (xpos, ypos) != (_xpos, _ypos), [xpos, ypos, _xpos, _ypos, diff, posdelta, pos, ts]
            queue[s2] = heatloss
            #queue.insert(0, s2)

    count += 1
    if count % 50000 == 0:
        print("q", len(queue))
        if len(queue) > 900 * 1000:
            print("too many loops, abort")
            break

# check what space is used in the queue
x, y, dx, dy, l = set(), set(), set(), set(), set()
print("--------------", len(queue))
print("count", count)

# Part 1
# 741 too low

# 745 wrong

# 757 wrong

# 762 wrong

# 770 wrong
# 771 wrong
# 772 too high

# XXX 758 correct!!!!!

