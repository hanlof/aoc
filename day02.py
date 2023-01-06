# ROCK    = 1  loses to 2, wins to 3
# PAPER   = 2  loses to 3, wins to 1
# SCISSOR = 3  loses to 1, wins to 2
class RPS():
    def __init__(s, c):
        if   ord('A') <= ord(c) <= ord('C'): s.val = ord(c) - ord('A') + 1
        elif ord('X') <= ord(c) <= ord('Z'): s.val = ord(c) - ord('X') + 1
        s.loses_to = (s.val % 3) + 1
        s.wins_to  = (s.loses_to % 3) + 1
    def score_against(s, o):
        if   o.val == s.loses_to: return 0
        elif o.val == s.wins_to: return 6
        elif o.val == s.val: return 3

def part1scores(lines):
    for line in lines:
        mymove = RPS(line[2])
        yield mymove.score_against(RPS(line[0])) + mymove.val

def part2scores(lines):
    for line in lines:
        if line[2] == 'X': # should lose
            yield RPS(line[0]).wins_to
        if line[2] == 'Y': # should draw
            yield 3 + RPS(line[0]).val
        if line[2] == 'Z': # should win
            yield 6 + RPS(line[0]).loses_to

print("Day 2: Rock, Paper, Scissors")
inputlines = open("inputdata/input02").readlines()
print("Part 1:", sum(part1scores(inputlines)))
print("Part 2:", sum(part2scores(inputlines)))
