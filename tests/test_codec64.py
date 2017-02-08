import pykmer.codec64 as codec64

import math
import random

def test_enc_0():
    xs = [0]
    ys = list(codec64.encode(xs))
    assert len(ys) == 1
    assert ys[0] == 1

def test_enc_0():
    xs = [1]
    ys = list(codec64.encode(xs))
    assert len(ys) == 1
    assert ys[0] == 17

def test_enc_dec():
    N = 4000
    xs = [int(math.exp(10*random.random())) for i in xrange(N)]
    ys = list(codec64.encode(xs))
    zs = list(codec64.decode(ys))
    assert len(xs) == len(zs)
    for i in xrange(len(xs)):
        assert xs[i] == zs[i]

