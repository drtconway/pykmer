"""
This module provides functions for reading and writing sorted sequences
of *k*-mers in a compressed representation.
"""

__docformat__ = 'restructuredtext'

import pykmer.container.vectors as vectors
from itertools import izip

def writeKmers(K, xs, z, nm=None):
    assert 'K' not in z.meta or z.meta['K'] == K
    assert nm is not None or 'kmers' not in z.meta

    if nm is None:
        nm = str(K) + '-mers'

    n = vectors.write64(z, xs, nm)
    z.meta['kmers'] = nm
    z.meta['K'] = K
    z.meta[nm + '-' + 'N'] = n

    return n

class KmerWriter:
    def __init__(self, K, z, nm = None):
        self.K = K
        if nm is None:
            nm = str(K) + '-mers'
        self.nm = nm
        self.z = z
        self.w = vectors.writer64(z, nm)

    def __enter__(self):
        return self.w

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        self.close()
        return True

    def close(self):
        self.w.close()
        self.z.meta['kmers'] = self.nm
        self.z.meta['K'] = self.K
        self.z.meta[self.nm + '-' + 'N'] = self.w.n

def kmerWriter(z, K, nm = None):
    return KmerWriter(K, z, nm)

def readKmers(z, nm = None):
    assert nm is not None or 'kmers' in z.meta

    if nm is None:
        nm = z.meta['kmers']

    K = z.meta['K']
    N = z.meta[nm + '-' + 'N']

    return vectors.read64(z, nm, N)

def readKmersBlock(z, nm = None):
    assert nm is not None or 'kmers' in z.meta

    if nm is None:
        nm = z.meta['kmers']

    K = z.meta['K']
    N = z.meta[nm + '-' + 'N']

    return vectors.read64block(z, nm, N)

def writeCounts(K, xs, z, nm=None):
    assert 'K' not in z.meta or z.meta['K'] == K
    assert nm is not None or 'counts' not in z.meta

    if nm is None:
        nm = str(K) + '-counts'

    n = vectors.write32(z, xs, nm)

    z.meta['counts'] = nm
    z.meta['K'] = K
    z.meta[nm + '-' + 'N'] = n

    return n

class CountsWriter:
    def __init__(self, K, z, nm = None):
        self.K = K
        if nm is None:
            nm = str(K) + '-counts'
        self.nm = nm
        self.z = z
        self.w = vectors.writer32(z, nm)

    def __enter__(self):
        return self.w

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        self.close()
        return True

    def close(self):
        self.w.close()
        self.z.meta['counts'] = self.nm
        self.z.meta['K'] = self.K
        self.z.meta[self.nm + '-' + 'N'] = self.w.n

def countsWriter(z, K, nm = None):
    return CountsWriter(K, z, nm)

def readCounts(z, nm = None):
    assert nm is not None or 'counts' in z.meta

    if nm is None:
        nm = z.meta['counts']

    K = z.meta['K']
    N = z.meta[nm + '-' + 'N']

    return vectors.read32(z, nm, N)

def readCountsBlock(z, nm = None):
    assert nm is not None or 'counts' in z.meta

    if nm is None:
        nm = z.meta['counts']

    K = z.meta['K']
    N = z.meta[nm + '-' + 'N']

    return vectors.read32Block(z, nm, N)

def writeKmersAndCounts(K, vs, z, nm = None):
    if nm is None:
        with KmerWriter(K, z) as kw:
            with CountsWriter(K, z) as cw:
                for (x,c) in vs:
                    kw.append(x)
                    cw.append(c)
    else:
        with KmerWriter(K, z, nm + '-kmers') as kw:
            with CountsWriter(K, z, nm + '-counts') as cw:
                for (x,c) in vs:
                    kw.append(x)
                    cw.append(c)

def writeKmersAndCountsBlock(K, vs, z, nm = None):
    if nm is None:
        with KmerWriter(K, z) as kw, CountsWriter(K, z) as cw:
                for (xs,cs) in vs:
                    kw.appendBlock(xs)
                    cw.appendBlock(cs)
    else:
        with KmerWriter(K, z, nm + '-kmers') as kw, CountsWriter(K, z, nm + '-counts') as cw:
                for (xs,cs) in vs:
                    kw.appendBlock(xs)
                    cw.appendBlock(cs)

def readKmersAndCounts(z, nm=None):
    if nm is None:
        xs = readKmers(z)
        cs = readCounts(z)
    else:
        xs = readKmers(z, nm + '-kmers')
        cs = readCounts(z, nm + '-counts')
    return izip(xs, cs)

def readKmersAndCountsBlock(z, nm=None):
    if nm is None:
        xs = readKmers(z)
        cs = readCounts(z)
    else:
        xs = readKmers(z, nm + '-kmers')
        cs = readCounts(z, nm + '-counts')

    B = 65536
    moreXs = True
    moreCs = True

    try:
        xsBlk = xs.next()
        xsZ = len(xsBlk)
    except StopIteration:
        moreXs = False

    try:
        csBlk = cs.next()
        csZ = len(csBlk)
    except StopIteration:
        moreCs = False

    blk = []
    i = 0
    j = 0
    n = 0
    while moreXs and moreYs:
        while i < xsZ and j < csZ and n < B:
            blk.append((xsBlk[i], csBlk[j]))

        if moreXs and i == xsZ:
            try:
                xsBlk = xs.next()
                xsZ = len(xsBlk)
                i = 0
            except StopIteration:
                moreXs = False

        if moreCs and j == csZ:
            try:
                csBlk = cs.next()
                csZ = len(csBlk)
                j = 0
            except StopIteration:
                moreCs = False

        if n == B:
            yield blk
            blk = []
            n = 0

    if n > 0:
        yield blk

    assert moreXs == False
    assert moreYs == False

