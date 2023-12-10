import aoc

def extrapolate(seq):
    assert len(seq) > 0
    if all(map(lambda x: x == 0, seq)):
        return [0] + seq + [0]
    else:
        deltas = extrapolate([b - a for a, b in itertools.pairwise(seq)])
        return [seq[0] - deltas[0]] + seq + [deltas[-1] + seq[-1]]

histories = [[int(s) for s in re.findall("-?\d+", l)] for l in aoc_inputlines]
extrapolated = list(map(extrapolate, histories))

print("Part 1:", sum([t[-1] for t in extrapolated]))
print("Part 2:", sum([t[0] for t in extrapolated]))
