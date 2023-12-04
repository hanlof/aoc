import sys

print("Day 3: Rucksack Reorganization")

allinput = open("inputdata/input03").read().splitlines()

def getprio(c):
    lettervalue = ord(c)
    if lettervalue < 97: return lettervalue - ord('A') + 27
    else: return lettervalue - ord('a') + 1

priosum = 0
for i in allinput:
    halflength = len(i) // 2
    firsthalf = set(i[0:halflength])
    secondhalf = set(i[-halflength:])
    same = firsthalf & secondhalf
    priosum += getprio(same.pop())
print("Part 1:", priosum)

priosum = 0
i = iter(allinput)
while True:
    try:
        a, b, c = next(i), next(i), next(i)
        same = set(a) & set(b) & set(c)
        priosum += getprio(same.pop())
    except:
        break
print("Part 2:", priosum)

