import aoc

def mix(l, times):
    t = list(range(len(l)))
    while times > 0:
        for i, steps in enumerate(l):
            pos = t.index(i)
            newpos = (pos + steps) % (len(l) - 1)
            t.pop(pos)
            t.insert(newpos, i)

        times -= 1
    return t

def groovecoords(t, l):
    reordered = list([l[i] for i in t])
    zeropos = reordered.index(0)
    c1 = reordered[(zeropos + 1000) % len(t)]
    c2 = reordered[(zeropos + 2000) % len(t)]
    c3 = reordered[(zeropos + 3000) % len(t)]
    #print("grove", c1, c2, c3)
    return c1 + c2 + c3


l = list(aoc.getinput(conv=int))
t = mix(l, 1)
print("Part 1:", groovecoords(t, l))

KEY = 811589153
l2 = list(map(lambda a: a * KEY, l))
t = mix(l2, 10)
print("Part 2:", groovecoords(t, l2))


# 6640 is correct!
# 11908 too high
# 6517 too low
