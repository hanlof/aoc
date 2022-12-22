import sys
import re

print(__file__)

#inputfile = sys.stdin
inputfile = open("input12")
allinput = inputfile.readlines()

# 64 x 41
map = []
nodemap = []
for i in allinput:
#    print(len(i), i)
    map.append(list(i[0:64]))
    nodemap.append([None] * 64)

for y in range(len(map)):
    for x in range(len(map[y])):
        cur = ord(map[y][x])
        marker = ' '
        if y > 0:
            if ord(map[y - 1][x]) == (cur + 1):
                marker = '|'
            elif ord(map[y - 1][x]) == (cur - 1):
                marker = '|'
            elif ord(map[y - 1][x]) == (cur):
                marker = '|'
            print(marker, end="")
        print(' ', end="")
    print("")
    for x in range(len(map[y])):
        cur = ord(map[y][x])
        marker = ' '
        if x > 0:
            if ord(map[y][x - 1]) == (cur + 1):
                marker = '-'
            elif ord(map[y][x - 1]) == (cur - 1):
                marker = '-'
            elif ord(map[y][x - 1]) == (cur):
                marker = '-'
            print(marker, end="")
        print(map[y][x], end="")
    print("")

# Prepare dijkstras...
class Node():
    visited = False
    distance = None
    reachable_nodes = None
    x = None
    y = None
    elevation = None
    def __init__(self, x, y, ele):
        self.x = x
        self.y = y
        self.elevation = ele
        self.reachable_nodes = list()
    def __repr__(self):
        return "%s%-3d" % ( chr(self.elevation or "-"), self.distance or -1)
    def __str__(self):
        #return "N%d/%d" % (self.x, self.y)
        return "%s%-3d" % ( chr(self.elevation or "-"), self.distance or -1)
        #return "N%c%d" % (chr(self.elevation), len(self.reachable_nodes))

# Create nodes (without connections)
startnode = None
endnode = None
for y in range(len(map)):
    for x in range(len(map[y])):
        elc = map[y][x]
        if elc == 'S':
            ele = ord('a')
        elif elc == 'E':
            ele = ord('z')
        else:
            ele = ord(elc)
        nodemap[y][x] = Node(x, y, ele)
        if elc == 'S':
            startnode = nodemap[y][x]
        elif elc == 'E':
            endnode = nodemap[y][x]

# Create all connections between nodes
for y in range(len(map)):
    for x in range(len(map[y])):
        n = nodemap[y][x]
        if y > 0:
            if nodemap[y - 1][x].elevation <= (n.elevation + 1):
                n.reachable_nodes.append(nodemap[y - 1][x])
        if y < (len(map) - 1):
            if nodemap[y + 1][x].elevation <= (n.elevation + 1):
                n.reachable_nodes.append(nodemap[y + 1][x])
        if x > 0:
            if nodemap[y][x - 1].elevation <= (n.elevation + 1):
                n.reachable_nodes.append(nodemap[y][x - 1])
        if x < (len(map[0]) - 1):
            if nodemap[y][x + 1].elevation <= (n.elevation + 1):
                n.reachable_nodes.append(nodemap[y][x + 1])

startnode.distance = 0
startnode.visited = True
nodequeue = [ startnode ]
count = 0
while len(nodequeue) > 0:
    n = nodequeue.pop()
    for r in n.reachable_nodes:
        if r.visited: continue
        r.distance = n.distance + 1
        nodequeue.insert(0, r)
        r.visited = True
    count = count + 1
    if n is endnode:
        break

#for i in nodemap:
#    print(i[10:])

print("Part 1:", endnode.distance)
