import aoc

l2val = dict(zip(list("AKQJT98765432"), range(14, 1, -1)))
l2val_wild = dict(zip(list("AKQ_T98765432J"), range(14, 0, -1)))

class Hand():
    use_wildcards = False
    def __init__(self, s):
        cards, bid = s.split(" ")
        self.cards = cards
        self.bid = int(bid)
        self.cardvalues = list(map(l2val.__getitem__, cards))
        self.cardvalues_wild = list(map(l2val_wild.__getitem__, cards))
        self.cardtypes = set(self.cardvalues)
        self.cardcount = dict(zip(self.cardtypes, map(lambda x: self.cardvalues.count(x), self.cardtypes)))
        match sorted(self.cardcount.values()):
            case [5]:             self.type = 10 # 5 of a kind
            case [1, 4]:          self.type = 9  # 4 of a kind
            case [2, 3]:          self.type = 8  # full house
            case [1, 1, 3]:       self.type = 7  # 3 of a kind
            case [1, 2, 2]:       self.type = 6  # two pair
            case [1, 1, 1, 2]:    self.type = 5  # one pair
            case [1, 1, 1, 1, 1]: self.type = 4  # nothing!
            case _:               assert False   # any nasty surprises?
        J = self.cardcount.pop(11, None)
        match sorted(self.cardcount.values()):
            case [5] | [4] | [3] | [2] | [1] | []: # 5 of a kind
                self.type_wild = 10
            case [1, 4] | [1, 3] | [1, 2] | [1, 1]: # 4 of a kind
                self.type_wild = 9
            case [2, 3] | [2, 2]: # full house
                self.type_wild = 8
            case [1, 1, 3] | [1, 1, 2] | [1, 1, 1]: # 3 of a kind
                self.type_wild = 7
            case [1, 2, 2]: # two pair
                self.type_wild = 6
            case [1, 1, 1, 2] | [1, 1, 1, 1]: # one pair
                self.type_wild = 5
            case [1, 1, 1, 1, 1]: # nothing!
                self.type_wild = 4
            case _: # any other type?!
                assert False, self.cardcount.values()
        if J is not None: self.cardcount[11] = J
    def __lt__(self, other):
        if not Hand.use_wildcards:
            if self.type == other.type:
                return self.cardvalues < other.cardvalues
            else:
                return self.type < other.type
        else:
            if self.type_wild == other.type_wild:
                return self.cardvalues_wild < other.cardvalues_wild
            else:
                return self.type_wild < other.type_wild

hands = list()
for l in aoc_inputlines:
    hands.append(Hand(l))

ans1 = 0
ans2 = 0
for rank, hand in enumerate(sorted(hands), start = 1):
    ans1 += rank * hand.bid

Hand.use_wildcards = True
for rank, hand in enumerate(sorted(hands), start = 1):
    ans2 += rank * hand.bid

print("Part 1:", ans1)
print("Part 2:", ans2)

