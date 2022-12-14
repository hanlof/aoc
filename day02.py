import sys

print(__file__)

#inputfile = sys.stdin
inputfile = open("input02")
allinput = inputfile.readlines()

ROCK = 1
PAPER = 2
SCISSOR = 3

def parse(c):
    if c == 'A' or c == 'X': return ROCK
    if c == 'B' or c == 'Y': return PAPER
    if c == 'C' or c == 'Z': return SCISSOR

score = 0
for i in allinput:
    opp = parse(i[0])
    my = parse(i[2])

    if my == opp:
        score += 3
    elif my == ROCK and opp == SCISSOR:
        score += 6
    elif my == PAPER and opp == ROCK:
        score += 6
    elif my == SCISSOR and opp == PAPER:
        score += 6
    score += my


print("Score: %d" % (score))

score = 0
for i in allinput:
    opp = parse(i[0])
    outcome = i[2]
    if opp == ROCK:
        if outcome == 'X': # lose
            my = SCISSOR
        elif outcome == 'Y': # draw
            my = ROCK
        elif outcome == 'Z': # win
            my = PAPER
    elif opp == PAPER:
        if outcome == 'X': # lose
            my = ROCK
        elif outcome == 'Y': # draw
            my = PAPER
        elif outcome == 'Z': # win
            my = SCISSOR
    elif opp == SCISSOR:
        if outcome == 'X': # lose
            my = PAPER
        elif outcome == 'Y': # draw
            my = SCISSOR
        elif outcome == 'Z': # win
            my = ROCK

    if my == opp:
        score += 3
    elif my == ROCK and opp == SCISSOR:
        score += 6
    elif my == PAPER and opp == ROCK:
        score += 6
    elif my == SCISSOR and opp == PAPER:
        score += 6
    score += my

print("Score 2: %d", score)
# 10961 too high
