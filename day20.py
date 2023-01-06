inputlines = open("inputdata/input20").readlines()
l = list(map(int, inputlines))
#l = [1, 2, -3, 3, -2, 0, 4]

def mix(l, times):
    t = list(range(len(l)))
    if len(l) < 20:
        print("Init:", l)
    for i in range(times):
        for i in range(len(l)):
            steps = l[i]
            assert i in t, t[:10]
            pos = t.index(i)
            newpos = (pos + steps) % (len(l) - 1)

            t.pop(pos)
            t.insert(newpos, i)

            l2 = list([l[i] for i in t])
            if len(l) < 20 and times == 1:
                print("     ", l2)
    return t

def groovecoords(t, l):
    reordered = list([l[i] for i in t])
    zeropos = reordered.index(0)
    c1 = reordered[(zeropos + 1000) % len(t)]
    c2 = reordered[(zeropos + 2000) % len(t)]
    c3 = reordered[(zeropos + 3000) % len(t)]
    print("grove", c1, c2, c3)
    return c1 + c2 + c3


t = mix(l, 1)
print("Part 1:", groovecoords(t, l))

KEY = 811589153
l2 = list(map(lambda a: a * KEY, l))
t = mix(l2, 10)
print("Part 2:", groovecoords(t, l2))


# 6640 is correct!
# 11908 too high
# 6517 too low
