# Examples

This directory contains several small sample programs that illustrate
various aspects of the Pykmer library.

The example programs use genome data from FASTA files. We have not
packaged here, but two examples which can be readily obtained and used
to try out these example programs can be retrieved from
 - https://www.ncbi.nlm.nih.gov/nuccore/NC_003098
 - https://www.ncbi.nlm.nih.gov/nuccore/NC_008533

### kmer-copy-number.py

    pypy kmer-copy-number.py 25 NC_003098.fasta

This program takes a FASTA format file and extracts *k*-mers of the
given length and records how many times each occurs in the input sequence.

### make-kset.py

    pypy make-kset.py 25 NC_003098.k25 NC_003098.fasta

This program takes a FASTA format file and extracts all the forward and
reverse complement *k*-mers, and aggregates them in to a sorted list,
then uses the kset module to write them out in a compressed form for
use by some of the other example programs.

### kset-prefix-density.py

    pypy kset-prefix-density.py 12 NC_003098.k25

This program takes a compressed *k*-mer set (as produced by make-kset.py),
and counts how many *k*-mers share each prefix of the given length
(e.g. 12 in the above invocation).  These counts are then compiled in
to a histogram.

### kset-jaccard.py

    pypy kset-jaccard.py NC_003098.k25 NC_008533.k25

This program takes two or more ksets and computes the pair-wise Jaccard
distances.  (The Jaccard distance is the size of the intersection divided
by the size of the union of two sets.)

### sample-kset.py

    pypy sample-kset.py 0.05 11 NC_008533.x25 NC_008533.k25

This program takes a probability and a seed and samples an input kset
in a determinist fashion so that any individual *k*-mer is sampled with
the given probability, but the sampling is determinist, in that for the
same seed, the same *k*-mers will always be included in, or excluded
from the output kset. As a result, this may be fuitfully combined with
the Jaccard distance example above to get approximate Jaccard distances
very quickly, by sampling both inputs with the same probability and seed.
