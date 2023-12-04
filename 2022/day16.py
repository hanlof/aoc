import sys
import re
import copy
import itertools
import sys
import aoc

class Tunnel():
    def __init__(s, length):
        s.src = None
        s.dst = None
        s.length = length
    def __str__(s):
        return "T<%s->%s %s>" % (s.src.name, s.dst.name, str(s.length))
    def __repr__(s):
        return "T<%s->%s %s>" % (s.src.name, s.dst.name, str(s.length))

class VTunnel(Tunnel):
    def __init__(s, length, rate):
        s.length = length
        s.rate = rate
    def __str__(s):
        return "T<%s->%s %s %s>" % (s.src.name, s.dst.name, str(s.length), str(s.rate))
    def __repr__(s):
        return "T<%s->%s %s %s>" % (s.src.name, s.dst.name, str(s.length), str(s.rate))
    def __eq__(s, o):
        return s.src.name == o.src.name and s.dst.name == o.dst.name and s.length == o.length and s.rate == o.length
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        s = ("%s%s%s%s" % (self.src.name, self.dst.name, str(self.length), str(self.rate))).__hash__()
        return s

class Valve():
    def __init__(self, name, rate):
        self.name = name
        self.rate = int(rate)
        self.tunnels = list()
    def removedst(self, valve):
        self.tunnels = list(filter(lambda t: t.dst is not valve, self.tunnels))
    def __str__(s):
        return "V<%s %d (%s)>" % (s.name, s.rate, str(s.tunnels))
    def __repr__(s):
        return "V<%s %d (%s)>" % (s.name, s.rate, str(s.tunnels))


level = 0
class System():
    def __init__(self, inputstr):
        self.valves = dict()
        self.tunnels = dict()
        self.cacheddistances = dict()
        self.valvesbynum = list()
        for inputline in inputstr:
            # parse text input
            r = re.match("Valve (\w\w).*rate=(\d+).*valves? (((, )?(\w\w))+)", inputline)
            # make valve object
            self.valves[r[1]] = Valve(r[1], r[2])
            # make tunnel objects
            for tunnelstr in re.findall("\w\w", r[3]):
                self.tunnels[(r[1], tunnelstr)] = Tunnel(1)
        # Create all the connections
        for (s, d), t in self.tunnels.items():
            fromvalve = self.valves[s]
            tovalve = self.valves[d]
            t.src = fromvalve
            t.dst = tovalve
            fromvalve.tunnels.append(t)

    def copy(self):
        return copy.deepcopy(self)

    def connect(self, v1, v2, rate):
        newt = Tunnel(rate)
        newt.src = self.valves[v1]
        newt.dst = self.valves[v2]
        self.valves[v1].tunnels.append(newt)
        newt = Tunnel(rate)
        newt.src = self.valves[v2]
        newt.dst = self.valves[v1]
        self.valves[v2].tunnels.append(newt)

    def removevalve(self, name):
        valve = self.valves[name]
        valves = [t.dst for t in valve.tunnels]
        for v in valves:
            v.removedst(valve)
        for v1, v2 in itertools.product(valves, valves):
            if v1 is v2:
                continue
            newlen = list(filter(lambda v: v.dst is v1, valve.tunnels))[0].length
            newlen = newlen + list(filter(lambda v: v.dst is v2, valve.tunnels))[0].length
            newt = Tunnel(newlen)
            newt.src = v1
            newt.dst = v2
            l = [t for t in v1.tunnels if t.dst is newt.dst]
            if len(l) == 0:
                v1.tunnels.append(newt)
            elif len(l) == 1:
                shortest = l[0].length if l[0].length < newt.length else newt.length
                l[0].length = shortest
            else:
                print("ERROR! 789")
                sys.exit(1)
        del(self.valves[name])

    def checkoptions(self, vname, minutes):
        global level
        global count
        level = level + 1
        self.makedot("play/s%d.dot" % count, mark=vname)
        valve = self.valves[vname]
        if len(valve.tunnels) == 0:
            #print("TIME UP!")
            return 2
        if minutes <= 0: return 0
        s = 2 # open valve
        newsystem = self.copy()
        newsystem.removevalve(vname)
        count = count + 1
        if len(newsystem.valves) == 1:
            level = level - 1
            return 0
        s = s + sum(map(lambda t: newsystem.checkoptions(t.dst.name, minutes - t.length - 1), valve.tunnels))
        s = s + sum(map(lambda t: newsystem.checkoptions(t.dst.name, minutes - t.length), valve.tunnels))
        level = level - 1
        return s

    def makedot(self, fname, mark=""):
        with open(fname, "w+") as dotfile:
            dotfile.write("digraph new_graph {\n")
            for i in self.valves.values():
                dotfile.write("%s [label=\"%s %d\" %s]\n" % (i.name, i.name, i.rate, "color=red" if mark==i.name else "color=black"))
                for j in i.tunnels:
                    if (type(j) is VTunnel):
                        dotfile.write("%s -> %s [label=\"%s %s\"];\n" % (i.name, j.dst.name, str(j.length), str(j.rate)))
                    else:
                        dotfile.write("%s -> %s [label=\"%s\"];\n" % (i.name, j.dst.name, str(j.length)))
            dotfile.write("}\n")

    def shortestpathsbynum(self, v1num):
        if v1name in self.cacheddistances:
            return self.cacheddistances[v1name]
        v1 = self.valves[v1name]
        visited = dict({v1.name: 0})
        queue = list(v1.tunnels)
        while len(queue) > 0:
            tun = queue[0]
            shortest = visited[tun.src.name] + tun.length
            shortestidx = 0
            for i in range(len(queue)):
                candidate = queue[i]
                candlen = visited[candidate.src.name] + candidate.length
                if candlen < shortest:
                    shortest = candlen
                    shortestidx = i
            tun = queue.pop(shortestidx)

            newlen = visited[tun.src.name] + tun.length
            if not tun.dst.name in visited:
                queue.extend(tun.dst.tunnels)
            if tun.dst.name in visited:
                if visited[tun.dst.name] > newlen:
                    visited[tun.dst.name] = newlen
            else:
                visited[tun.dst.name] = newlen
        self.cacheddistances[v1name] = visited
        return visited

    def shortestpaths(self, v1name):
        if v1name in self.cacheddistances:
            return self.cacheddistances[v1name]
        v1 = self.valves[v1name]
        visited = dict({v1.name: 0})
        queue = list(v1.tunnels)
        while len(queue) > 0:
            tun = queue[0]
            shortest = visited[tun.src.name] + tun.length
            shortestidx = 0
            for i in range(len(queue)):
                candidate = queue[i]
                candlen = visited[candidate.src.name] + candidate.length
                if candlen < shortest:
                    shortest = candlen
                    shortestidx = i
            tun = queue.pop(shortestidx)

            newlen = visited[tun.src.name] + tun.length
            if not tun.dst.name in visited:
                queue.extend(tun.dst.tunnels)
            if tun.dst.name in visited:
                if visited[tun.dst.name] > newlen:
                    visited[tun.dst.name] = newlen
            else:
                visited[tun.dst.name] = newlen
        self.cacheddistances[v1name] = visited
        return visited

    def shortestpath(self, v1name, v2name):
        return self.shortestpaths(v1name)[v2name]

easyinput = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
inputfile = open("inputdata/input16")
allinput = inputfile.readlines()

#s = System(easyinput.split("\n"))
s = System(allinput)

s.makedot("play/b.dot", "AA")

# Remove zero valves
for i in [v.name for v in s.valves.values() if v.rate == 0 and v.name != "AA"]:
    s.removevalve(i)

s.makedot("play/a.dot", "AA")
cachedres4 = dict()
def recurse4(queue, system, minutes, visitednodes):
    # first find what name/minute pair to work with
    if (len(visitednodes) == 6): print("6")
    if (len(visitednodes) == 5): print("5")
    if (len(visitednodes) == 4): print("4")
    if (len(visitednodes) == 3): print("3")
    if (len(visitednodes) == 2): print("222")
    if (len(visitednodes) == 1): print("1111111")
    assert type(queue) is list
    assert len(queue) == 2, queue
    assert max([m[1] for m in queue]) <= minutes, (queue, minutes)
    visitednodes.append(queue[0][0])
    visitednodes.append(queue[1][0])
    if queue[0][1] == minutes:
        vname = queue[0][0]
        queue = [ queue[1] ]
    else:
        vname = queue[1][0]
        queue = [ queue[0] ]
    assert len(queue) == 1, str(queue)
    if minutes <= 0: return 0
    curvault = system.valves[vname]
    if curvault.rate > 0: minutes = minutes - 1
    paths = dict(system.shortestpaths(vname))
    for visited in visitednodes:
        if visited in paths:
            del(paths[visited])
    cachekey = tuple(paths.items()) + (minutes, queue[0][1], queue[0][0])
    if len(paths) == 1:
        if minutes >= 1:
            return (minutes) * curvault.rate
        else:
            return 0
    if len(visitednodes) < 12:
        if cachekey in cachedres4:
            return cachedres4[cachekey]
    highestscore = 0
    for v in paths.items():
        q = list(queue)
        q.append((v[0], minutes - v[1]))
        nextminute = max([m[1] for m in q])
        r = recurse4(q, system, nextminute, list(visitednodes))
        if r > highestscore:
            highestscore = r
    if len(visitednodes) < 8:
        cachedres4[cachekey] = highestscore
    return highestscore + curvault.rate * (minutes)

enumeratedvalves = dict()
for n, vname in enumerate(s.valves):
    enumeratedvalves[vname] = n
cres = None
cachedres = dict()
def recurse3(vname, system, minutes, visitednodes, accumulatedvalue):
    if minutes <= 0:
        if minutes == 0:
            cachedres[tuple(visitednodes) + (vname, minutes,)] = (accumulatedvalue, 0)
        return 0
    curvalve = system.valves[vname]
    if curvalve.rate > 0: minutes = minutes - 1
    paths = dict(system.shortestpaths(vname))
    visitednodes.append(vname)
    for visited in visitednodes:
        del(paths[visited])
    cachekey = tuple(visitednodes) + (minutes,)
    if cachekey in cachedres:
        return cachedres[cachekey][0]
    ans = 0
    for valve, mins in paths.items():
        if minutes - mins <= 0:
            continue
        r = recurse3(valve, system, minutes - mins, list(visitednodes), accumulatedvalue + curvalve.rate * minutes)
        if r > ans:
            ans = r
    if ans == 0:
        cachedres[tuple(visitednodes) + (0,)] = (ans, accumulatedvalue + curvalve.rate * minutes)

    cachedres[cachekey] = (ans, accumulatedvalue + curvalve.rate * minutes)
    return ans + curvalve.rate * minutes

cachedres = dict()
tim = aoc.Timing("Timing:")
print("Part 1:", recurse3("AA", s, 30, [], 0))

print(len(cachedres))
tim.add("Part 1")
# Part 2 is solved by looking at pairs of cached results that has fully disjoint paths,
# not by checking all combinations, because iterating the combinations of two
# moving 'players' takes hours (with my implementation at least
cachedres = dict()
recurse3("AA", s, 26, [], 0)
tim.add("Redid cache")

usefulsubset = dict()
for key, val in [(a[1:-1], b[1]) for a, b in cachedres.items() if a[-1] == 0 and b[1] > 0]:
    newkey = tuple(set([enumeratedvalves[v] for v in key]))
    tempval = usefulsubset.get(newkey, 0)
    usefulsubset[newkey] = max(tempval, val)


print("Len", len(usefulsubset))
tim.add("Culled data set")
with aoc.Spinner():
    bestcombo = 0
    lowestsingle = 0
    for key1, val1 in usefulsubset.items():
        if val1 < lowestsingle: continue # this one cuts the time REAL good
        for key2, val2 in usefulsubset.items():
            if val1 + val2 > bestcombo:
                if set(key1).isdisjoint(set(key2)):
                    lowestsingle = max(lowestsingle, min(val1, val2))
                    bestcombo = val1 + val2
print("Part 2:", bestcombo)
tim.add("Found disjoint combo")
tim.print()

# TODO: identify valves by number in recurse3 and findshortest!


"""
V<AA 0 ([T<AA->DD 1>, T<AA->II 1>, T<AA->BB 1>])>
V<FF 0 ([T<FF->EE 1>, T<FF->GG 1>])>
V<GG 0 ([T<GG->FF 1>, T<GG->HH 1>])>
V<II 0 ([T<II->AA 1>, T<II->JJ 1>])>
V<CC 2 ([T<CC->DD 1>, T<CC->BB 1>])>
V<EE 3 ([T<EE->FF 1>, T<EE->DD 1>])>
V<BB 13 39([T<BB->CC 1>, T<BB->AA 1>])>
V<DD 20 20 ([T<DD->CC 1>, T<DD->AA 1>, T<DD->EE 1>])>
V<JJ 21 42 ([T<JJ->II 1>])>
V<HH 22 110 ([T<HH->GG 1>])>
"""

