import operator
import itertools

trans={"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
def sn2int(sn):
    return sum(map(operator.mul, map(lambda n: trans[n], reversed(sn)), map(operator.pow, itertools.repeat(5), itertools.count(0))))


d = { "1=-0-2":      1747,
        "12111":     906,
        "2=0=":      198,
        "21":        11,
        "2=01":      201,
        "111":       31,
        "20012":     1257,
        "112":       32,
        "1=-1=":     353,
        "1-12":      107,
        "12":        7,
        "1=":        3,
        "122":       37,
        "22":       12,
        "1--":       19}

for k, v in d.items():
    print(sn2int(k), "\t", k, "\t", (sn2int(k) % 5), sn2int(k) == v)
# 33448434171005
# 302875106592253
print("---")
_sum = 0
for i in open("inputdata/input25").readlines():
    #print(sn2int(i[:-1]))
    _sum = _sum + sn2int(i[:-1])

print(_sum)

import itertools as I2
import itertools as I3
I=itertools
s = _sum
accumulated = 0
answer = list()
while accumulated != s:
    for i in I.count(0):
        curvalue = (5 ** i)
        halfcur = curvalue // 2
        upper = accumulated + (curvalue * 2 + halfcur)
        lower = accumulated + (curvalue * -2 - halfcur)
        #print(i, curvalue, (s), lower, upper)
        if lower <= (s) <= upper:
            print("  ", i, "s:", s, "within", lower, lower + curvalue, 0, upper - curvalue, upper)
            output = (s - lower) // ((upper - lower) // 5)
            output -= 2
            accumulated += (output * curvalue)
            answer.append(output)
            print("  outputting:", output, "worth ", curvalue * output)
            break
    # s -= (output * curvalue)

print(answer)

trans2={2: "2", 1: "1", 0: "0", -1: "-", -2: "="}
st = ""
for i in answer:
    print(trans2[i], end="")
    st = st + trans2[i]
print("")
print(sn2int("1-20--11-00--122-=1"))
print("----")
print(st, sn2int(st))

print(s)

print(sn2int("2---1010-0=1220-=010"))
# 2---1010-0=1220-=010 is correct!@! (current solution not outputing zeroes....)
