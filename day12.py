import sys
import re
import aoc

class Node():
    visited = False
    distance = None
    reachable_nodes = None
    x = None
    y = None
    elevation = None
    def __init__(self, x, y, elevationsign):
        self.x = x
        self.y = y
        if elevationsign == 'S': ele = 0
        elif elevationsign == 'E': ele = ord('z') - ord('a')
        else: ele = ord(elevationsign) - ord('a')
        self.elevation = ele
        self.reachable_nodes = list()
        self.reachable_from = list()
    def __repr__(self):
        return "%s%-3d" % ( chr(self.elevation or "-"), self.distance or -2)
    def __str__(self):
        return "%s%-3d" % ( chr(self.elevation or "-"), self.distance or -2)

def parseandsetup(inputlines):
    nodedict = dict()
    # Create nodes (without connections)
    for y, row in enumerate(inputlines):
        for x, elesign in enumerate(row):
            node = Node(x, y, elesign)
            if elesign == 'S': startnode = node
            elif elesign == 'E': endnode = node
            nodedict[(x, y)] = node
    # Create node connections
    above = lambda n: nodedict.get((n.x, n.y - 1))
    below = lambda n: nodedict.get((n.x, n.y + 1))
    left  = lambda n: nodedict.get((n.x - 1, n.y))
    right = lambda n: nodedict.get((n.x + 1, n.y))
    for n in nodedict.values():
        for neighbour in [above(n), below(n), left(n), right(n)]:
            if neighbour is None: continue # happens on edge rows. top, bottom, etc
            if neighbour.elevation <= (n.elevation + 1):
                n.reachable_nodes.append(neighbour)
                neighbour.reachable_from.append(n)
    return nodedict, startnode, endnode

def calculatedistances(nodedict, fromnode):
    for n in nodedict.values():
        n.visited = False
    fromnode.distance = 0
    fromnode.visited = True
    nodequeue = [ fromnode ]
    while len(nodequeue) > 0:
        curnode = nodequeue.pop()
        newdist = curnode.distance + 1
        for n in curnode.reachable_from:
            if n.visited: continue
            n.visited = True
            n.distance = newdist
            nodequeue.insert(0, n)

nodedict, startnode, endnode = parseandsetup(aoc.getinput())

calculatedistances(nodedict, endnode)

print("Part 1:", startnode.distance)
part2filter = lambda n: n.elevation == 0 and n.distance is not None
print("Part 2:", min([n.distance for n in nodedict.values() if part2filter(n)]))
