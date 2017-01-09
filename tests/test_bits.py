import pykmer.bits as bits
from pykmer.basics import kmer, render

import random

def test_popcnt():
    x = 466311136197825
    y = x
    c = 0
    while y > 0:
        c += y&1
        y >>= 1
    j = bits.popcnt(x)
    assert c == j
