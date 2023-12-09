import aoc

def extrapolate(hist):
    assert len(hist) > 0
    if all(map(lambda x: x == 0, hist)):
        return [0] + hist + [0]
    else:
        nextlevel = extrapolate([b - a for a, b in itertools.pairwise(hist)])
        return [hist[0] - nextlevel[0]] + hist + [nextlevel[-1] + hist[-1]]

histories = [[int(s) for s in re.findall("-?\d+", l)] for l in aoc_inputlines]
extrapolated = list(map(extrapolate, histories))

print("Part 1:", sum([t[-1] for t in extrapolated]))
print("Part 2:", sum([t[0] for t in extrapolated]))
