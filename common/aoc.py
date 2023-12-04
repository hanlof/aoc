import os
import re
import inspect
import itertools
import time
import threading
import sys
from io import StringIO
from lxml import etree

""" Notes
    * Auto download htmlpage and input UNLESS it's already there
    * Submit answer by manual action. DON'T submit already answered tasks
    * Clean up html parsing
    * Move day 22 interaction to here
    * add debug() function
    * parsing maps
    * parsing maps as node trees
    * producing .dot files
    * Add some color printing
        if inp == bytes(b'\x1b[A'): print("UP")
        if inp == bytes(b'\x1b[D'): print("LEFT")
        if inp == bytes(b'\x1b[B'): print("DOWN")
        if inp == bytes(b'\x1b[C'): print("RIGHT")
"""
verbose = 1


def bigletterstostring(picture):
    from bigletters import LETTERS
    import numpy
    ret = ""
    pic = numpy.array(picture)
    r=numpy.rot90(pic, -1)
    o=r.reshape(8, 5, 6)
    letters = dict()
    for l, raster in LETTERS.items():
        s = list()
        for y, row in enumerate(raster.splitlines()):
            for x, c in enumerate(row):
                if c == "#": s.append( (y, x) )
        letters[tuple(sorted(s))] = l

    for i in numpy.rot90(o, axes=(1, 2)):
        s = list()
        i = i[:,0:4]
        for y, row in enumerate(i):
            for x, n in enumerate(row):
                if n == 1: s.append( (y, x) )
        ret += letters[tuple(sorted(s))]
    return ret

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

def callerstackframe():
    callstack = inspect.stack()
    for frame in callstack:
        if frame.filename == callstack[0].filename:
            continue
        if frame.filename.startswith('<'):
            continue
        caller = frame
        break
    return caller or None

def getverbosity():
    callerframe = callerstackframe()
    global verbose
    if "verbose" in callerframe.frame.f_globals:
        verbose = callerframe.frame.f_globals['verbose']
    if "verbose" in callerframe.frame.f_locals:
        verbose = callerframe.frame.f_locals['verbose']
    return verbose

def metadata(day=None):
    if day is None:
        callerframe = callerstackframe()
        pyfile = callerframe.filename
        r = re.search("day(\d+)", pyfile)
        if r and r[1]:
            day = int(r[1])
        else:
            day = None
    if not day: return None
    pyfile = "day%02d.py" % day
    basepath = os.path.dirname(pyfile)
    inputfname = os.path.join(basepath, "inputdata/input%02d" % day)
    htmlfname = os.path.join(basepath, "htmlpages/%d.html" % day)
    return {'pyfile': pyfile, 'daynb': day, 'basepath': basepath, 'inputfname': inputfname, 'htmlfname': htmlfname }

def getinput(day=None, conv=None):
    verbose = getverbosity()
    cinfo = metadata(day=day)
    if not cinfo: return None
    if day is None:
        inputfilename = cinfo['inputfname']
    else:
        inputfilename = os.path.join(cinfo['basepath'], "inputdata/input%02d" % day)
    if verbose > 2: print("Input file is:", inpfilepath)
    if not os.path.exists(inputfilename):
        # XXX try to fetch it using ./fetch_input ?!
        raise Exception("Input file'" + inputfilename + "'not found")
    lines = open(inputfilename).read().splitlines()
    if conv is not None: return list(map(conv, lines))
    return lines


# splits input into sections by empty lines
# and convert the types of elements
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
    c = metadata(day)
    if c is None: return ""
    s = open(c['htmlfname']).read()
    a = re.findall("<pre><code>(.*?)</code></pre>", s, flags=re.MULTILINE | re.DOTALL)
    return [s.splitlines() for s in a]

def htmlemcodesections(day=None):
    c = metadata(day)
    if c is None: return ""
    s = open(c['htmlfname']).read()
    a = re.findall("<em><code>(.*?)</code></em>", s, flags=re.MULTILINE | re.DOTALL)
    return [s for s in a]

def htmlcodeemsections(day=None):
    c = metadata(day)
    if c is None: return ""
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

# import everything that potentially will be useful right into the importer namespace
importerframe = callerstackframe()
if importerframe and metadata():
    importerframe.frame.f_globals["itertools"] = __import__("itertools")
    importerframe.frame.f_globals["re"] = __import__("re")
    importerframe.frame.f_globals["os"] = __import__("os")
    importerframe.frame.f_globals["sys"] = __import__("sys")
    importerframe.frame.f_globals["numpy"] = __import__("numpy")
    importerframe.frame.f_globals["inspect"] = __import__("inspect")
    importerframe.frame.f_globals["threading"] = __import__("threading")
    importerframe.frame.f_globals["operator"] = __import__("operator")
    importerframe.frame.f_globals["functools"] = __import__("functools")
    importerframe.frame.f_globals["copy"] = __import__("copy")
    importerframe.frame.f_globals["fractions"] = __import__("fractions")
    importerframe.frame.f_globals["aoc_codeblocks"] = htmlcodesections()
    importerframe.frame.f_globals["aoc_constants"] = htmlemcodesections() + htmlcodeemsections()
    importerframe.frame.f_globals['aoc_inputlines'] = getinput()
    importerframe.frame.f_globals['aoc_sections'] = sections(getinput())
    try:
        importerframe.frame.f_globals['aoc_sections_int'] = sections(getinput(), conv=int)
    except:
        pass

