import pykmer.misc as misc

import random

def test_uniq_empty():
    xs = []
    misc.uniq(xs)
    assert len(xs) == 0

def test_uniq_singleton():
    xs = [1]
    misc.uniq(xs)
    assert len(xs) == 1
    assert xs[0] == 1

def test_uniq_simple():
    xs = [i for i in xrange(10)]
    print xs
    misc.uniq(xs)
    print xs
    assert len(xs) == 10
    for i in xrange(10):
        assert xs[i] == i

def test_uniq_few():
    xs = [1, 1, 2, 3, 3, 3, 4]
    misc.uniq(xs)
    assert len(xs) == 4
    assert xs[0] == 1
    assert xs[1] == 2
    assert xs[2] == 3
    assert xs[3] == 4

def test_uniq_many():
    xs = []
    ys = set([])
    random.seed(17)
    N = 100000
    for i in xrange(N):
        x = random.randint(0, 1000)
        xs.append(x)
        ys.add(x)
    ys = list(ys)
    ys.sort()
    xs.sort()
    misc.uniq(xs)
    assert len(xs) == len(ys)
    for i in xrange(len(xs)):
        assert xs[i] == ys[i]

def test_radix_sort():
    random.seed(17)
    N = 16*1024*1024
    K = 27
    M = (1 << (2*K)) - 1
    xs = []
    for i in xrange(N):
        xs.append(random.randint(0, M))
    misc.radix_sort(2*K, xs)
    for i in xrange(1, N):
        assert xs[i - 1] <= xs[i]
