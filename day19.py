import sys
import operator
import itertools
import re
import time
import multiprocessing

# Not enough minerals....

# Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 3 ore and 13 obsidian.
# Blueprint 14: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 10 clay. Each geode robot costs 2 ore and 7 obsidian.

NONE, ORE, CLAY, OBSI, GEO = range(5)

costs = [ [0, 0, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 10, 0, 0], [ 0, 2, 0, 7, 0 ] ] # Blueprint 14

#costs = [ [0, 0, 0, 0, 0], [ 0, 3, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 18, 0, 0], [ 0, 3, 0, 13, 0 ] ]
#costs = [ [0, 0, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 11, 0, 0], [ 0, 4, 0, 12, 0 ] ]
#resources = [0] * 5
#robots = [0] * 5
#robots[ORE] = 1

blueprints=dict()
allinput = open("inputdata/input19").readlines()
for l in allinput:
    r = re.search("^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian\..*", l)
    bpindex = int(r[1])
    orecost = [ 0, int(r[2]), 0, 0, 0 ]
    claycost = [ 0, int(r[3]), 0, 0, 0 ]
    obsicost = [ 0, int(r[4]), int(r[5]), 0, 0 ]
    geodcost = [ 0, int(r[6]), 0, int(r[7]), 0 ]
    blueprints[bpindex] = [ [0, 0, 0, 0, 0], orecost, claycost, obsicost, geodcost ]

def potentialgeodes(m, rob, res, highest):
    robrange = itertools.islice(itertools.count(rob), m)
    r = 0
    for i in itertools.accumulate(robrange):
        r = i + res
        if r > highest:
            return r
    return r

def haspotential(minutes, georobots, geodes, highest):
    # a simple while with integer variables is way faster than
    # itertools.accumulate(itertools.islice(itertools.count(...), ...) etc
    geodes += georobots # unrolling the loop once seems to improve efficiency slightly
    if geodes > highest: return True
    georobots += 1
    minutes -= 1
    while minutes > 0:
        geodes += georobots
        if geodes > highest: return True
        georobots += 1
        minutes -= 1
    return False

def minutestogeo(cost, rob, obsi):
     robiter = itertools.count(rob)
     totobsi = itertools.accumulate(robiter, initial=obsi)
     acclist = itertools.takewhile(lambda o: o < cost, totobsi)
     count = 0
     sum([1 for _ in acclist])
     return count

#In [156]: 17 * 31 * 40


def recurse(minutesleft, robots, resources, skipped, globalstate):
    # first make a choice and spend
    # then robots collect
    # then building robots finishes
    if minutesleft == 0: return resources[GEO]
    # throw away resources if we don't have enough minutes to possibly spend them
    # to improve cache hits. this is a slight improvement
    if resources[CLAY] >= globalstate["possiblespendingcache"][minutesleft][CLAY]:
        resources[CLAY] = globalstate["possiblespendingcache"][minutesleft][CLAY]
    if resources[ORE] >= globalstate["possiblespendingcache"][minutesleft][ORE]:
        resources[ORE] = globalstate["possiblespendingcache"][minutesleft][ORE]
    if resources[OBSI] >= globalstate["possiblespendingcache"][minutesleft][OBSI]:
        resources[OBSI] = globalstate["possiblespendingcache"][minutesleft][OBSI]
    # running without cache is not an option. a single blueprint takes > 5 seconds
    cachekey = (minutesleft,) + tuple(robots) + tuple(resources)
    if cachekey in globalstate["cachedres"]:
        #coveredsearchspace += 5 ** minutesleft
        return globalstate["cachedres"][cachekey]
    # using minutestogeo loses time. too much computing for the saving
    #mintogeo = -1 - minutestogeo(costs[GEO][OBSI], robots[OBSI], resources[OBSI])
    #potgeo = potentialgeodes(minutesleft, robots[GEO], resources[GEO], bestresult)
    if not haspotential(minutesleft, robots[GEO], resources[GEO], globalstate["bestresult"]):
        globalstate["cachedres"][cachekey] = 0
        #coveredsearchspace += 5 ** minutesleft
        return 0

    choices = set()
    for i in range(5):
        canbuy = True
        for j in range(5):
            if resources[j] < globalstate["costs"][i][j]:
                canbuy = False
                break
        if canbuy: choices.add(i)
    #if not GEO in choices and not GEO in robots and not haspotential(minutesleft - 1, 0, 0, bestresult): return 0
    if resources[CLAY] >= globalstate["possiblespendingcache"][minutesleft][CLAY]:
        choices -= {CLAY}
    if resources[ORE] >= globalstate["possiblespendingcache"][minutesleft][ORE]:
        choices -= {ORE}
    if resources[OBSI] >= globalstate["possiblespendingcache"][minutesleft][OBSI]:
        choices -= {OBSI}
    if choices.issuperset({ORE,CLAY,OBSI,GEO}):
        choices -= {NONE}

    # Big optimization. Can't do the same for ORE or OBSI unfortunately
    # Doing the same for GEO is at best a very slight improvement
    if CLAY not in robots and CLAY in choices: choices -= {NONE}
    # HUGE optimization. We can't buy whatever we skipped last round
    # (must be saving for something else or otherwise we should have bought it ASAP)
    choices -= skipped
    if globalstate["highestcosts"][ORE] <= robots[ORE]: choices -= {ORE}
    if globalstate["highestcosts"][CLAY] <= robots[CLAY]: choices -= {CLAY}
    if globalstate["highestcosts"][OBSI] <= robots[OBSI]: choices -= {OBSI}
    #if GEO not in robots and GEO in choices:
    #    choices -= {NONE}
    geo = 0
    # this specific ordering improves runtime
    for c in GEO, OBSI, CLAY, ORE, NONE:
        if not c in choices:
            #coveredsearchspace += 5 ** (minutesleft - 1)
            continue
        newresources = list(resources)
        newrobots = list(robots)
        newresources[ORE] = newresources[ORE] + newrobots[ORE] - globalstate["costs"][c][ORE]
        newresources[CLAY] = newresources[CLAY] + newrobots[CLAY] - globalstate["costs"][c][CLAY]
        newresources[OBSI] = newresources[OBSI] + newrobots[OBSI] - globalstate["costs"][c][OBSI]
        newresources[GEO] = newresources[GEO] + newrobots[GEO] - globalstate["costs"][c][GEO]
        newrobots[c] = newrobots[c] + 1
        newresources[0] = 0
        newrobots[0] = 0
        if c == NONE: skipped |= choices - {NONE}
        else: skipped = set()
        g  = recurse(minutesleft - 1, newrobots, newresources, skipped, globalstate)
        if g > geo: geo = g

    globalstate["cachedres"][cachekey] = geo

    if geo > globalstate["bestresult"]:
        globalstate["bestresult"] = geo
    return geo

bestresult = 0
highestcosts = [0, 0, 0, 0, 0]

def runbp(n, minutes):
    cachedres = dict()
    fastestobsidian = 0
    fastestgeo = 0
    costs = blueprints[n]
    highestcosts = list(map(max, zip(*costs)))
    possiblespendingcache = dict()
    for i in range(1, 33):
        possiblespendingcache[i] = list(map(operator.mul, highestcosts, itertools.repeat(i)))
    bestresult = 0
    searchspace = 5 ** minutes
    coveredsearchspace = 1
    percentsearchspace = 0
    timing = False
    if timing: starttime = time.time()
    globalstate =  { "percentsearchspace": percentsearchspace,
                     "coveredsearchspace": coveredsearchspace,
                     "searchspace": searchspace,
                     "bestresult": bestresult,
                     "possiblespendingcache": possiblespendingcache,
                     "highestcosts": highestcosts,
                     "costs": costs,
                     "cachedres": cachedres,
                     "fastestobsidian": fastestobsidian,
                     "fastestgeo": fastestgeo }


    geo = recurse(minutes, [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], set(), globalstate)
    if timing: print("Time: %.2f" % (time.time() - starttime))
    return geo

totalgeodes = dict()
"""
    if inp == bytes(b'\x1b[A'): print("UP")
    if inp == bytes(b'\x1b[D'): print("LEFT")
    if inp == bytes(b'\x1b[B'): print("DOWN")
    if inp == bytes(b'\x1b[C'): print("RIGHT")
"""
CURSORLEFT = "\x1b[50D"

if __name__ == "__main_":
    for i in blueprints:
        lastone = len(blueprints)
        print(CURSORLEFT, "Part 1: ? %d/%d" % (i, lastone), sep="", end="", flush=True)
        totalgeodes[i] = runbp(i, 24)
        print(">>>", i, totalgeodes[i])
    print(CURSORLEFT, "                  ", CURSORLEFT, sep="", end="")

    print("Part 1:", sum([k * v for k, v in totalgeodes.items()]))

    # part 2 runs up to 32nd minute but only for BP 1, 2 and 3
    print(CURSORLEFT, "Part 2: ? %d/%d" % (0, 3), sep="", end="", flush=True)
    geo =  runbp(1, 32)
    print(CURSORLEFT, "Part 2: ? %d/%d" % (1, 3), sep="", end="", flush=True)
    geo *= runbp(2, 32)
    print(CURSORLEFT, "Part 2: ? %d/%d" % (2, 3), sep="", end="", flush=True)
    geo *= runbp(3, 32)
    print(CURSORLEFT, "                  ", CURSORLEFT, sep="", end="", flush=True)
    print("Part 2:", geo)

# threading does not save time, but multiprocessing do!
def runbpwrapper( tup ):
    return runbp( tup[0], tup[1] )

print([(1, 32), (2, 32), (3, 32)] + [(i + 1, 24) for i in range(30)])
with multiprocessing.Pool(8) as p:
    res = p.map(runbpwrapper, [(1, 32), (2, 32), (3, 32)] + [(i + 1, 24) for i in range(30)])

print(res[3:])
print("Multi part1:", sum(itertools.starmap(operator.mul, [(n + 1, k) for n, k in enumerate(res[3:])])))
print("Multi part2:", res[0] * res[1] * res[2])

# TODO! a bit too long runtime. maybe discard paths where there's not enough time left to make enough obsi robots to collect enough obsidian to make a single geo robot

