import datetime
starttime = datetime.datetime.now()
lines = open("1").read().splitlines()
tot = 0
for l in lines:
    digits = list(filter(lambda x: x.isdigit(), l))
    tot += int(digits[0] + digits[-1])
print("Part 1:", tot)

# part 2
tot = 0
numberwords=("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
numberwords += ("1", "2", "3", "4", "5", "6", "7", "8", "9")
word2num = dict()
for d, w in enumerate(numberwords, start=1):
    word2num[w] = d
for i in range(1, 10):
    word2num[str(i)] = i

def findfirstnum(s):
    for p in range(len(s)):
        for w in numberwords:
            if s.find(w, p, p + len(w)) != -1:
                return word2num[w]
    assert False

def findlastnum(s):
    s = s[::-1]
    for p in range(len(s)):
        for w in numberwords:
            if s.find(w[::-1], p, p + len(w)) != -1:
                return word2num[w]
    assert False

for l in lines:
    d1 = findfirstnum(l)
    d2 = findlastnum(l)
    tot += int(str(d1) + str(d2))

print("Part 2:", tot)
# 53789 too low
# 53802 too low
# 99000 is wrong
print(datetime.datetime.now() - starttime)
