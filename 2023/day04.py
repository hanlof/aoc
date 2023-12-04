import re

ans1 = ans2 = 0
cardhits, cardcache = dict(), dict()
for l in open("4").read().splitlines():
    m = re.match("Card\s+(\d+):([^|]+)\|(.+)$", l)
    hits = set(map(int, re.findall("(\d+)", m.group(2)))) & \
           set(map(int, re.findall("(\d+)", m.group(3))))
    cardhits[int(m.group(1))] = nhits = len(hits)
    if nhits > 0: ans1 += 1 << (nhits - 1)

def processcard(n):
    val = 1
    if n in cardcache:
        return cardcache[n]
    for i in range(cardhits[n]):
        val += processcard(i + n + 1)
    cardcache[n] = val
    return val

for n in cardhits:
    ans2 += processcard(n)

print(ans1)
print(ans2)
# 23750
# 13261850
