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
            self.tests.append( (func, actualtarget(target), r) )
        self.tests.append( (lambda p: True, actualtarget(rules[-1]), rules[-1] ) )
        Ruleset.byname[self.name] = self
    def eval(self, part):
        #print("eval", self.name, part.values)
        for test, target, printable in self.tests:
            if test(part):
                if type(target) is bool: return target
                else: return Ruleset.byname[target].eval(part)
    def __str__(self):
        return self.name


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
    r = Ruleset(line)

ans1 = 0
for line in aoc_sections[1]:
    p = Part(line)
    if Ruleset.byname['in'].eval(p):
        ans1 += sum(p.values.values())

print("Part 1:", ans1)

