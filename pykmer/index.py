from pykmer.basics import kmers
from pykmer.misc import uniq
from pykmer.sparse import sparse
from pykmer.file import openFile, readFasta
from pykmer.container import container
from pykmer.container.std import readKmers, writeKmers
from pykmer.container.vectors import read32, write32, read16, write16

import array

class KmerIndex:
    def __init__(self, z):
        self.K = z.meta['K']
        S = array.array('L', readKmers(z))
        self.S = sparse(2*self.K, S)
        n = z.meta['T']
        self.T = array.array('I', read32(z, 'offsets', n))
        n = z.meta['U']
        self.U = array.array('H', read16(z, 'postings', n))
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
    with container(fn, 'r') as z:
        idx = KmerIndex(z)
    return idx

def buildIndex(K, inputs, output):
    seqs = []
    for inp in inputs:
        with openFile(inp) as f:
            seqs += list(readFasta(f))

    S = []
    nms = []
    for i in xrange(len(seqs)):
        (nm, seq) = seqs[i]
        nms.append(nm)
        xs = list(kmers(K, seq))
        xs.sort()
        uniq(xs)
        seqs[i] = [nm, xs]
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
        z.meta['names'] = nms
