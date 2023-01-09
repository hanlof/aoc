import re, itertools

def update_tail(head, tail):
    dx = head.real - tail.real
    signx = (dx > 0) - (dx < 0)
    dy = head.imag - tail.imag
    signy = 1j * ((dy > 0) - (dy < 0))
    if (abs(dx) > 1) or (abs(dy) > 1):
        tail += signx + signy
    return tail

movements = {"U": -1j, "D": 1j, "L": -1, "R": 1}
def simrope(ropelen, moves):
    positions, rope = set(), [0 + 0j for _ in range(ropelen)]
    for move in moves:
        r = re.match("(?P<dir>.) (?P<count>\d+)", move)
        for i in range(int(r['count'])):
            rope[0] += movements[r['dir']]
            for n, p in enumerate(itertools.pairwise(rope)):
                rope[n + 1] = update_tail(*p)
            positions.add(rope[-1])
    return len(positions)

print("Day 9: Rope simulations")
allinput = open("inputdata/input09").readlines()
print("Part 1:", simrope(2, allinput))
print("Part 2:", simrope(10, allinput))



