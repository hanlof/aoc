import re
import operator
import aoc

class Monkey():
    inspectcount = 0
    index = 0
    items = None
    op = ""
    test = 0
    truetarget = 0
    falsetarget = 0
    mttarget = None
    mftarget = None
    def __init__(self, str):
        r = re.match("""
?^Monkey (?P<index>\d+):$
  Starting items: (?P<items>((\d+)(, )?)+).*$
  Operation: new = (?P<operation>.*)$
  Test: divisible by (?P<test>.*)$
    If true: throw to monkey (?P<true>.*)$
    If false: throw to monkey (?P<false>.*)$""", str, flags=re.MULTILINE)
        self.index = int(r.group('index'))
        l = eval("[" + r.group('items') + "]")
        self.items = [int(i) for i in l]
        ops = r.group('operation').split(" ")
        if ops[2] == "old" and ops[1] == "*":
            self.oper = lambda x: (x * x) % 9699690 # prevent number from growing to silly values
        elif ops[1] == "*":
            self.operarg = int(ops[2])
            self.oper = lambda x: x * self.operarg
        elif ops[1] == "+":
            self.operarg = int(ops[2])
            self.oper = lambda x: x + self.operarg
        self.test = int(r.group('test'))
        self.truetarget = int(r.group('true'))
        self.falsetarget = int(r.group('false'))
    def __str__(self):
        return "<Monkey %d: C:%-5d '%-9s' div:%-2d t:%d f:%d (I:%s)>" % (self.index, self.inspectcount, self.op, self.test, self.truetarget, self.falsetarget, self.items.__repr__())
    def __repr__(self):
        return "<Monkey %d: C:%-5d '%-9s' div:%-2d t:%d f:%d (I:%s)>" % (self.index, self.inspectcount, self.op, self.test, self.truetarget, self.falsetarget, self.items.__repr__())
    def inspectall(self, divisor):
        while len(self.items) != 0:
            item = self.items.pop(0)
            item = self.oper(item)
            item = item // divisor
            target = self.mttarget if (item % self.test) == 0 \
                    else self.mftarget
            target.append(item)
            self.inspectcount += 1
    def inspectall2(self):
        for it in self.items:
            item = self.oper(it)
            if (item % self.test) == 0:
                self.mttarget.append(item)
            else:
                self.mftarget.append(item)
            self.inspectcount += 1
        self.items.clear() # XXX can't do self.items = [] because items is referenced in other monkeys

monkeys = dict()

for n, s in enumerate(aoc.sections(aoc.getinput())):
    monkeys[n] = Monkey("\n".join(s))

for n, m in monkeys.items():
    m.mftarget = monkeys[m.falsetarget].items
    m.mttarget = monkeys[m.truetarget].items

for i in range(20):
    for (index, monkey) in monkeys.items():
        monkey.inspectall(3)

toplist = sorted(monkeys.values(), key=lambda m: (m.inspectcount), reverse=True)

print("Part 1:", toplist[0].inspectcount * toplist[1].inspectcount)

# reset all for round 2
for n, s in enumerate(aoc.sections(aoc.getinput())):
    monkeys[n] = Monkey("\n".join(s))

for n, m in monkeys.items():
    m.mftarget = monkeys[m.falsetarget].items
    m.mttarget = monkeys[m.truetarget].items

for i in range(10000):
    for monkey in monkeys.values():
        monkey.inspectall2()

toplist = sorted(monkeys.values(), key=operator.attrgetter("inspectcount"), reverse=True)

print("Part 2:", toplist[0].inspectcount * toplist[1].inspectcount)

