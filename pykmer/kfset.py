"""
This module provides functions for reading and writing sorted sequences
of <*k*-mer,frequency> pairs in a compressed representation.
"""

__docformat__ = 'restructuredtext'

from codec8 import encodeInto, decode
import pykmer.container as container
from exceptions import MetaDataIncompatible

import array

meta = {
    'type' : 'k-mer frequency set',
    'version' : 20160930,
    'K' : None
}


def write(k, xs, nm, extra = None):
    """
    Write a sorted sequence `xs` composed of *k*-mer-frequency pairs
    into a file named `nm` in a compressed format.

    If the parameter `extra` is supplied, it should be dictionary of
    key-value pairs representing additional metadata to be stored with
    the *k*-mer-frequency pairs.

    At a minimum, the metadata written will contain 'K' giving `k`.
    """
    m = meta.copy()
    m['K'] = k
    if extra is not None:
        for (k, v) in extra.items():
            if k in m and m[k] != v:
                raise MetaDataIncompatible(k, m[k], v)
            m[k] = v
    f = container.make(nm, m)
    p = 0
    for (x,c) in xs:
        assert x == 0 or p < x
        d = x - p
        bs = array.array('B')
        encodeInto(d, bs)
        encodeInto(c, bs)
        bs.tofile(f)
        p = x

def read0(itr):
    "read0 is for internal use only."
    x = 0
    while True:
        try:
            x += decode(itr)
            c = decode(itr)
            yield (x,c)
        except StopIteration:
            return

def read(nm):
    """
    Read the file `nm` and read from it the metadata and construct an
    iterator to the  sorted sequence of kmer-frequency pairs writen with
    the function `write` in this module.

    The metadata dictionary returned will contain at least the key 'K'
    for the size of the *k*-mers.
    """
    (m, itr) = container.probe(nm, meta)
    return (m, read0(itr))

def probeK(nm):
    """
    Open the file called `nm`, and read the metadata to determine the
    value of 'K'.
    """
    (m, itr) = container.probe(nm, meta)
    return m['K']
