import aoc

p1stacks = [ list() for _ in range(10)]
p2stacks = [ list() for _ in range(10)]
for line in aoc_sections[0]:
    for n, s in [(n, s) for n, s in enumerate(line[1::4]) if s != ' ']:
        p1stacks[n].insert(0, s)
        p2stacks[n].insert(0, s)

for  line in aoc_sections[1]:
    r = re.search("move (?P<howmany>\d+) from (?P<from>\d+) to (?P<to>\d+)", line)
    n, src, dst = int(r['howmany']), int(r['from']) - 1, int(r['to']) - 1
    p1stacks[dst].extend(reversed(p1stacks[src][-n:]))
    del(p1stacks[src][-n:])
    p2stacks[dst].extend(p2stacks[src][-n:])
    del(p2stacks[src][-n:])
print("Part 1:", "".join([s[-1] for s in p1stacks if len(s) > 0]))
print("Part 2:", "".join([s[-1] for s in p2stacks if len(s) > 0]))

