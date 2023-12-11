import aoc

galaxies        = [(x, y) for y, l in enumerate(aoc_inputlines) for x, c in enumerate(l) if c == "#"]
yexpansiontable = list(itertools.accumulate([0 if "#" in l else 1 for l in aoc_inputlines]))
xexpansiontable = list(itertools.accumulate([0 if "#" in l else 1 for l in zip(*aoc_inputlines)]))
expanded        = lambda g, f: [(x + xexpansiontable[x] * f, y + yexpansiontable[y] * f) for x, y in g]
sumdist         = lambda l: sum([abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in l])
print("Part 1:", sumdist(itertools.combinations(expanded(galaxies, 1), 2)))
print("Part 2:", sumdist(itertools.combinations(expanded(galaxies, 999999), 2)))

# Lessons learned:
# 1000 * 1000 should have been 999999. it was supposed to be "multiplied by 1 million" and not "add 1 million"!
# effed up a for loop where i used enumerate but forgot to expand 2 values
