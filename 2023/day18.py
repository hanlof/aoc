import aoc
import heapq
import bisect

dirletters = "RDLU"
dirnumbers = list(range(0, 4))
posdeltas = [1, 1j, -1, -1j]
posturns = list(itertools.pairwise((itertools.islice(itertools.cycle(dirnumbers), 0, 5))))
negturns = list(itertools.pairwise((itertools.islice(itertools.cycle(reversed(dirnumbers)), 0, 5))))
turnmap = dict(zip(posturns, itertools.repeat(1)))
turnmap.update(dict(zip(negturns, itertools.repeat(-1))))

class Segment:
    bystartpos = dict()
    prevseg = None
    prevdir = None
    totrot = 0
    curpos = 0
    totremoved = 0
    def __str__(s):
        if s.ymin == s.ymax:
            return str(s.ymin)
        else:
            return str(s.xmin)
    def __repr__(s):
        return s.__str__()
    def __init__(self, line):
        d, l = re.match("(\w) (\d+)", line).groups()
        l2, d2 = re.match("\w \d+ \(#(\w{5})(\d)", line).groups()
        l2 = int(l2, 16)
        d2 = int(d2)

        self.len = int(l) # p1
        self.len = l2 # p2

        dirnum = dict(zip(dirletters, dirnumbers))[d]
        dirnum = d2 # p2
        if Segment.prevdir is not None:
            Segment.totrot += turnmap[(Segment.prevdir, dirnum)]

        Segment.prevdir = dirnum

        self.dir = dirnum

        posdelta = int(self.len) * posdeltas[dirnum]
        self.startpos = Segment.curpos
        Segment.bystartpos[Segment.curpos] = self
        Segment.curpos += posdelta
        self.endpos = Segment.curpos
        if Segment.curpos in Segment.bystartpos: # final segment
            self.next = Segment.bystartpos[Segment.curpos]
            Segment.totrot += turnmap[(dirnum, self.next.dir)]
            self.next.prev = self
        self.prev = Segment.prevseg
        if self.prev is not None:
            self.prev.next = self
        Segment.prevseg = self
        self.xmin = min(int(self.startpos.real), int(self.endpos.real))
        self.xmax = max(int(self.startpos.real), int(self.endpos.real))
        self.ymin = min(int(self.startpos.imag), int(self.endpos.imag))
        self.ymax = max(int(self.startpos.imag), int(self.endpos.imag))

    def tryremove(self):
        p, n = self.prev, self.next
        posturn = [turnmap[(s1.dir, s2.dir)] == 1 for s1, s2 in itertools.pairwise([p.prev, p, self, n, n.next])]
        match posturn, (p.len < n.len) - (n.len < p.len):
            case [False, True, True, False], shortest:
                #print("YEAH", shortest)
                pass
            case [True, True, True, False], -1:
                #print("mkey")
                pass
            case [False, True, True, True], 1:
                #print("mkay")
                pass
            case _:
                return False
        length = min(p.len, n.len) # -1 makes sense because the inner most coordinate is not removed
        p1 = self.startpos
        p2 = self.endpos + (length * posdeltas[n.dir])
        x1, x2 = int(p1.real), int(p2.real)
        y1, y2 = int(p1.imag), int(p2.imag)
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)

        for i in Segment.bystartpos.values():
            if xmin <= i.startpos.real <= xmax:
                if ymin <= i.startpos.imag <= ymax:
                    if i is not p.prev and i is not p and i is not n and i is not n.next and i is not self:
                        # if there's any segment within the area to be removed and it's not self or next or prev then we skip removing the segment
                        #print("### whatttt ###")
                        #draw(xmin - 2, ymin - 2, xmax + 2, ymax + 2)
                        #print(xmin, xmax, ymin, ymax)
                        #print(i.startpos.real, i.startpos.imag)
                        return False
        area = (self.len + 1) * length
        Segment.totremoved += area

        del1 = p.prev.startpos
        del2 = p.startpos
        del3 = self.startpos
        del4 = n.startpos
        del5 = n.next.startpos

        p.len -= length
        p.endpos = p.startpos + p.len * posdeltas[p.dir]
        n.len -= length
        n.startpos = n.endpos - n.len * posdeltas[n.dir]

        assert p.startpos == p.endpos or n.startpos == n.endpos

        if p.endpos == p.startpos:
            # prev has shrunk to 0
            # => remove prev and prevprev and extend self to start of prevprev
            p.prev.prev.next = self
            self.prev = p.prev.prev
            self.startpos = self.prev.endpos
            self.len += p.prev.len
            self.endpos = self.startpos + self.len * posdeltas[self.dir]
            self.next.startpos = self.endpos
        if n.startpos == n.endpos:
            # next has shrunk to 0
            # => remove next and nextnext and extend self to end of nextnext
            n.next.next.prev = self
            self.next = n.next.next
            self.endpos = self.next.startpos
            self.len = self.len + n.next.len
            self.startpos = self.endpos - self.len * posdeltas[self.dir]
            self.prev.endpos = self.startpos

        del(Segment.bystartpos[del1])
        del(Segment.bystartpos[del2])
        del(Segment.bystartpos[del3])
        del(Segment.bystartpos[del4])
        del(Segment.bystartpos[del5])

        Segment.bystartpos[self.startpos] = self
        Segment.bystartpos[self.prev.prev.startpos] = self.prev.prev
        Segment.bystartpos[self.prev.startpos] = self.prev
        Segment.bystartpos[self.next.startpos] = self.next
        Segment.bystartpos[self.next.next.startpos] = self.next.next

        assert self.startpos.real == self.endpos.real or self.startpos.imag == self.endpos.imag, (self.startpos, self.endpos)

def draw(x1, y1, x2, y2):
    covered = dict()
    for p, seg in Segment.bystartpos.items():
        match seg.dir:
            case 0:
                for x in range(int(seg.startpos.real), int(seg.endpos.real + 1)):
                    covered[(int(seg.startpos.imag), int(x))] = "#"
            case 2:
                for x in range(int(seg.endpos.real), int(seg.startpos.real + 1)):
                    covered[(int(seg.startpos.imag), int(x))] = "#"
            case 1:
                for y in range(int(seg.startpos.imag), int(seg.endpos.imag)):
                    covered[(int(y), int(seg.startpos.real))] = "#"
            case 3:
                for y in range(int(seg.endpos.imag), int(seg.startpos.imag)):
                    covered[(int(y), int(seg.startpos.real))] = "#"
    for y in range(y1, y2):
        for x in range(x1, x2):
            c = "."
            #if x in range(168,173): c = "#"# and y in range(-10, 10): c = "#"
            #else: c = "."
            if (y, x) in covered:
                print(c, sep="", end="")
            else:
                print(" ", sep="", end="")
        print()


curpos = 0
for line in aoc_inputlines:
    s = Segment(line)

visited = set()
s = Segment.bystartpos[0]
n = 1

while len(Segment.bystartpos) > 4:
    s.tryremove()
    visited.add(s)
    s = s.next
    n += 1

# find ANY x, y values as a starting point for getting min/max
for i in Segment.bystartpos.values():
    xmin = min(i.startpos.real, i.endpos.real)
    xmax = max(i.startpos.real, i.endpos.real)
    ymin = min(i.startpos.imag, i.endpos.imag)
    ymax = max(i.startpos.imag, i.endpos.imag)
    break

for i in Segment.bystartpos.values():
    xmin = min(xmin, i.endpos.real)
    xmax = max(xmax, i.startpos.real)
    ymin = min(ymin, i.endpos.imag)
    ymax = max(ymax, i.startpos.imag)

xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

# XXX TODO maybe get rid of bystartpos if it is really only used for checking how many segments are left
#        -- we only really need a handle to the "first" segment and then they can be iterated using .next

area = (xmax - xmin + 1) * (ymax - ymin + 1)
print("Ans:        ", Segment.totremoved + area)
print("Correct Ans: 54058824661845")

