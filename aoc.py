import os
import re
import inspect
import itertools
import time
import threading
from lxml import etree

"""
    if inp == bytes(b'\x1b[A'): print("UP")
    if inp == bytes(b'\x1b[D'): print("LEFT")
    if inp == bytes(b'\x1b[B'): print("DOWN")
    if inp == bytes(b'\x1b[C'): print("RIGHT")
"""

verbose = 1

class Timing():
    def __init__(s, label="Timing:", lineprefix=" ", precision=2):
        s.timestamps = list()
        s.add(label)
        s.precision = precision
        s.lineprefix = lineprefix
    def add(s, label=None):
        s.timestamps.append( (label, time.time() ) )
    def print(s):
        if s.timestamps[0][0] is not None:
            print(s.timestamps[0][0])
        for t1, t2 in itertools.pairwise(s.timestamps):
            print(s.lineprefix, t2[0], ":", round(t2[1] - t1[1], s.precision),
                    round(t2[1] - s.timestamps[0][1], s.precision))

class Spinner():
    CURSORLEFT = "\x1b[D"
    def __init__(s, delay=0.1):
        s.e = threading.Event()
        s.t = None
        s.delay=delay
    def __enter__(s):
        s.start()
    def __exit__(s, *a):
        s.stop()
    def start(s):
        s.t = threading.Thread(target=s.spinner)
        s.e.clear()
        s.t.start()
    def spinner(s):
        states = itertools.cycle((list("/-\\|")))
        print(next(states), end="", flush=True)
        for c in states:
            if s.e.wait(timeout=s.delay):
                print(s.CURSORLEFT, end="", flush=True)
                break
            print(s.CURSORLEFT, c, sep="", end="", flush=True)
    def stop(s):
        s.e.set()
        s.t.join()

def firstcallerstackframe():
    callstack = inspect.stack()
    for frame in callstack:
        if frame.filename == callstack[0].filename:
            continue
        caller = frame
        break
    return caller

def getverbosity():
    callerframe = firstcallerstackframe()
    global verbose
    if "verbose" in callerframe.frame.f_globals:
        verbose = callerframe.frame.f_globals['verbose']
    if "verbose" in callerframe.frame.f_locals:
        verbose = callerframe.frame.f_locals['verbose']
    return verbose

def metadata(day=None):
    if day is None:
        callerframe = firstcallerstackframe()
        pyfile = callerframe.filename
        r = re.search("day(\d+)", pyfile)
        if r[1]:
            day = int(r[1])
        else:
            day = None
    pyfile = "day%02d.py" % day
    basepath = os.path.dirname(pyfile)
    inputfname = os.path.join(basepath, "inputdata/input%02d" % day)
    htmlfname = os.path.join(basepath, "htmlpages/%d.html" % day)
    return {'pyfile': pyfile, 'daynb': day, 'basepath': basepath, 'inputfname': inputfname, 'htmlfname': htmlfname }

def getinput(day=None, conv=None):
    verbose = getverbosity()
    cinfo = metadata(day=day)
    if day is None:
        inputfilename = cinfo['inputfname']
    else:
        inputfilename = os.path.join(cinfo['basepath'], "inputdata/input%02d" % day)
    if verbose > 2: print("Input file is:", inpfilepath)
    if not os.path.exists(inputfilename):
        # XXX try to fetch it using ./fetch_input ?!
        raise Exception("Input file'" + inputfilename + "'not found")
    lines = open(inputfilename).read().splitlines()
    if conv is not None: return map(conv, lines)
    return lines


# splits input into sections by empty lines
# and converts the types of elements
def sections(elements, conv=None):
    if conv is None: t = lambda x: x
    else: t = conv
    sections = itertools.groupby(elements, key=lambda l: l == "")
    return [[t(l) for l in sec] for isempty, sec in sections if not isempty]

#for i in h.findall(".//em"): print(i.text)

def gethtmletree(day=None):
    c = metadata(day=day)
    return etree.HTML(open(c['htmlfname']).read())

def htmlcodesections(day=None):
    c = metadata()
    s = open(c['htmlfname']).read()
    a = re.findall("<pre><code>(.*?)</code></pre>", s, flags=re.MULTILINE | re.DOTALL)
    return [s.splitlines() for s in a]

def htmlemcodesections(day=None):
    c = metadata()
    s = open(c['htmlfname']).read()
    a = re.findall("<em><code>(.*?)</code></em>", s, flags=re.MULTILINE | re.DOTALL)
    return [s for s in a]

def htmlcodeemsections(day=None):
    c = metadata()
    s = open(c['htmlfname']).read()
    a = re.findall("<code><em>(.*?)</em></code>", s, flags=re.MULTILINE | re.DOTALL)
    return [s for s in a]

def htmlanswers(day=None):
    c = metadata(day)
    s = open(c['htmlfname']).read()
    a = re.findall("Your puzzle answer was <code>(.*?)</code>", s, flags=re.MULTILINE | re.DOTALL)
    return a

def htmltitle(day=None):
    c = metadata(day)
    s = open(c['htmlfname']).read()
    a = re.findall("day-desc..<h2>(.*?)</h2>", s, flags=re.MULTILINE | re.DOTALL)
    return a[0]
    """day-desc..<h2>.*</h2>"""

