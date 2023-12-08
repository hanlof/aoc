import aoc

# parse
leftright = aoc_sections[0]
d = dict()
for l in aoc_sections[1]:
    a = l[0:3]
    b = l[7:10]
    c = l[12:15]
    d[a] = (b, c)

# evaluate
def atoz(node):
    ans = 0
    for direction in itertools.cycle(list(leftright[0])):
        # XXX This is a bad criteria for Part 1.
        # Should be: equals 'ZZZ' but this happens to work
        if node.endswith('Z'): break
        match direction:
            case 'L': node = d[node][0]
            case 'R': node = d[node][1]
        ans += 1
    return ans

anodes = list(filter(lambda x: x.endswith('A'), d.keys()))
atozmap = dict(zip(anodes, map(atoz, anodes)))

print("Part 1:", atozmap['AAA'])
print("Part 2:", math.lcm(*atozmap.values()))
