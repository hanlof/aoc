import operator
import itertools
import aoc

symbol_to_value = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
value_to_symbol = {v: k for k, v in symbol_to_value.items()}

# if this looks scary then please consider it could have been written as
# one line without descriptive names for the different parts O:-)
powers_of_five_sequence = lambda: map(operator.pow, itertools.repeat(5), itertools.count(0))
symbol_values = lambda s: map(symbol_to_value.get, reversed(s))
digits_actual_values = lambda s: map(operator.mul, symbol_values(s), powers_of_five_sequence())
snafu2int = lambda s: sum(digits_actual_values(s))
p1sum = sum(aoc.getinput(conv=snafu2int))

def getpow(n):
    for i in itertools.count(0):
        val = (5 ** i)
        halfcur = val // 2
        upper = (val * 2 + halfcur)
        lower = (val * -2 - halfcur)
        if lower <= (n) <= upper:
            return i

answer = ""
tmp = p1sum
for i in range(getpow(tmp), -1, -1):
    curvalue = (5 ** (i))
    halfcur = curvalue // 2
    upper = (curvalue * 2 + halfcur)
    lower = (curvalue * -2 - halfcur)
    output = (tmp - lower) // curvalue
    output -= 2
    answer += value_to_symbol[output]
    tmp -= (output * curvalue)

print("Part 1:", answer)
print("Part 2:", "*** 49/49 (100%) gold stars collected ***")
