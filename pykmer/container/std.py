"""
This module provides functions for reading and writing sorted sequences
of *k*-mers in a compressed representation.
"""

__docformat__ = 'restructuredtext'

import pykmer.container.vectors as vectors

def writeKmers(K, xs, z):
    nm = str(K) + '-mers'
    n = vectors.write64(z, xs, nm)
    z.manifest[nm]['kind'] = 'k-mers'
    z.manifest[nm]['K'] = K
    z.manifest[nm]['N'] = n
    return n

def readKmers(z, which=None):
    if which is None:
        cs = z.find(kind='k-mers')
        if len(cs) == 0:
            raise "no k-mers"
        if len(cs) > 1:
            raise "multiple k-mers"
        nm = cs[0]
    else:
        nm = which
    n = z.manifest[nm]['N']
    return (z.manifest[nm], vectors.read64(z, nm, n))

def writeCounts(K, xs, z):
    nm = str(K) + '-counts'
    n = vectors.write32(z, xs, nm)
    z.manifest[nm]['kind'] = 'k-mer counts'
    z.manifest[nm]['K'] = K
    z.manifest[nm]['N'] = n
    return n

def readCounts(z, which=None):
    if which is None:
        cs = z.find(kind='k-mer counts')
        if len(cs) == 0:
            raise "no k-mer counts"
        if len(cs) > 1:
            raise "multiple k-mer counts"
        nm = cs[0]
    else:
        nm = which
    n = z.manifest[nm]['N']
    return (z.manifest[nm], vectors.read32(z, nm, n))

def writeKmersAndCounts(K, vs, z):
    (xs, cs) = zip(*vs)
    writeKmers(K, xs, z)
    writeCounts(K, cs, z)

def readKmersAndCounts(z, which=None):
    if which is None:
        (m0, xs) = readKmers(z)
        (m1, cs) = readCounts(z)
    else:
        (m0, xs) = readKmers(z, which + '-kmers')
        (m1, cs) = readCounts(z, which + '-counts')
    assert m0['K'] == m1['K']
    assert m0['N'] == m1['N']
    return zip(xs, cs)

