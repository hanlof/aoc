import sys
import re
import os

print(__file__)

#inputfile = sys.stdin
allinput = open("inputdata/input07").read().splitlines()

dirsizes = {}
path = "/"
for i in allinput:
    r = re.search("\$ cd (.*)", i)
    if r:
        d = r[1]
        if d == "/":
            path = "/"
        else:
            path = os.path.realpath(path + "/" + d)
        print(path)
        if not path in dirsizes:
            dirsizes[path] = {'d': 0, 'i': 0}
    r = re.match("(\d+).*", i)
    if r:
        dirsizes[path]['d'] += int(r[1])
        dirsizes[path]['i'] += int(r[1])
        tmpdir = path
        while tmpdir != "/":
            tmpdir = os.path.realpath(tmpdir + "/..")
            dirsizes[tmpdir]['i'] += int(r[1])
        print(path, dirsizes[path])


print(dirsizes)

print(sum([i[1]['d'] for i in dirsizes.items() if i[1]['d'] <= 100000]))
print("Part 1:", sum([i[1]['i'] for i in dirsizes.items() if i[1]['i'] <= 100000]))

print("--------------")
print(sorted(dirsizes.items(), key=lambda a: a[1]['i'])) # print(a[1]['i']))) # a[1]['i']))

free = 70000000 - dirsizes["/"]['i']
print("Free:", free)
print("Need:", 30000000-free)
#print([i for i in dirsizes.items() if i[1]['d'] <= 100000])

# 11327531 too high (part 2)
