import aoc

class Part:
    def __init__(self, line):
        m = re.match("{x=(-?\d+),m=(-?\d+),a=(-?\d+),s=(-?\d+)}", line)
        self.x, self.m, self.a, self.s = m.groups()
        self.values = { 'x': int(self.x), 'm': int(self.m), 'a': int(self.a), 's': int(self.s) }

targetmap = {'A': True, 'R': False}
actualtarget = lambda t: targetmap[t] if t in targetmap else t
comparemap = {'<': int.__lt__, '>': int.__gt__}
class Ruleset:
    byname = dict()
    def __init__(self, line):
        m = re.match("(\w+){([\w<>,:]+)}", line)
        self.name = m[1]
        self.tests = list()
        rules = m[2].split(",")
        for r in rules[:-1]:
            letter, comparison, value, target = re.match("(\w)([<>])(\d+):(\w+)", r).groups()
            func = lambda p, cmp=comparemap[comparison], c=letter, v=int(value): cmp(p.values[c], v)
            self.tests.append( [func, actualtarget(target), r] )
        self.tests.append( [lambda p: True, actualtarget(rules[-1]), rules[-1] ] )
        Ruleset.byname[self.name] = self
    def eval(self, part):
        for test, target, printable in self.tests:
            if test(part):
                if type(target) is bool: return target
                else: return Ruleset.byname[target].eval(part)
    def combinations(self):
        head = []
        ret = []
        for test, target, printable in self.tests:
            if type(target) is bool:
                if target: innerpart = [target]
                else: innerpart = None
            else: innerpart = Ruleset.byname[target].combinations()
            if innerpart is not None:
                for i in innerpart:
                    t = head + [printable+"/t"]
                    if type(i) is list:
                        t.extend(i)
                    else:
                        pass
                        #t += [i]
                    ret.append(t)
            head.append(printable+"/f")

        return ret
    def __str__(self):
        return self.name


"""
in{s<1351:px,s>2770:A,m<1801:hdj,R}
px{a<2006:qkq,m>2090:A,s<537:R,x>2440:R,A}
qkq{x<1416:A,x>2662:A,R}
hdj{m>838:A,a>1716:R,A}"""

#aoc_sections[0] = \
"""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}""".splitlines()

#aoc_sections[1] = \
"""{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}""".splitlines()

for line in aoc_sections[0]:
    Ruleset(line)


ans1 = 0
for line in aoc_sections[1]:
    p = Part(line)
    if Ruleset.byname['in'].eval(p):
        ans1 += sum(p.values.values())

print("Part 1:", ans1)

print(len(Ruleset.byname.values()))
# if the last rule in a chain is another chain then insert that chain here
# and remove it from the list
while True:
    for r in Ruleset.byname.keys():
        t = Ruleset.byname[r].tests[-1][1]
        if t not in [True, False]:
            del(Ruleset.byname[r].tests[-1])
            Ruleset.byname[r].tests.extend(Ruleset.byname[t].tests)
            break
    else:
        break
    del(Ruleset.byname[t])

print(len(Ruleset.byname.values()))


kill = []
for n, i in Ruleset.byname.items():
    for rule in i.tests:
        if rule[1] in [True, False]: continue
        if all([r[1] == True for r in Ruleset.byname[rule[1]].tests]):
            kill.append(rule[1])
            rule[2] = rule[2].replace(rule[1], "A")
            rule[1] = True
            continue
        if all([r[1] == False for r in Ruleset.byname[rule[1]].tests]):
            kill.append(rule[1])
            rule[2] = rule[2].replace(rule[1], "R")
            rule[1] = False
            continue
for k in kill:
    del(Ruleset.byname[k])
print(len(Ruleset.byname.values()))

#for n, i in Ruleset.byname.items():
#    print(n, [r[2] for r in i.tests])
#    pass

print("-----------__")
x=Ruleset.byname['in'].combinations()
for i in x:
    print(i)
# all combinations are probably mutually exclusive! makes it a whole lot simpler!
r = x[-1][0]
def combinations(rulechain):
    ran = dict(x=[1, 4000], m=[1, 4000], a=[1, 4000], s=[1, 4000])
    for rule in rulechain:
        if rule[0] == "A":
            continue
        letter, comparison, value, _, truefalse = re.match("(\w)([<>])(\d+):(\w+)/(\w)", rule).groups()
        #print(letter, comparison, value, truefalse)
        match comparison, truefalse:
            case "<", "t":
                ran[letter][1] = int(value) - 1
            case ">", "t":
                ran[letter][0] = int(value) + 1
            case "<", "f":
                ran[letter][0] = int(value)
            case ">", "f":
                ran[letter][1] = int(value)
            case _: assert False
    print(ran)
    ret = 1
    for v in ran.values():
        ret *= (v[1] - v[0] + 1)
        print(v[1] - v[0] + 1)
    print(ret)
    return ret

print(sum(map(combinations, x)))
