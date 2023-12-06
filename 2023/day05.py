import aoc

pointsdicts = list()
for i in aoc_sections[1:]:
    pointsdict = dict()
    for m in i[1:]:
        dst, src, length = [int(s) for s in re.findall(r"\d+", m)]
        if src in pointsdict:
            assert pointsdict[src] == 0
        pointsdict[src] = dst - src
        if src + length not in pointsdict:
            pointsdict[src + length] = 0
        else:
            assert pointsdict[src + length] != 0
    pointsdicts.append(pointsdict)

# Part 1: 340994526
# Part 2: 52210644

def seed_to_loc(tmp):
    for pointsdict in pointsdicts:
        for start, stop in itertools.pairwise(sorted(pointsdict)):
            if tmp in range(start, stop):
                tmp += pointsdict[start]
                break
    return tmp

# expect a range and return remapped ranges for every part of original range
def seed_range_to_loc(tmp):
    assert type(tmp) == range
    ranges = [tmp]
    for pointsdict in pointsdicts:
        newranges = list()
        for r in ranges:
            prevdiff = 0
            assert r.start < r.stop
            foundstart = False
            for start, stop in itertools.pairwise(sorted(pointsdict)):
                diff = pointsdict[start]
                assert start != stop
                if r.start in range(start, stop) and r.stop in range(start, stop):
                    newranges.append(range(r.start + diff, r.stop + diff))
                    break
                elif r.start in range(start, stop):
                    newranges.append(range(r.start + diff, stop + diff))
                    foundstart = True
                    continue
                elif r.stop in range(start, stop):
                    newranges.append(range(start + diff, r.stop + diff))
                    break
                elif foundstart:
                    newranges.append(range(start + diff, stop + diff))
        ranges = newranges
    return min([r.start for r in ranges])

seeds      = list(map(int, re.findall(r"\d+", aoc_sections[0][0])))
seedranges = [range(start, start + length) for start, length in zip(seeds[0::2], seeds[1::2])]
print("Part 1:", min(map(seed_to_loc, seeds)))
print("Part 2:", min(map(seed_range_to_loc, seedranges)))
