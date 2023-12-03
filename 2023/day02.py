import re
lines = open("2").read().splitlines()
tot1 = tot2 = 0
p1_conditions = dict(red=12, blue=14, green=13)
default_colordict = lambda: dict(red=0, blue=0, green=0)
offsets = [(x, y*1j) for x in [-1, 0, 1] for y in [-1, 0, 1]]
for game in lines:
    # Game 100: 9 blue, 18 green, 4 red; 5 green, 10 blue, 11 red; 1 green, 1 red; 16 green, 5 red, 1 blue
    m = re.match("Game (\d+):( .*)", game)
    gamenumber = int(m.group(1))
    min_cubes = default_colordict()
    possible = True
    for samplestring in re.findall(r" (\d[^;]+);?", m.group(2)):
        samplecolors = default_colordict()
        for col in re.findall(r"((\d+) (red|blue|green))+", samplestring):
            samplecolors[col[2]] = int(col[1])
        for n in default_colordict().keys():
            if samplecolors[n] > p1_conditions[n]: possible = False # p1
            min_cubes[n] = max(min_cubes[n], samplecolors[n]) # p2
    tot1 += gamenumber if possible else 0
    tot2 += min_cubes['red'] * min_cubes['blue'] * min_cubes['green'] # p2

print("Part 1:", tot1)
print("Part 2:", tot2)

# Part 1: 2268
# Part 2: 63542

