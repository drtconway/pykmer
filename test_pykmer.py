import pykmer

import random

def binary(x):
    r = []
    while x > 0:
        r.append("01"[x&1])
        x >>= 1
    return ''.join(r[::-1])

def test_make_kmer_polyA():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAA"
    x = pykmer.make_kmer(s)
    assert x == 0

def test_make_kmer_polyAC():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAC"
    x = pykmer.make_kmer(s)
    assert x == 1

def test_make_kmer_polyAG():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAG"
    x = pykmer.make_kmer(s)
    assert x == 2

def test_make_kmer_polyAT():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAT"
    x = pykmer.make_kmer(s)
    assert x == 3

def test_make_kmer_CpolyA():
    s = "CAAAAAAAAAAAAAAAAAAAAAAAA"
    x = pykmer.make_kmer(s)
    assert x == (1 << 48)

def test_rc_1():
    s = "CTTTTTTT"
    k = len(s)
    x = pykmer.make_kmer(s)
    y = pykmer.rc(k, x)
    assert y == 2

def test_popcnt():
    x = 466311136197825
    y = x
    c = 0
    while y > 0:
        c += y&1
        y >>= 1
    j = pykmer.popcnt(x)
    assert c == j

def test_ham():
    random.seed(17)
    k = 25
    a = ''.join([random.choice("ACGT") for i in range(k)])
    b = ''.join([random.choice("ACGT") for i in range(k)])
    x = pykmer.make_kmer(a)
    y = pykmer.make_kmer(b)
    h = 0
    for i in range(k):
        if a[i] != b[i]:
            h += 1
    j = pykmer.ham(x, y)
    assert h == j

def test_lcp():
    random.seed(17)
    k = 25
    a = ''.join([random.choice("ACGT") for i in range(k)])
    x = pykmer.make_kmer(a)
    y = x ^ (1 << 18)
    b = pykmer.render(k, y)
    h = 0
    for i in range(k):
        h = i
        if a[i] != b[i]:
            break
    j = pykmer.lcp(k, x, y)
    assert h == j
