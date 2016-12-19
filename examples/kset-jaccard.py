import pykmer.kset as kset

import sys

def jaccard(xs, ys):
    zX = len(xs)
    zY = len(ys)
    both = 0
    xonly = 0
    yonly = 0
    i = 0
    j = 0
    while i < zX and j < zY:
        x = xs[i]
        y = ys[j]
        if x < y:
            xonly += 1
            i += 1
        elif x > y:
            yonly += 1
            j += 1
        else: # x == y
            both += 1
            i += 1
            j += 1
    xonly += (zX - i)
    yonly += (zY - j)
    return float(both)/float(both + xonly + yonly)

if len(sys.argv) < 3:
    print >> sys.stderr, "usage: kset-jaccard.py <input-kset>...."
    sys.exit(1)

K = None
ksets = []
for fn in sys.argv[1:]:
    (meta, itr) = kset.read(fn)
    K0 = meta['K']
    if K is None:
        K = K0
    elif K0 != K:
        print >> sys.stderr, "K is not equal across ksets."
        sys.exit(1)
    xs = list(itr)
    ksets.append((fn, xs))

for i in xrange(len(ksets)):
    for j in xrange(i + 1, len(ksets)):
        d = jaccard(ksets[i][1], ksets[j][1])
        print '%s\t%s\t%f' % (ksets[i][0], ksets[j][0], d)
