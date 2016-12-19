from pykmer.basics import kmers
from pykmer.file import readFasta
from pykmer.misc import uniq
import pykmer.kset as kset

import sys

if len(sys.argv) < 4:
    print >> sys.stderr, "usage: make-kset.py <K> <output-filename> <input-FASTA>...."

K = int(sys.argv[1])

xs = []
for fn in sys.argv[3:]:
    with open(fn) as f:
        for (nm, seq) in readFasta(f):
            xs += list(kmers(K, seq, True))

xs.sort()
uniq(xs)
kset.write(K, xs, sys.argv[2])
