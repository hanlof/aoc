import aoc

elfs = [sum(numbers) for numbers in aoc_sections_int]
print("Part 1:", sorted(elfs)[-1])
print("Part 2:", sum(sorted(elfs, reverse=True)[0:3]))

