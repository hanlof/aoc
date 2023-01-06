import sys
import re

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
    def intersect(s, o):
        intervaltop = o.coversat(s.y - s.dist)
        intervalbot = o.coversat(s.y + s.dist)
        intervalmid = o.coversat(s.y)
        covers = 0
        if intervaltop is not None and intervaltop[0] <= s.x <= intervaltop[1]:
            covers |= 1 # TOP
        if intervalbot is not None and intervalbot[0] <= s.x <= intervalbot[1]:
            covers |= 2 # BOT
        if intervalmid is not None and intervalmid[0] <= (s.x - s.dist) <= intervalmid[1]:
            covers |= 4 # LEFT
        if intervalmid is not None and intervalmid[0] <= (s.x + s.dist) <= intervalmid[1]:
            covers |= 8 # RIGHT
        if covers == 0:
            return None
        elif covers == 15:
            return None
        elif covers == 1|4:
            pass
            #print("covers topleft")
        elif covers == 1|8:
            pass #print("covers topright")
        elif covers == 2|4:
            pass #print("covers botleft")
        elif covers == 2|8:
            pass #print("covers botright")
        elif covers == 1:
            p1 = (s.y - s.dist) + ((intervaltop[1] - s.x) // 2)
            p2 = (s.y - s.dist) + ((s.x - intervaltop[0]) // 2)
            return (p1, p2)
        elif covers == 2:
            p1 = (s.y + s.dist) - ((intervalbot[1] - s.x) // 2)
            p2 = (s.y + s.dist) - ((s.x - intervalbot[0]) // 2)
            return (p1, p2)
        elif covers == 4:
            dy = o.y - s.y
            px = o.x + o.dist
            tx1 = px + dy
            tx2 = px - dy
            dx1 = s.x + s.dist - tx1
            dx2 = s.x + s.dist - tx2
            return (s.y - (dx2 // 2), s.y + (dx1 // 2))

        elif covers == 8:
            dy = o.y - s.y
            px = o.x - o.dist
            tx1 = px - dy
            tx2 = px + dy
            dx1 = s.x + s.dist - tx1
            dx2 = s.x + s.dist - tx2
            return (s.y - (dx2 // 2), s.y + (dx1 // 2))

        else:
            assert False, "not implemented covering pattern"
            print("WHAT")


inputfile = open("inputdata/input15")
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
        for idx, i in enumerate(self.intervals):
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
            del self.intervals[updatedidx]
            self.add(updated[0], updated[1])
            pass

inter = Intervals()
for i in sensors:
    interv = i.coversat(2000000)
    if interv is not None:
        inter.add( interv[0], interv[1] )

beacons_at2M = set([b.x for b in beacons if b.y==2000000])
lengths = [a[1] - a[0] + 1 for a in inter.intervals]
# must remove all beacons from the sum of lengths to get the correct answer
ans = sum(lengths) - len(beacons_at2M)
print("Part 1:", ans)


def visualiseshapes():
    s1 = XY(-3, -5)
    s1.setnearest(XY(2, 0))
    s2 = XY(2, 7)
    s2.setnearest(XY(7, 2))
    for y in range(-12, 12):
        print("%-3d" % y, end="")
        for x in range(-20, 20):
            cov1 = s1.coversat(y)
            cov2 = s2.coversat(y)
            if cov1 is not None and x in cov1:
                print("#", end="")
            elif cov2 is not None and x in cov2:
                print("@", end="")
            else:
                print(" ", end="")
        print("")
    print(s2.intersect(s1))

# for part 2 it takes a long time to calculate all intervals for 4 million lines
# but holes in the coverage can only happen near intersections between coverages
# so find intersections and look at +/1 one line from those
inter = Intervals()
intersections = list()
for i in sensors:
    for j in sensors:
        lines = i.intersect(j)
        if lines is not None:
            intersections.append(lines[0])
            intersections.append(lines[1])

for ylevel in intersections:
    if not (0 <= ylevel <= 4000000): continue
    for delta in [-1, 0, +1]:
        inter = Intervals()
        for i in sensors:
            interv = i.coversat(ylevel + delta)
            if interv is not None:
                inter.add( interv[0], interv[1] )
        if (len(inter.intervals) > 1):
            #print("Found a hole at y =", ylevel + delta)
            inter.intervals.sort()
            #print(inter.intervals[0][1], inter.intervals[1][0])
            x1 = inter.intervals[0][1]
            x2 = inter.intervals[1][0]
            part2x = x1 + 1
            part2y = ylevel + delta
            print("Part 2:", part2x * 4 * 1000 * 1000 + part2y)
            sys.exit(0)

# 2686239 is the ylevel for Part 2
# 3316868 is the x coordinate for Part 2


