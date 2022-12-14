import sys
import re

print(__file__)

#inputfile = sys.stdin
inputfile = open("input12")
allinput = inputfile.readlines()

# 64 x 41
map = []
for i in allinput:
    print(len(i), i)
    map.append(list(i[0:64]))

for y in range(len(map)):
    for x in range(len(map[y])):
        cur = ord(map[y][x])
        marker = ' '
        if y > 0:
            if ord(map[y - 1][x]) == (cur + 1):
                marker = '|'
            elif ord(map[y - 1][x]) == (cur - 1):
                marker = '|'
            elif ord(map[y - 1][x]) == (cur):
                marker = '|'
            print(marker, end="")
        print(' ', end="")
    print("")
    for x in range(len(map[y])):
        cur = ord(map[y][x])
        marker = ' '
        if x > 0:
            if ord(map[y][x - 1]) == (cur + 1):
                marker = '-'
            elif ord(map[y][x - 1]) == (cur - 1):
                marker = '-'
            elif ord(map[y][x - 1]) == (cur):
                marker = '-'
            print(marker, end="")
        print(map[y][x], end="")
    print("")

# part 2 364 too high
print()
