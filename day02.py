import sys

# ROCK    = 1  loses to 2, wins to 3
# PAPER   = 2  loses to 3, wins to 1
# SCISSOR = 3  loses to 1, wins to 2

allinput = open("input02").readlines()

class RPS():
    def __init__(s, c):
        if   ord('A') <= ord(c) <= ord('C'): s.val = ord(c) - ord('A') + 1
        elif ord('X') <= ord(c) <= ord('Z'): s.val = ord(c) - ord('X') + 1
        s.loses_to = (s.val % 3) + 1
        s.wins_to = (s.loses_to % 3) + 1
    def score_against(s, o):
        if   o.val == s.loses_to: return 0
        elif o.val == s.wins_to: return 6
        elif o.val == s.val: return 3
        else: assert False

p1score = 0
for i in allinput:
    my = RPS(i[2])
    p1score += my.score_against(RPS(i[0])) + my.val

p2score = 0
for i in allinput:
    opp = RPS(i[0]) #parse(i[0])
    outcome = i[2]
    if outcome == 'X':  # should lose
        myval = opp.wins_to
        p2score += myval
    if outcome == 'Y': # should draw
        myval = opp.val
        p2score += 3 + myval
    if outcome == 'Z': # should win
        myval = opp.loses_to
        p2score += 6 + myval

print("Day 2: Rock, Paper, Scissors")
print("Part 1:", p1score)
print("Part 2:", p2score)
