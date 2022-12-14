import sys

print(__file__)

#inputfile = sys.stdin
inputfile = open("input01")
allinput = inputfile.readlines()

section = 0
parsedinput = []
parsedinput.append([])

for i in allinput:
    if i == '\n':
        section = section + 1
        parsedinput.append([])
        continue
    parsedinput[section].append(int(i))

biggest = 0
for i in parsedinput:
    summa = sum(i)
    if summa > biggest:
        biggest = summa


parsedinput.sort(key=lambda a: sum(a))

print(sum(list(map(lambda a: sum(a), parsedinput))[-3:]))
