"""
A 64-bit word based codec.  The 64-bit word is divided in to 4 tag
bits in the low-order positions, and the remaining 60 bits are
divided in to equal sized codes:

Number  Width
1       60
2       30
3       20
4       15
5       12
6       10
7        8
8        7
10       6
12       5
15       4
20       3
30       2
60       1

The 4-bit tag is the number of codes.
"""

# The maximum number of codes we can fit in a 64-bit word
W = 60

_codes = {}
for i in xrange(1, W+1):
    b = W // i
    _codes[b] = i

_lookup = [(0, 64) for i in xrange(W+1)]
for i in xrange(1, W+1):
    b = W // i
    j = W % i
    if j == 0:
        _lookup[i] = (b, i)
    else:
        _lookup[i] = _lookup[i - 1]

def encode(xs):
    """
    Encode a sequence of integers in the range [0,2^60) yielding a
    sequence of 64-bit codes.
    """
    stk = []
    n = 0
    mw = 0
    for x in xs:
        wx = x.bit_length()
        mwx = max(wx, mw)
        if n == W or mwx > _lookup[n+1][0] or n >= _lookup[n+1][1]:
            (b, m0) = _lookup[n]
            m = m0
            v = 0
            while m > 0:
                m -= 1
                v = (v << b) | stk[m]
            v = (v << 4) | m0
            yield v
            del stk[0:m0]
            n = len(stk)
            if n > 0:
                mw = max([y.bit_length() for y in stk])
                mwx = max(wx, mw)
            else:
                mwx = wx
        stk.append(x)
        n += 1
        mw = mwx
    if n > 0:
        (b, m0) = _lookup[n]
        m = m0
        v = 0
        while m > 0:
            m -= 1
            v = (v << b) | stk[m]
        v = (v << 4) | m0
        yield v

def decode(ws):
    """
    Take a sequence of 64-bit code words and decode them yielding
    a sequence of integers.
    """
    for w in ws:
        m0 = w & 15
        w >>= 4
        b = _codes[m0]
        msk = (1 << b) - 1
        while m0 > 0:
            yield (w & msk)
            w >>= b
            m0 -= 1
