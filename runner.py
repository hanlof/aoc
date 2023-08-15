#!/usr/bin/python3

import sys
import os
import re
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
    def gettime(s, regex):
        # XXX TODO printing timings disrupts recognition of patterns.
        #       need to investigate!
        m = re.search(regex, s.getvalue(), re.MULTILINE)
        if m:
            patternstart, patternend = m.span()
            partstart = partend = 0
            for n, time in enumerate(s.times):
                partstart = partend
                partend += len(s.parts[n])
                if partstart <= patternend < partend:
                    return (time - s.times[0]).total_seconds()
        return None

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

for i in range(1, 26):
    #correctanswers = aoc.htmlanswers(i)
    #desc = aoc.htmltitle(i)
    print("Day %-2d " % i, end="")
    split = None
    # XXX super lazy arguments handling
    if len(sys.argv) > 1:
        split = sys.stdout
    with Redir(TimedIO(split=split)) as o:
        d = __import__("day%02d" % i)
        # Potentially scary shenanigans to make the aoc module run
        # module-level code each time it is imported from the different modules we load
        if 'aoc' in sys.modules:
            del(sys.modules['aoc'])
    t1 = o.io.gettime("^Part 1:.*$")
    t2 = o.io.gettime("^Part 2:.*$")
    if t1 and t2:
        print(f"{t2:.3f} " , end="")
        print("\x1b[1m", "*" * ((int(t1 * 60))), sep="", end="\x1b[0m")
        print("*" * ((int((t2 - t1) * 60))))
    else:
        print(f"day {i} does not output 'Part 1'/'Part 2' strings")
