import aoc

stuckrocks = dict()
movingrocks = dict()
#aoc_inputlines = """\
#OOOO.#.O..
#OO..#....#
#OO..O##..O
#O..#.OO...
#........#.
#..#....#.#
#..O..#.O.O
#..O.......
##....###..
##....#....""".splitlines()
def parse():
    rocks = dict()
    for y, l in enumerate(aoc_inputlines):
        rocks[y * 1j - 1] = "%" # the edge
        rocks[y * 1j + 100] = "%"
        for x, c in enumerate(l):
            rocks[-1j + x] = "%" # the edge
            rocks[100j + x] = "%"
            if c != ".":
                rocks[y * 1j + x] = c
    return rocks


def pri():
    for y in range(-1, 102):
        for x in range(-1, 102):
            if y * 1j + x in rocks:
                print(rocks[y * 1j + x], sep="", end="")
            else:
                print(" ", sep="", end="")
        print()

def moveall(r, movement):
    rem = list()
    add = list()
    for coord, c in r.items():
        if c == "O" and coord + movement not in r:
            rem.append(coord)
            add.append( (coord + movement, c) )
    if not add: return 0
    for re in rem:
        del(r[re])
    for ad, c in add:
        assert ad not in r
        r[ad] = c
    return len(add)

"""
%O#  ##    #     OOOOOO#           O#           #    OOO# O#             OOOOOO#  # O#             OO% 
%   O#     OO#O#O#   O##   OO#                   O# OOO## #      OOOO##  # # O#   O#  O#           OO% 
%    O#### #  ## O#             OOOO#             OOOO#     OOOOO# O#      O#   # #   #           OO#% 
%           OOO#    OO# #   O#             OO# #  ###   O# ##   OOO#                OOOOO#O#        #% 
%          OOOOO#   OOO#          OOOO#   O# #     # #     O#   OO#  #       O#  #     #     OO#  # #% 
%   OOOOO#     OOO# OO#  #  OOO# O#    O## O##     # O#  ## ##       O#                OOO# # ##     % 
%#OO#OOO#    OO#  OOOO#  OOO#       OOOO##      OO#        O#         OOOOOO#          O#   #     OOO% 
% O##OO#  #O# #   OOOOOOOOO# O#  OOOOO# O#  O#   OOOOOOOO# O#    OOOOOOOO####    OO# O#    O# O#O# # % 
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
"""


def calcload(r):
    tot = 0
    for coord, rock in r.items():
        if rock == "O":
            tot += (100 - coord.imag)
    return int(tot)

rocks = parse()
while moveall(rocks, -1j) != 0:
    pass
print(calcload(rocks))

rocks = parse()
states = set()
statesafterhit = set()
hits = 0
doublehits = 0
for i in range(1000000000):
    while moveall(rocks, -1j) != 0: pass # north
    while moveall(rocks, -1) != 0: pass  # west
    while moveall(rocks, 1j) != 0: pass  # south
    while moveall(rocks, 1) != 0: pass   # east
    state = tuple([(a, b) for a, b in rocks.items()])
    if state in states:
        hits += 1
        tmp = len(statesafterhit)
        statesafterhit |= {state}
        if len(statesafterhit) == tmp:
            doublehits += 1
        print("HIT", i, doublehits, len(statesafterhit), calcload(rocks), 1000000000 % 21, i % 21)
    states |= {state}
    if (i % 10) == 0:
        print(1000000000 - i)

pri()
print(len(statesafterhit))
print("Part 2:", calcload(rocks))
# 102643 too low
# 102645 too low
# 102655 too low
# 102656 incorrect
# 102657 CORRECT!
# 102660 incorrect
