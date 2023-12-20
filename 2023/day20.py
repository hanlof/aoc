import aoc

class Module():
    byname = dict()
    sigcount = { False: 0, True: 0 }
    pendingsigs = list()
    def __init__(s, line):
        mtype, name, dests = re.match("([%&]?)(\w+) -> (.*)", line).groups()
        s.name = name
        s.type = mtype
        s.dests = list()
        s.destasstring = dests
        s.ffstate = False
        s.inputs = dict()
        Module.byname[name] = s
    def __str__(s):
        return "%s/%s%d" % (s.name, s.type, sum(s.inputs.values()))
    def __repr__(s):
        return s.__str__()

    def process(s, level, src):
        global counter
        global buttoncount
        Module.sigcount[level] += 1
        newsigs = list()
        match (s.type, level):
            case 'SINK', _:
                assert level == True, buttoncount
                pass
            case '', _:
                newsigs = [functools.partial(d.process, level, s) for d in s.dests]
            case '%', True:
                pass # ignore HIGH pulse
            case '%', False:
                s.ffstate = not s.ffstate
                newsigs = [functools.partial(d.process, s.ffstate, s) for d in s.dests]
            case '&', _:
                s.inputs[src] = level
                if all(s.inputs.values()):
                    newsigs = [functools.partial(d.process, False, s) for d in s.dests]
                else:
                    # if s.name == "xc": print("XC", buttoncount)
                    # if s.name == "ct": print("CT", buttoncount)
                    # if s.name == "kp": print("KP", buttoncount)
                    # if s.name == "ks": print("KS", buttoncount)
                    newsigs = [functools.partial(d.process, True, s) for d in s.dests]
        Module.pendingsigs.extend(newsigs)

    @staticmethod
    def init():
        sink = list()
        for m in Module.byname.values():
            for d in m.destasstring.split(", "):
                if d in Module.byname:
                    m.dests.append(Module.byname[d])
                    Module.byname[d].inputs[m] = False
                else:
                    sink.append( (d, m) )
        for name, src in sink:
            snk = Module("%s -> " % name)
            snk.type = "SINK"
            src.dests.append(snk)
for line in aoc_inputlines:
    m = Module(line)

Module.init()

bcast = Module.byname['broadcaster']

conjlist = [m for m in Module.byname.values() if m.type == "&"]
buttoncount = 0
def tostr(inputs):
    s = ""
    for i in inputs.values():
        s += "1" if i else "0"
    return s


for counter in range(4096):
    bcast.process(False, "button")
    buttoncount += 1
    while len(Module.pendingsigs) > 0:
        Module.pendingsigs.pop(0)()

print("Part 1:", Module.sigcount[True] * Module.sigcount[False])
"""
KP 3733
CT 3797
XC 3823
KS 3907
"""
print("Part 2:", math.lcm(3733, 3797, 3823, 3907))
ms = Module.byname['ms']

def makedot(fname, mark=""):
    with open(fname, "w+") as dotfile:
        dotfile.write("digraph new_graph {\n")
        for i in Module.byname.values():
            dotfile.write("%s [label=\"%s %s\" %s]\n" % (i.name, i.name, i.type, "color=red" if mark==i.name else "color=black"))
            for j in i.dests:
                dotfile.write("%s -> %s [label=\"%s %s\"];\n" % (i.name, j.name, str("a"), str("b")))
        dotfile.write("}\n")

#makedot("1.dot")

"""
Button sends one low pulse to the broadcaster
broadcaster sends its input to all its destinations
% modules start OFF
% high pulse is ignored
% low pulse FLIPS between ON and OFF
% if turned on sends a high pulse / if turned off send low pulse
& remembers the most recent pulse on each input
& all memories start as LOW
& when it receives a pulse it FIRST updates memory and THEN
& > send LOW if all inputs are HIGH
& > send HIGH if all inputs are LOW
"""
n = 'broadcaster'

# 324 too low
