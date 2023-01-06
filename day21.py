import re
import sys
import itertools
import fractions

nodes = dict()

f = open("inputdata/input21")
for i in f.readlines():
    s = i.split(": ")
    nodes[s[0]] = s[1][:-1]

def recurse1(node):
    #print("AAA", n)
    if node == "humn":
        pass
    if node.isdecimal(): return int(node)
    k = node.split(" ")
    if len(k) == 1:
        return recurse1(nodes[node])
    n0 = recurse1(k[0])
    n2 = recurse1(k[2])
    return eval("%s %s %s" % (n0, k[1], n2))

t = nodes["root"].split(" ")
left = t[0]
right = t[2]
with open("play/day21.dot", "w+") as dotfile:
    dotfile.write("digraph new_graph {\n")
    for name, content in nodes.items():
        k = content.split(" ")
        dotfile.write("%s [label=\"%s\" %s];\n" % (name, content, " fillcolor=red style=filled" if name == "humn" else ""))
        #dotfile.write("%s [label=\"%s\"];\n" % (name, content))
        #dotfile.write("%s;\n" % (name))
        if len(k) > 1:
            dotfile.write("%s -> %s;\n" % (name, k[0]))
            dotfile.write("%s -> %s;\n" % (name, k[2]))
    dotfile.write("}\n")
print("Part 1:", recurse1(nodes["root"]))

humn = None
def recurse2(node, res=None):
    global humn
    if node == "humn":
        if res is not None: # Found the correct value for the "humn" node!
            humn = res
        return res
    if node.isdecimal(): return fractions.Fraction(int(node), 1)
    k = node.split(" ")
    if len(k) == 1:
        return recurse2(nodes[node], res)
    n0 = recurse2(k[0])
    n2 = recurse2(k[2])
    if n0 is None:
        if res is not None:
            if   k[1] == "*": res = res / fractions.Fraction(n2, 1)
            elif k[1] == "+": res = res - fractions.Fraction(n2, 1)
            elif k[1] == "-": res = res + fractions.Fraction(n2, 1)
            elif k[1] == "/": res = res * fractions.Fraction(n2, 1)
            else: return None
            recurse2(k[0], res=res)
        return None

    if n2 is None:
        if res is not None:
            if   k[1] == "*": res = res / fractions.Fraction(n0, 1)
            elif k[1] == "+": res = res - fractions.Fraction(n0, 1)
            elif k[1] == "-": res = n0  - fractions.Fraction(res, 1)
            elif k[1] == "/": res = res * fractions.Fraction(n0, 1)
            else: return None
            recurse2(k[2], res=res)
        return None

    return fractions.Fraction(eval("fractions.Fraction(%s, 1) %s fractions.Fraction(%s, 1)" % (n0, k[1], n2)), 1)


rightside = recurse1(nodes[right]) # this is a value. does not contain 'humn'
recurse2(left, res=fractions.Fraction(int(rightside), 1))
print("Part 2:", humn)


nodes["humn"] = "3740214169961" # == 72950437236592.06
#print("LEFT: >", recurse1(nodes[left]))
#print("RIGHT: ", recurse1(nodes[right]))
#print("LEFT2: ", recurse2(nodes[left]))
#print("RIGHT2:", recurse2(nodes[right]))

