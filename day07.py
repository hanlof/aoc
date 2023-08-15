import aoc

class Directory():
    def __init__(s):
        s.this = 0
        s.tot = 0

allinput = aoc.getinput()
dirsizes = dict()
curpath = "/"
for i in allinput:
    r = re.search("\$ cd (.*)", i)
    if r:
        d = r[1]
        if d == "/":
            curpath = "/"
        else:
            curpath = os.path.realpath(curpath + "/" + d)
        if not curpath in dirsizes:
            dirsizes[curpath] = Directory()
    r = re.match("(\d+).*", i)
    if r:
        dirsizes[curpath].this += int(r[1])
        dirsizes[curpath].tot += int(r[1])
        tmpdir = curpath
        while tmpdir != "/":
            tmpdir = os.path.realpath(tmpdir + "/..")
            dirsizes[tmpdir].tot += int(r[1])

# P1: sum of all directories smaller than 100000
print("Part 1:", sum([d.tot for d in dirsizes.values() if d.tot < 100000]))

# P2: smallest directory that would free up enough space
# DISKSIZE and NEEDSIZE are always just 70000000 and 30000000 but it's kinda cuter to fetch these from html
DISKSIZE = int(aoc.htmlcodeemsections()[1])
NEEDSIZE = int(aoc.htmlcodeemsections()[2])
free = DISKSIZE - dirsizes["/"].tot
mindir = min(filter(lambda d: d.tot > (NEEDSIZE - free), dirsizes.values()), key=lambda d: d.tot)
print("Part 2:", mindir.tot)
