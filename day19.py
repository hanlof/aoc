import sys
# Not enough minerals....

# Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 3 ore and 13 obsidian.
# Blueprint 14: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 10 clay. Each geode robot costs 2 ore and 7 obsidian.

NONE, ORE, CLAY, OBSI, GEO = range(5)

costs = [ [0, 0, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 10, 0, 0], [ 0, 2, 0, 7, 0 ] ] # Blueprint 14

#costs = [ [0, 0, 0, 0, 0], [ 0, 3, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 18, 0, 0], [ 0, 3, 0, 13, 0 ] ]
#costs = [ [0, 0, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 4, 11, 0, 0], [ 0, 4, 0, 12, 0 ] ]
resources = [0] * 5
robots = [0] * 5
robots[ORE] = 1

blueprints=dict()
import re
allinput = open("inputdata/input19").readlines()
for l in allinput:
    r = re.search("^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian\..*", l)
    bpindex = int(r[1])
    orecost = [ 0, int(r[2]), 0, 0, 0 ]
    claycost = [ 0, int(r[3]), 0, 0, 0 ]
    obsicost = [ 0, int(r[4]), int(r[5]), 0, 0 ]
    geodcost = [ 0, int(r[6]), 0, int(r[7]), 0 ]
    blueprints[bpindex] = [ [0, 0, 0, 0, 0], orecost, claycost, obsicost, geodcost ]
import operator
import itertools
def recurse(minutesleft, robots, resources):
    global fastestobsidian
    global fastestgeo
    global cachedres
    global costs
    global highestcosts
    possiblespending = list(map(operator.mul, highestcosts, itertools.repeat(minutesleft))) # theoretical max spending until end of time
    #if min(map(operator.gt, resources, highestcosts)) == True:
    #    resources = list(highestcosts)
    if resources[CLAY] >= possiblespending[CLAY]:
        resources[CLAY] = possiblespending[CLAY]
    if resources[ORE] >= possiblespending[ORE]:
        resources[ORE] = possiblespending[ORE]
    if resources[OBSI] >= possiblespending[OBSI]:
        resources[OBSI] = possiblespending[OBSI]

    cachekey = (minutesleft,) + tuple(robots) + tuple(resources)
    #if minutesleft < fastestobsidian:
    #    return 0
    #if minutesleft < fastestgeo and robots[GEO] == 0:
    #   return 0
    if cachekey in cachedres:
        return cachedres[cachekey]
    if minutesleft == 0: return resources[GEO]
    # first make a choice and spend
    # then robots collect
    # then building robots finishes
    choices = set()
    for i in range(5):
        #if min(map(lambda p: p[0]>=p[1], zip(resources, costs[i]))) == True:
        #   choices.add(i)
        canbuy = True
        for j in range(5):
            if resources[j] < costs[i][j]:
                canbuy = False
        if canbuy: choices.add(i)
    #if OBSI in choices:
    #    if minutesleft > fastestobsidian:
    #        fastestobsidian = minutesleft
    #        print("Fastest", fastestobsidian, resources, robots)
    if GEO in choices:
        if minutesleft > fastestgeo:
            fastestgeo = minutesleft
            #print("Fastest", fastestgeo, resources, robots)
    if choices.issuperset({ORE,CLAY,OBSI,GEO}):
        #print("Opti :o", minutesleft, resources, robots)
        choices -= {NONE}
    #if CLAY not in robots and CLAY in choices:
    #    choices -= {NONE} # {CLAY}
    #if OBSI not in robots and OBSI in choices:
    #    choices -= {NONE} # {OBSI}
    if highestcosts[ORE] < robots[ORE]: choices -= {ORE}
    if highestcosts[CLAY] < robots[CLAY]: choices -= {CLAY}
    if highestcosts[OBSI] < robots[OBSI]: choices -= {OBSI}
    #if GEO not in robots and GEO in choices:
    #    choices -= {NONE}
    geo = 0
    #print("M ", "  " * (5 - minutesleft), "C", choices, "R", resources, robots)
    for c in choices:
        newresources = list(resources)
        newrobots = list(robots)
        newresources[ORE] = newresources[ORE] + newrobots[ORE] - costs[c][ORE]
        newresources[CLAY] = newresources[CLAY] + newrobots[CLAY] - costs[c][CLAY]
        newresources[OBSI] = newresources[OBSI] + newrobots[OBSI] - costs[c][OBSI]
        newresources[GEO] = newresources[GEO] + newrobots[GEO] - costs[c][GEO]
        newrobots[c] = newrobots[c] + 1
        newresources[0] = 0
        newrobots[0] = 0
        #print(" S", "  " * (5 - minutesleft), "R", newresources, newrobots)
        g  = recurse(minutesleft - 1, newrobots, newresources)
        if g > geo: geo = g

    cachedres[cachekey] = geo
    return geo

highestcosts = [0, 0, 0, 0, 0]
def runbp(c):
    global cachedres
    cachedres = dict()
    global fastestobsidian
    fastestobsidian = 0
    global fastestgeo
    fastestgeo = 0
    global costs
    costs = c
    global highestcosts
    highestcosts = list(map(max, zip(*costs)))
    print("Running BP", i, "=", costs)
    return recurse(24, [0, 1, 0, 0, 0], [0, 0, 0, 0, 0])


#blueprints.clear()
#blueprints[1] = [ [0, 0, 0, 0, 0], [ 0, 4, 0, 0, 0], [ 0, 2, 0, 0, 0], [ 0, 3, 14, 0, 0], [ 0, 2, 0, 7, 0 ] ] # test input 1
#blueprints[2] = [ [0, 0, 0, 0, 0], [ 0, 2, 0, 0, 0], [ 0, 3, 0, 0, 0], [ 0, 3, 8, 0, 0], [ 0, 3, 0, 12, 0 ] ] # test input 2
totalgeodes = dict()
for i in blueprints:
    geo = runbp(blueprints[i])
    totalgeodes[i] = geo
    print("... BP", i, "GEO", geo)
    #if i > 3: continue

print(totalgeodes.items())
print("Qualuty sum:", sum([k * v for k, v in totalgeodes.items()]))


# TODO! a bit too long runtime. maybe discard paths where there's not enough time left to make enough obsi robots to collect enough obsidian to make a single geo robot
#       maybe discard paths where there's not enough time left to make enough geo robots to collect enough geodes to beat current max ?!

# 1413 is correct!! :D

# Part 2.... runs in several minutes... (need to change 24 to 32 in recurse call in runbp
#Running BP 1 = [[0, 0, 0, 0, 0], [0, 3, 0, 0, 0], [0, 4, 0, 0, 0], [0, 4, 18, 0, 0], [0, 3, 0, 13, 0]]
#... BP 1 GEO 17
#Running BP 2 = [[0, 0, 0, 0, 0], [0, 4, 0, 0, 0], [0, 4, 0, 0, 0], [0, 2, 11, 0, 0], [0, 4, 0, 8, 0]]
#... BP 2 GEO 31
#Running BP 3 = [[0, 0, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 2, 15, 0, 0], [0, 3, 0, 9, 0]]
#... BP 3 GEO 40
#Running BP 4 = [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 2, 0, 0, 0], [0, 2, 8, 0, 0], [0, 2, 0, 14, 0]]
#
#In [156]: 17 * 31 * 40
#Out[156]: 21080
# 21080 is correct!!
