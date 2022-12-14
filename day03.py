import sys

print(__file__)

#inputfile = sys.stdin
inputfile = open("input03")
allinput = inputfile.readlines()

priosum = 0
for i in allinput:
    l = int(len(i) / 2)
    f = i[0:l]
    s = i[-(l+1):-1]
    space = " " * (25 - l) * 2
    same = set(f) & set(s)
    asc = ord(list(same)[0])
    if asc < 97:
        prio = asc - 65 + 27
    else:
        prio = asc - 97 + 1

    print("'%s' %s' %s' %s %d" % (f, space, s, same, prio))
    priosum = priosum + prio

print("Part 1:", priosum)

priosum = 0
for i in range(2, len(allinput), 3):

    same = set(allinput[i-2]) & set(allinput[i-1]) & set(allinput[i])
    same = filter(lambda c: c != '\n', same)
    asc = ord(list(same)[0])
    if asc < 97:
        prio = asc - 65 + 27
    else:
        prio = asc - 97 + 1

    print("'%s' %s' %s' %s %d" % (allinput[i-2], allinput[i-1], allinput[i], same, prio))
    priosum = priosum + prio

print("Part2:", priosum)
