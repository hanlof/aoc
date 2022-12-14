import sys
import re

print(__file__)

#inputfile = sys.stdin
inputfile = open("input06")
allinput = inputfile.readlines()

line=allinput[0]
for i in range(0, len(line)):
    if len(set((line[i:i+4]))) == 4:
        print("Part 1:", i+4)
        break

for i in range(0, len(line)):
    if len(set((line[i:i+14]))) == 14:
        print("Part 2:", i+14)
        break


