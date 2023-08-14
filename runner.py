import aoc
import sys
import os
import datetime
from io import StringIO


class TimedIO(StringIO):
    def __init__(s, split=None):
        s.times = list([datetime.datetime.now()])
        s.parts = list([""])
        s.split = split
        s.counter =  0
        super().__init__()
    def write(s, data): 
        if s.split:
            s.split.write(data)
        s.counter += 1
        s.times.append(datetime.datetime.now())
        s.parts.append(data)
        super().write(data)
    def flush(s): 
        if s.split:
            s.split.flush()
        super().flush()
    def close(s):
        s.times.append(datetime.datetime.now())
        super().close()

class Redir():
    def __init__(self, io):
        self.io = io
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._io = self.io
        return self
    def __exit__(self, *args):
        self.str = self._io.getvalue()
        #del self._stringio    # free up some memory
        sys.stdout = self._stdout

runday = lambda day: __import__("day%02d" % day)

def findtime(times, parts, start, end):
    spos = 0
    for n, time in enumerate(times):
        part = parts[n]
        partlen = len(part)
        epos = spos + partlen
        if spos <= start < epos:
            t1 = time
        if spos <= end < epos:
            t2 = time
        spos = epos
    return t2

for i in range(1, 26):
    #print(aoc.htmltitle(i), aoc.htmlanswers(i))
    print(aoc.htmltitle(i), end="", flush=True)
    #with Redir(TimedIO(split=sys.stdout)) as o:
    with Redir(TimedIO(split=None)) as o:
        before = datetime.datetime.now()
        runday(i)
        after = datetime.datetime.now()
    
    for n, (i, j) in enumerate(itertools.pairwise(o.io.times)):
        seconds = (j - i).total_seconds()
      #  print("%.03f" % seconds, repr(o.io.parts[n]))
    alloutput = ("".join(o.io.parts))
    p1 = re.search("^Part 1:.*$", alloutput, re.MULTILINE)
    p2 = re.search("^Part 2:.*$", alloutput, re.MULTILINE)
    stimestamp = o.io.times[0]
    if p1:
        p1timestamp = findtime(o.io.times, o.io.parts, *p1.span())
    if p2:
        p2timestamp = findtime(o.io.times, o.io.parts, *p2.span())
    p1time = (p1timestamp - stimestamp).total_seconds()
    p2time = (p2timestamp - p1timestamp).total_seconds()
    tottime = (p2timestamp - stimestamp).total_seconds()
    t = (after - stimestamp).total_seconds()
    print("Timing:", p1time, p2time, tottime, t)
