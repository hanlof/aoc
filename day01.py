import sys

inputfile = open("input01")
allinput = inputfile.readlines()

parsedinput = [[]]
for i in allinput:
    if i == '\n':
        parsedinput.append([])
        continue
    parsedinput[-1].append(int(i))

parsedinput.sort(key=lambda a: sum(a))
print("Day 1: Calorie Counting")
print("Part 1:", sum(parsedinput[-1]))
print("Part 2:", sum(list(map(sum, parsedinput))[-3:]))
