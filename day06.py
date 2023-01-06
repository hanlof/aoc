inp = open("inputdata/input06").readline()
p1, p2 = None, None
for i in range(len(inp)):
    if p1 is None and len(set((inp[i:i +  4]))) == 4:  p1 = i + 4
    if p2 is None and len(set((inp[i:i + 14]))) == 14: p2 = i + 14
print("Part 1:", p1)
print("Part 2:", p2)
