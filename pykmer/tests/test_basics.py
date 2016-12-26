import pykmer.basics as basics

import random

def binary(x):
    r = []
    while x > 0:
        r.append("01"[x&1])
        x >>= 1
    return ''.join(r[::-1])

def test_kmer_polyA():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAA"
    x = basics.kmer(s)
    assert x == 0

def test_kmer_polyAC():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAC"
    x = basics.kmer(s)
    assert x == 1

def test_kmer_polyAG():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAG"
    x = basics.kmer(s)
    assert x == 2

def test_kmer_polyAT():
    s = "AAAAAAAAAAAAAAAAAAAAAAAAT"
    x = basics.kmer(s)
    assert x == 3

def test_kmer_CpolyA():
    s = "CAAAAAAAAAAAAAAAAAAAAAAAA"
    x = basics.kmer(s)
    assert x == (1 << 48)

def test_rc_1():
    s = "CTTTTTTT"
    k = len(s)
    x = basics.kmer(s)
    y = basics.rc(k, x)
    assert y == 2

def test_ham():
    random.seed(17)
    k = 25
    a = ''.join([random.choice("ACGT") for i in range(k)])
    b = ''.join([random.choice("ACGT") for i in range(k)])
    x = basics.kmer(a)
    y = basics.kmer(b)
    h = 0
    for i in range(k):
        if a[i] != b[i]:
            h += 1
    j = basics.ham(x, y)
    assert h == j

def test_lev():
    s0 = "CAAAAAAAAAAAAAAAATTTTTTTT"
    s1 = "CAAAAAAAAAAAAATTTTTTTTCGG"
    k = len(s0)
    x0 = basics.kmer(s0)
    x1 = basics.kmer(s1)
    assert basics.lev(k, x0, x1) == 3

def test_lcp():
    random.seed(17)
    k = 25
    a = ''.join([random.choice("ACGT") for i in range(k)])
    x = basics.kmer(a)
    y = x ^ (1 << 18)
    b = basics.render(k, y)
    h = 0
    for i in range(k):
        h = i
        if a[i] != b[i]:
            break
    j = basics.lcp(k, x, y)
    assert h == j

def test_kmers():
    s = "CCTCGTACGCCATATTTTCGCATTTCACGTACGTATTGTTTTTGCAACATAATTACCTATTCTCTTTTGGGGGGGGTTTTAGGCATTCCATTTAATNGCTTTTCTTTTAATGCATGGAGTTTTTCCCATTCATCCTTTGATATATTATCTTTACTTGCTTCGAAGTCTNTTGCTGTGAGATGTATATCTTCTGGATGGATTTGTTTACGTTCTTTTGTTACTGGATCTATAGTAAATGGAATCATTTCCTT"
    k = 25
    xs = list(basics.kmers(k, s, False))
    ys = []
    for i in range(len(s) - k + 1):
        y = basics.kmer(s[i:i+k])
        if y is not None:
            ys.append(y)
    assert xs == ys

def test_kmers_both():
    s = "CCTCGTACGCCATATTTTCGCATTTCACGTACGTATTGTTTTTGCAACATAATTACCTATTCTCTTTTGGGGGGGGTTTTAGGCATTCCATTTAATNGCTTTTCTTTTAATGCATGGAGTTTTTCCCATTCATCCTTTGATATATTATCTTTACTTGCTTCGAAGTCTNTTGCTGTGAGATGTATATCTTCTGGATGGATTTGTTTACGTTCTTTTGTTACTGGATCTATAGTAAATGGAATCATTTCCTT"
    k = 25
    xs = list(basics.kmers(k, s, True))
    ys = []
    for i in range(len(s) - k + 1):
        y = basics.kmer(s[i:i+k])
        if y is not None:
            ys.append(y)
            ys.append(basics.rc(k, y))
    assert xs == ys
