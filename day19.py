import sys
import operator
import itertools
import re
import time
import multiprocessing
import aoc

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

def haspotential(minutes, georobots, geodes, highest):
    # a simple while with integer variables is way faster than
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

def recurse(minutesleft, robots, resources, skipped, unlocked, globalstate):
    if minutesleft == 0: return resources[GEO]
    # throw away resources if we don't have enough minutes left to possibly spend them. improves cache hits!
    globalstate["maxrobots"][ORE] = max(globalstate["maxrobots"][ORE], robots[ORE])
    globalstate["maxrobots"][CLAY] = max(globalstate["maxrobots"][CLAY], robots[CLAY])
    globalstate["maxrobots"][OBSI] = max(globalstate["maxrobots"][OBSI], robots[OBSI])
    globalstate["maxrobots"][GEO] = max(globalstate["maxrobots"][GEO], robots[GEO])
    resources[ORE] = min(resources[ORE], globalstate["possiblespendingcache"][minutesleft][ORE])
    resources[CLAY] = min(resources[CLAY], globalstate["possiblespendingcache"][minutesleft][CLAY])
    resources[OBSI] = min(resources[OBSI], globalstate["possiblespendingcache"][minutesleft][OBSI])
    cachekey = (minutesleft,) + tuple(robots) + tuple(resources)
    if cachekey in globalstate["cachedres"]:
        return globalstate["cachedres"][cachekey]
    if not haspotential(minutesleft, robots[GEO], resources[GEO], globalstate["bestresult"]):
        globalstate["cachedres"][cachekey] = 0
        return 0
    if globalstate["latestrobotat"][OBSI] > minutesleft and robots[OBSI] == 0:
        return 0
    if globalstate["latestrobotat"][CLAY] > minutesleft and robots[CLAY] == 0:
        return 0
    choices = 0
    for i in ORE, CLAY, OBSI, GEO:
        for j in [ORE, CLAY, OBSI, GEO]:
            if resources[j] < globalstate["costs"][i][j]:
                choices |= (1 << i)
                break
    choices ^= 0b11111
    if (choices & unlocked) == unlocked: choices &= 0b11110
    if robots[CLAY] == 0 and (0b00100 & choices): choices &= 0b11110
    # HUGE optimization. We can't buy whatever we skipped last round
    # (must be saving for something else or otherwise we should have bought it ASAP)
    choices &= (skipped ^ 0b11111)
    if globalstate["highestcosts"][ORE]  == robots[ORE]:  choices &= 0b11101
    if globalstate["highestcosts"][CLAY] == robots[CLAY]: choices &= 0b11011
    if not (minutesleft > 1): choices &= 0b01111
    if not (minutesleft > 3): choices &= 0b10111
    if not (minutesleft > 5): choices &= 0b11011
    if not (minutesleft > 7): choices &= 0b11101

    if   choices & 0b10000: choices = 0b10000
    elif choices & 0b01000: choices = 0b01001
    geo = 0
    for c in [c for c in [NONE, GEO, OBSI, CLAY, ORE] if (1 << c) & choices]:
        newresources = list(resources)
        newresources[ORE]  += robots[ORE]  - globalstate["costs"][c][ORE]
        newresources[CLAY] += robots[CLAY] - globalstate["costs"][c][CLAY]
        newresources[OBSI] += robots[OBSI] - globalstate["costs"][c][OBSI]
        newresources[GEO]  += robots[GEO]  - globalstate["costs"][c][GEO]
        newrobots = list(robots)
        if c == NONE:
            skipped |= (choices & 0b11110)
        else:
            skipped = 0
            newrobots[c] += 1
            unlocked |= 1 << (c + 1)
        #print("Minute", minutesleft, "choices", choices, "chosing", c, "resources", newresources, "robots", newrobots)
        g  = recurse(minutesleft - 1, newrobots, newresources, skipped, unlocked, globalstate)
        geo = max(g, geo)
    globalstate["cachedres"][cachekey] = geo
    globalstate["bestresult"] = max(globalstate["bestresult"], geo)
    return geo

bestresult = 0
highestcosts = [0, 0, 0, 0, 0]

def runbp(n, minutes):
    tim = aoc.Timing(str(n))
    cachedres = dict()
    costs = blueprints[n]
    highestcosts = list(map(max, zip(*costs)))
    possiblespendingcache = dict()
    for i in range(1, 33):
        possiblespendingcache[i] = list(map(operator.mul, highestcosts, itertools.repeat(i - 1)))
    latestpossibleobsi = sum([1 for x in itertools.accumulate(range(minutes)) if x < costs[GEO][OBSI]])
    latestpossibleclay = latestpossibleobsi + sum([1 for x in itertools.accumulate(range(minutes)) if x < costs[OBSI][CLAY]])
    bestresult = 0
    timing = False
#    for i in range(1, 33):
        #       possiblespendingcache[i][CLAY] //= 2
    globalstate =  { "bestresult": bestresult,
                     "highestcosts": highestcosts,
                     "possiblespendingcache": possiblespendingcache,
                     "costs": costs,
                     "maxrobots": [0, 0, 0, 0, 0],
                     "cachedres": cachedres,
                     "latestrobotat": [0, 0, latestpossibleclay, latestpossibleobsi, 0],
                     "choicescount": { 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
                     }

    if n == 3 and minutes == 32: globalstate["bestresult"] = 4
    if n == 2 and minutes == 32: globalstate["bestresult"] = 3

    geo = recurse(minutes, [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], 0, 0b00110, globalstate)
    tim.add(str(n))
    #tim.print()
    #print("%-2d" % n, "%.3f" % (tim.timestamps[-1][1] - tim.timestamps[-2][1]), "%-2d" % minutes, "%-2d" % geo, globalstate["maxrobots"], costs)
    if 'robots' in globalstate:
        print(globalstate['robots'])
    return geo

runbp(1, 17)
#sys.exit()

if __name__ == "__main_":
    CURSORLEFT = "\x1b[50D"
    totalgeodes = dict()
    for i in blueprints:
        lastone = len(blueprints)
        print(CURSORLEFT, "Part 1: ? %d/%d" % (i, lastone), sep="", end="", flush=True)
        totalgeodes[i] = runbp(i, 24)
        print(">>>", i, totalgeodes[i])
    print(CURSORLEFT, "                  ", CURSORLEFT, sep="", end="")

    print("Part 1:", sum([k * v for k, v in totalgeodes.items()]))

    # part 2 runs up to 32nd minute but only for BP 1, 2 and 3
    geo =  runbp(1, 32)
    geo *= runbp(2, 32)
    geo *= runbp(3, 32)
    print("Part 2:", geo)

# threading does not save time, but multiprocessing do!
def runbpwrapper( tup ):
    return runbp( tup[0], tup[1] )

t=aoc.Timing("Times")
#with aoc.Spinner():
with multiprocessing.Pool(4) as p:
    res = p.map(runbpwrapper, [(1, 32), (2, 32), (3, 32)] + [(i + 1, 24) for i in range(30)], 1)
t.add("Done")

print("Part 1:", sum(itertools.starmap(operator.mul, [(n + 1, k) for n, k in enumerate(res[3:])])))
print("Part 2:", res[0] * res[1] * res[2])

#print(aoc.htmlanswers())

