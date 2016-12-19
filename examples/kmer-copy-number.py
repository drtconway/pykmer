from pykmer.basics import kmers
from pykmer.file import readFasta

import sys

if len(sys.argv) < 3:
    print >> sys.stderr, "usage: kmer-copy-number.py <K> <input-FASTA>...."
    sys.exit(1)

K = int(sys.argv[1])

xs = {}
for fn in sys.argv[2:]:
    with open(fn) as f:
        for (nm, seq) in readFasta(f):
            for x in kmers(K, seq, True):
                xs[x] = 1 + xs.get(x, 0)

h = {}
for (x, c) in xs.iteritems():
    h[c] = 1 + h.get(c, 0)

h = h.items()
h.sort()
for (c, f) in h:
    print '%d\t%d' % (c, f)
