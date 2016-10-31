import pykmer.codec8 as codec8

import random

def test_enc_0():
    x = 0
    y = codec8.encode(x)
    assert len(y) == 1
    assert y[0] == 0

def test_enc_127():
    x = 127
    y = codec8.encode(x)
    assert len(y) == 1
    assert y[0] == 127

def test_enc_128():
    x = 128
    y = codec8.encode(x)
    assert len(y) == 2
    assert y[0] == 129
    assert y[1] == 0

def test_dec_0():
    x = 0
    y = codec8.encode(x)
    z = codec8.decode(y.__iter__())
    assert x == z

def test_dec_127():
    x = 0
    y = codec8.encode(x)
    z = codec8.decode(y.__iter__())
    assert x == z

def test_dec_128():
    x = 0
    y = codec8.encode(x)
    z = codec8.decode(y.__iter__())
    assert x == z

def test_lots():
    N = 1000
    random.seed(17)
    for i in range(N):
        x = random.randint(0, 0xFFFFFFFFFFFFFF)
        y = codec8.encode(x)
        z = codec8.decode(y.__iter__())
        assert x == z
