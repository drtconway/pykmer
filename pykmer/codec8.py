"""
This module provides a sequential access variable byte coding scheme.

The basic method is to produce 1 or more 8-bit code words comprised of
7 data bits and a *continuation* bit. An encoded integer is composed of
zero or more code words with the continuation bit set, followed by exactly
one code word with an unset (0) continuation bit. The integer is composed
from the sequence of groups of 7 data bits, most significant "byte" first.
"""

__docformat__ = 'restructuredtext'

def encode(x):
    """
    Encode the integer `x` using a 7-bit+continuation-bit encoding,
    and return the list of 8-bit code words.
    """
    r = []
    while True:
        r.append(x & 127)
        x >>= 7
        if x == 0:
            break
    r = r[::-1]
    n = len(r) - 1
    i = 0
    while i < n:
        r[i] |= 128
        i += 1
    return r

def encodeInto(x, r):
    """
    Encode the integer `x` using a 7-bit+continuation-bit encoding,
    appending the 8-bit code words to an existing list/array.
    """
    n = 0
    y = x
    while True:
        n += 1
        y >>= 7
        r.append(0)
        if y == 0:
            break
    v = n
    i = -1
    m = 0
    while n > 0:
        r[i] = (x & 127) | m
        x >>= 7
        i -= 1
        m = 128
        n -= 1

def decode(itr):
    """
    Dencode an integer from a 7-bit+continuation-bit encoding, reading
    8-bit code words from the iterator `itr`.
    """
    r = 0
    x = itr.next()
    r = (x & 127)
    while x & 128:
        x = itr.next()
        r = (r << 7) | (x & 127)
    return r

