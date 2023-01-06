allinput = open("input01").read().splitlines()
elfs = list([0])
for line in allinput:
    if line == '':
        elfs.append(0)
        continue
    elfs[-1] += int(line)
elfs.sort()
print("Day 1: Calorie Counting")
print("Part 1:", elfs[-1])
print("Part 2:", sum(elfs[-3:]))
