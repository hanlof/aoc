import re
import operator

inputfile = open("inputdata/input11")
allinput = inputfile.readlines()

class Item():
    level = 0
    def __init__(self, level):
        self.level = level
    def __repr__(self):
        return "<Item %d>" % self.level

monkeys = dict()

class Monkey():
    inspectcount = 0
    index = 0
    items = None
    op = ""
    test = 0
    truetarget = 0
    falsetarget = 0
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
        self.items = list(map(Item, l))
        self.op = r.group('operation')
        ops = r.group('operation').split(" ")
        if ops[2] == "old" and ops[1] == "*":
            self.oper = operator.methodcaller("__pow__", 2)
        elif ops[1] == "*":
            self.oper = operator.methodcaller("__mul__", int(ops[2]))
        elif ops[1] == "+":
            self.oper = operator.methodcaller("__add__", int(ops[2]))
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
            item.level = self.oper(item.level)
            item.level = item.level // divisor
            item.level = item.level % 9699690 # 2*3*5*7*11*13*17*19 (keeping number small for round 2)
            if (item.level % self.test) == 0:
                monkeys[self.truetarget].items.append(item)
            else:
                monkeys[self.falsetarget].items.append(item)
            self.inspectcount += 1

a = "".join(allinput)
r = re.findall("""
?(^Monkey (\d+):$
  Starting items: (?P<items>((\d+)(, )?)+).*$
  Operation.*$
  Test: .*$
    If.*$
    If.*$)+""", a, flags=re.MULTILINE)
if r:
    for m in r:
        monkeys[int(m[1])] = Monkey(m[0])
else:
    print("Bad input")

for i in range(20):
    for (index, monkey) in monkeys.items():
        monkey.inspectall(3)

toplist = sorted(monkeys.values(), key=lambda m: (m.inspectcount), reverse=True)

print("Part 1:", toplist[0].inspectcount * toplist[1].inspectcount)

# reset all for round 2
a = "".join(allinput)
r = re.findall("""
?(^Monkey (\d+):$
  Starting items: (?P<items>((\d+)(, )?)+).*$
  Operation.*$
  Test: .*$
    If.*$
    If.*$)+""", a, flags=re.MULTILINE)
if r:
    for m in r:
        monkeys[int(m[1])] = Monkey(m[0])
else:
    print("Bad input")

for i in range(10000):
    for (index, monkey) in monkeys.items():
        monkey.inspectall(1)

toplist = sorted(monkeys.values(), key=operator.attrgetter("inspectcount"), reverse=True)

print("Part 2:", toplist[0].inspectcount * toplist[1].inspectcount)


