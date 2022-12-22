import sys
import re

print(__file__)

class XY():
    def __init__(s, x, y):
        s.x = x; s.y = y
        s.dist = 0
    def __str__(s):
        return "%7d/%-7d" % (s.x, s.y)
    def __repr__(s):
        return "%7d/%-7d" % (s.x, s.y)
    def mdist(s, o):
        return abs(o.x - s.x) + abs(o.y - s.y)
    def setnearest(s, o):
        s.dist = abs(o.x - s.x) + abs(o.y - s.y)
    def covers(s, y):
        return (s.y - s.dist) <= y <= (s.y + s.dist)
    def coversat(s, y):
        if not (s.y - s.dist) <= y <= (s.y + s.dist):
            return None
        ydist = abs(s.y - y)
        return [(s.x - s.dist + ydist), (s.x + s.dist - ydist)]

#inputfile = sys.stdin
inputfile = open("input15")
allinput = inputfile.readlines()
sensors = list()
beacons = list()

lines = list()
for i in allinput:
    r = re.findall("(-?\d+)", i)
    sensors.append(XY(int(r[0]), int(r[1])))
    beacons.append(XY(int(r[2]), int(r[3])))
    sensors[-1].setnearest(beacons[-1])

# It is pretty inefficient to remove/reinsert intervals like in this code
# It would be better to improve the logic so that it considers multiple
# intervals at the same time and not one at a time

# Also clipping the range to 0..4M would probably simplify all calculations
class Intervals():
    def __init__(s):
        s.intervals = []
    def __str__(s):
        return str(s.intervals)
    def __repr__(s):
        return str(s.intervals)
    def add( self, start, end ):
        updated = None
        updatedidx = 0
        for idx, i in zip(range(len(self.intervals)), self.intervals):
            if i[0] <= start <= i[1] and end > i[1]: # new one overlaps the end of cur
                i[1] = end
                updated = i
                updatedidx = idx
                break
            if i[0] <= end <= i[1] and start < i[0]: # new one overlaps the start of cur
                i[0] = start
                updated = i
                updatedidx = idx
                break
            if start <= i[0] and end >= i[1]: # new one eats up current interval
                i[0] = start
                i[1] = end
                updated = i
                updatedidx = idx
                break
            if start >= i[0] and end <= i[1]: # new one is completely inside current
                updated = i
                updatedidx = idx
                break
        if updated is None:
            self.intervals.append( [start, end] )
        else:
            # remove and reinsert the updated interval in case it the changed
            # interval overlaps more intervals
            #del self.intervals[updatedidx]
            #self.add(updated[0], updated[1])
            pass

inter = Intervals()
for i in sensors:
    interv = i.coversat(2000000)
    if interv is not None:
        inter.add( interv[0], interv[1] )

beacons_at20M = set([b.x for b in beacons if b.y==2000000])
print(beacons_at20M)
print(inter.intervals)
print([a[1] - a[0] + 1 for a in inter.intervals])
# XXX must remove all beacons from this number before delivering answer
print(sum([a[1] - a[0] + 1 for a in inter.intervals]))
ans = sum([a[1] - a[0] + 1 for a in inter.intervals]) - len(beacons_at20M)
print("Part 1:", ans)

# 2686239 is the ylevel for Part 2
# 3316868 is the x coordinate for Part 2

import cProfile, pstats, io
from pstats import SortKey
pr = cProfile.Profile()
pr.enable()

for ylevel in range(0, 10000):
    inter = Intervals()
    for i in sensors:
        interv = i.coversat(ylevel)
        if interv is not None:
            inter.add( interv[0], interv[1] )
    if (ylevel % 100000) == 0:
        print(ylevel)
    if (len(inter.intervals) > 1):
        print(">>>", ylevel)
        print(inter.intervals)
        print([a[1] - a[0] + 1 for a in inter.intervals])
        print(sum([a[1] - a[0] + 1 for a in inter.intervals]))
pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())


#print("###")
#sensors2 = list([XY(10, 10), XY(30, 10)])
#sensors2[0].setnearest(XY(10, 11))
#sensors2[1].setnearest(XY(30, 28))
#inter = Intervals()
#for s in sensors2:
#    interv = s.coversat(10)
#    if interv is not None:
#        inter.add( interv[0], interv[1] )

#print(sensors2[1])
#print( sensors2[1].coversat(10))
#print(inter.intervals)
#print([a[1] - a[0] + 1 for a in inter.intervals])
#print(sum([a[1] - a[0] + 1 for a in inter.intervals]))

for i in sensors:
    print("Dist:", i.dist)
