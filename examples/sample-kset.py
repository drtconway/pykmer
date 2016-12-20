from pykmer.basics import fnv
import pykmer.kset as kset

import sys

def sample(p, s, xs):
    for x in xs:
        u = float(fnv(x, s) & 0xFFFFFFFFFFFF) / float(0xFFFFFFFFFFFF)
        if u < p:
            yield x

if len(sys.argv) != 5:
    print >> sys.stderr, "usage: sample-kset.py <probability> <seed> <output-kset> <input-kset>"
    sys.exit(1)

p = float(sys.argv[1])
s = int(sys.argv[2])

(meta, itr) = kset.read(sys.argv[4])
K = meta['K']

kset.write(K, sample(p, s, itr), sys.argv[3])
