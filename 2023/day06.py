import aoc
from math import sqrt, ceil, floor

def solve(b, c): # solve x^2 + b * x = c
    t = sqrt(b * b - 4 * c) / -2
    return (b/2 + t, b/2 - t)

def valuesabove(b, c): # find number of integers (x) that yields values above c for x*(x-b)
    l, h = solve(b, c)
    return ((ceil(h) - 1) - (floor(l) + 1) + 1)

times = re.findall(r"\d+", aoc_inputlines[0])
dists = re.findall(r"\d+", aoc_inputlines[1])

print("Part 1:", functools.reduce(int.__mul__, map(lambda x: valuesabove(*x), zip(map(int, times), map(int, dists)))))
print("Part 2:", valuesabove(int("".join(times)), int("".join(dists))))
