import aoc

"""
start with a current value of 0. Then, for each character in the string starting from the beginning:

    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """

s = open("inputdata/input15").read().strip()

#s = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
def h(s):
    curval = 0
    for c in s:
        curval += ord(c)
        curval *= 17
        curval %= 256
    return curval

ans1 = 0
codes = s.split(",")
boxes = dict()
newdict = lambda: dict()

for i in range(256):
    boxes[i] = dict()

def focpower(boxnum, box):
    bn = boxnum + 1
    retval = 0
    for slotnum, (label, foclen) in enumerate(box.items(), start=1):
        print(bn)
        retval += bn * slotnum * int(foclen)
    return retval

ans2 = 0
for c in codes:
    ha = h(c)
    ans1 += ha

    # p2
    print(">>>", c)
    label = re.match("\w+", c)[0]
    boxnumber = h(label)
    if '=' in c:
        foclen = c.split("=")[1]
        boxes[boxnumber][label] = foclen
    elif '-' in c:
        if label in boxes[boxnumber]:
            del(boxes[boxnumber][label])

for key, b in boxes.items():
    if len(b) > 0:
        #print(b, focpower(key, b))
        ans2 += focpower(key, b)
#print([b for b in boxes.values()])
print([(n, b) for n, b in boxes.items() if len(b) > 0])
print(len([b for b in boxes.values() if len(b) > 0]))

print("Part 1", ans1)
print("Part 2", ans2)

