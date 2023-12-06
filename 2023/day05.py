import aoc

example="""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

#aoc_sections = aoc.sections(example.splitlines())
#print(aoc_sections)
seeds = list(map(int, re.findall(r"\d+", aoc_sections[0][0])))

mapcollections = list()
pointcollections = list()
pointsdicts = list()
for i in aoc_sections[1:]:
    maps = list()
    points = list()
    for m in i[1:]:
        dst, src, length = [int(s) for s in re.findall(r"\d+", m)]
        maps.append( {"dst": dst, "src": src,
                      "len": length, "diff": dst - src,
                      "srcrange": range(src, src + length) } )
        points.append( { "point": src, "diff": dst - src } )
        points.append( { "point": src + length, "diff": 0 } )
    #print("Pb", points)
    pointsdict = dict()
    for p in points:
        #print(p)
        if p['point'] in pointsdict:
            #print("is in:")
            if pointsdict[p['point']] == 0:
                #print("  is 0", pointsdict[p['point']])
                pointsdict[p['point']] = p['diff']
            else:
                if p['diff'] != 0:
                    assert False, (p , pointsdict[p['point']])
        else:
            pointsdict[p['point']] = p['diff']
    #print("Pa", pointsdict)
    mapcollections.append(maps)
    pointcollections.append(points)
    pointsdicts.append(pointsdict)


def seed_to_loc(tmp):
    for mapcollection in mapcollections:
        for m in mapcollection:
            if tmp in m['srcrange']:
                tmp += m['diff']
                break
    return tmp


# expect a range and return the lowest location corresponding to any val in range
def seed_range_to_loc(tmp):
    print("calling seed_range...")
    ranges = [tmp]
    assert type(tmp) == range

    for pointsdict in pointsdicts:
        newranges = list()
        for r in ranges:
            print("XX", r)
            prevdiff = 0
            assert r.start < r.stop
            # det uppstår ett problem om start redan finns i points.
            # då ignoreras den befintliga punkten som behövde finnas där för att
            # applicera en korrekt diff.
            # på något vis behöver befintlig 'diff' sparas när man lägger in start/stop
            # måste start/stop behandlas utanför POINTS-listan?

            # assert r.start not in pointsdict
            # pointsdict[r.start] = "START"
            # assert r.stop not in pointsdict
            # pointsdict[r.stop] = "STOP"
            print("POINTSCOLLECTION", sorted(pointsdict))
            foundstart = False
            for start, stop in itertools.pairwise(sorted(pointsdict)):
                startdiff, stopdiff = pointsdict[start], pointsdict[stop]
                assert start != stop
                #print(start, stop, startdiff, stopdiff)
                if r.start in range(start, stop) and r.stop in range(start, stop):
                    print("found START and STOP")
                    newranges.append(range(r.start + startdiff, r.stop + startdiff))
                    break
                elif r.start in range(start, stop):
                    print("found START and STOP")
                    newranges.append(range(r.start + startdiff, stop + startdiff))
                    foundstart = True
                    continue
                elif r.stop in range(start, stop):
                    print("found STOP")
                    newranges.append(range(start + startdiff, r.stop + startdiff))
                    break
                elif foundstart:
                    print("found range within range'")
                    newranges.append(range(start + startdiff, stop + startdiff))
                """
                if startdiff == "START":
                    foundstart = True
                    print("found >>> START", start, stop, startdiff, stopdiff)
                    print("> RANGE:", r)
                    newranges.append(range(start + prevdiff, stop + prevdiff))
                    print("> ADDING", start + prevdiff, stop + prevdiff)
                    if stopdiff == "STOP":
                        print("--- found STOP", start, stop)
                        break
                    continue
                if stopdiff == "STOP":
                    print("found STOP", start, stop)
                    newranges.append(range(start + startdiff, stop + startdiff))
                    print("> ADDING", start + startdiff, stop + startdiff)
                    break
                if foundstart:
                    print("found range", startdiff, start, stop)
                    newranges.append(range(start + startdiff, stop + startdiff))
                    print("> ADDING", start + startdiff, stop + startdiff)
                prevdiff = startdiff
                """
            #del(pointsdict[r.start])
            #del(pointsdict[r.stop])
        ranges = newranges
        print("doing another mapping with ranges", ranges)
    return ranges
m = map(seed_to_loc, seeds)
print("Part 1:", min(m))


print("Seed ranges", [range(s, s + l) for s, l in zip(seeds[0::2], seeds[1::2])])
m = map(seed_range_to_loc, [range(s, s + l) for s, l in zip(seeds[0::2], seeds[1::2])])
#seed_range_to_loc(range(10))
l = list(m)
print(">>>>", l)
a = list()
for i in l:
    for j in i:
        print(j)
        a.append(j.start)
print(min(a))
print(sorted(a))
# 0 is not right
# 52210644
# 52210644
# 83874316 too high
# 64639870 too low
