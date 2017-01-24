"""
A module for constructing indexes over k-mers.

Indexes are built from 1 or more FASTA files, with each FASTA record
being a distinct entity. The index maps from k-mer back to the list
of FASTA records which contain that k-mer. Reverse complements are
included.
"""

__docformat__ = 'restructuredtext'

from pykmer.basics import kmers
from pykmer.misc import uniq
from pykmer.sparse import sparse
from pykmer.file import openFile, readFasta
from pykmer.container import container
from pykmer.container.std import readKmers, writeKmers
from pykmer.container.vectors import read32, write32, read16, write16

import array

class KmerIndex:
    """
    The KmerIndex object is loaded from a container, usually
    indirectly with the `index` function, created with the `buildIndex`
    function. It has three attributes of interest.

    `KmerIndex.K`
        is the value of K used for the index.
    `KmerIndex.names`
        is a list of the reference sequence names used for mapping
        the results of lookup back from sequence numbers to names.
    `KmerIndex[x]`
        is the lookup method for finding the reference sequence
        numbers for those sequences containing `x`.
    """
    def __init__(self, z):
        self.K = z.meta['K']
        S = array.array('L', readKmers(z))
        self.S = sparse(2*self.K, S)
        n = z.meta['T']
        self.T = array.array('I', read32(z, 'offsets', n))
        n = z.meta['U']
        self.U = array.array('H', read16(z, 'postings', n))
        n = z.meta['lens']
        self.lens = array.array('I', read32(z, 'lens', n))
        self.names = z.meta['names']

    def __getitem__(self, x):
        r = self.S.access(x)
        if r is None:
            return []
        res = []
        for i in xrange(self.T[r], self.T[r+1]):
            res.append(self.U[i])
        return res

def index(fn):
    """
    Load a k-mer index into memory and return the resulting KmerIndex
    object.
    """
    with container(fn, 'r') as z:
        idx = KmerIndex(z)
    return idx

def buildIndex(K, inputs, output):
    """
    Create a new k-mer index. The FASTA files named in the list
    `inputs` are read in and the `K` length k-mers and their reverse
    complements are extracted and collated to create an index that
    maps from k-mer to sequence number (numbering from 0). The
    `names` member of the KmerIndex object can be used to retrieve
    the name from the sequence number.
    """
    seqs = []
    for inp in inputs:
        with openFile(inp) as f:
            seqs += list(readFasta(f))

    S = []
    nms = []
    lens = array.array('I', [])
    for i in xrange(len(seqs)):
        (nm, seq) = seqs[i]
        nms.append(nm)
        xs = list(kmers(K, seq, True))
        xs.sort()
        uniq(xs)
        seqs[i] = [nm, xs]
        lens.append(len(xs))
        S += xs
    S.sort()
    uniq(S)
    S = sparse(2*K, S)

    T = array.array('I', [0 for i in xrange(S.count() + 1)])
    for i in xrange(len(seqs)):
        for x in seqs[i][1]:
            r = S.rank(x)
            T[r] += 1

    t0 = 0
    for i in xrange(len(T)):
        t1 = t0 + T[i]
        T[i] = t0
        t0 = t1

    T0 = [c for c in T]
    U = array.array('H', [0 for i in xrange(t0)])
    for i in xrange(len(seqs)):
        for x in seqs[i][1]:
            r = S.rank(x)
            U[T0[r]] = i
            T0[r] += 1

    with container(output, 'w') as z:
        writeKmers(K, S.xs, z)
        n = write32(z, T, 'offsets')
        z.meta['T'] = n
        n = write16(z, U, 'postings')
        z.meta['U'] = n
        n = write32(z, lens, 'lens')
        z.meta['lens'] = n
        z.meta['names'] = nms
