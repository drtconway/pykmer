"""
This example program demonstrates how to extract k-mers from
a sequence in a FASTA file, and compute a k-mer frequency
histogram. It is not expected to work for large genomes (i.e.
the human genome), as it is not particularly memory-efficient.

example usage:
$ pypy  histogram-ref.py 8 poliovirus.fa.gz
1       10978
2       1596
3       188
4       28
5       4
$
"""

from pykmer.basics import kmers
from pykmer.file import readFasta

import sys
import gzip

K = int(sys.argv[1])

# Step 1
# Open the gzipped file directly, rather than uncompressing it.
# If space is not an issue, it's usually faster to use uncompressed
# files, but it's pretty convenient to be able open the compressed
# file.
#
xs = {}
with gzip.open(sys.argv[2]) as f:
    # Now parse the FASTA file, to get the <name, sequence> pairs.
    for (nm, seq) in readFasta(f):
        # From each sequence extract k-mers.
        #
        # Note that the kmers() function is a generator - it uses
        # yield to return each k-mer in turn rather than composing
        # them in to a list or a set.
        #
        # The third argument is a boolean flag that indicates whether
        # or not to return reverse complement versions of the k-mers
        # as well as the "forward" ones in the sequence.
        for x in kmers(K, seq, True):
            # If this is the first instance of this k-mer
            # initialize an entry in the dict.
            if x not in xs:
                xs[x] = 0
            # Add this k-mer instance
            xs[x] += 1

# Step 2
# Iterate over the dictionary, and compile the k-mer frequency
# histogram.
#
hist = {}
for (x,f) in xs.iteritems():
    if f not in hist:
        hist[f] = 0
    hist[f] += 1

# Now print the results.
hist = hist.items()
hist.sort()
for (f,c) in hist:
    print '%d\t%d' % (f, c)
