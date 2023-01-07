import numpy

def p1compact(treematrix):
    # create new matrix with 2 slots for each tree: original value plus a visibility flag
    vmap = numpy.zeros( treematrix.shape + (2,) )
    vmap[..., 0] = treematrix
    # magically iterate each row AND each column using numpy matrix rotation
    for treerow in [r for r in vmap] + [c for c in numpy.rot90(vmap)]:
        for direction in treerow, numpy.flip(treerow, 0): # check both forward and reverse in each tree row
            visthreshold = 0
            for tree in direction: # track visibility threshold through the row
                if tree[0] >= visthreshold: # set trees visibility flag to 1 if it can be seen
                    tree[1] = 1
                    visthreshold = tree[0] + 1
    return int(vmap[...,1].sum()) # return sum of vilibilty flags

def p2scores(omap):
    for y in range(omap.shape[0]):
        for x in range(omap.shape[1]):
            totscore = 1
            originheight = omap[y, x]
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                tscore, tx, ty = 0, x + dx, y + dy
                while 0 <= tx < omap.shape[1] and 0 <= ty < omap.shape[0]:
                    tscore += 1
                    if omap[ty, tx] >= originheight: break
                    tx += dx; ty += dy
                totscore *= tscore
            yield totscore

allinput = open("inputdata/input08").read().splitlines()
origmap = numpy.array([[int(char) for char in list(line)] for line in allinput])
print("Part 1:", p1compact(origmap) )
print("Part 2:", max(p2scores(origmap)))

# this runs faster than p1compact() so it is kept here for fun.
# p1fast runs 1000 times in about 4.2s compared to p1compact 6.8s
treelist = []
for i in allinput:
    treelist.append(list(i))
def p1fast(treelist):
    visset = set()
    for y in range(len(treelist)):
        # check from the left
        visheight = 0
        for x in range(len(treelist[y])):
            height = int(treelist[y][x])
            if height >= visheight:
                visset.add( (x, y) )
                visheight = height + 1
        # check from the right
        visheight = 0
        for x in reversed(range(len(treelist[y]))):
            height = int(treelist[y][x])
            if height >= visheight:
                visset.add( (x, y) )
                visheight = height + 1
    for x in range(len(treelist[0])):
        # check from the top
        visheight = 0
        for y in range(len(treelist)):
            height = int(treelist[y][x])
            if height >= visheight:
                visset.add( (x, y) )
                visheight = height + 1
        # check from the right
        visheight = 0
        for y in reversed(range(len(treelist))):
            height = int(treelist[y][x])
            if height >= visheight:
                visset.add( (x, y) )
                visheight = height + 1
    return len(visset)

