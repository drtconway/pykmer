from pykmer.basics import render
import pykmer.kset as kset

import sys

if len(sys.argv) != 3:
    print >> sys.stderr, "usage: kset-prefix-density.py <prefix-length> <input-kset>"
    sys.exit(1)

J = int(sys.argv[1])

(meta, itr) = kset.read(sys.argv[2])
K = meta['K']
S = 2*(K - J)

h = {}

p = None
n = 0
for x in itr:
    y = x >> S
    if y != p:
        if n > 0:
            h[n] = 1 + h.get(n, 0)
        p = y
        n = 0
    n += 1
if n > 0:
    h[n] = 1 + h.get(n, 0)

h = h.items()
h.sort()
for (n, c) in h:
    print '%d\t%d' % (n, c)
