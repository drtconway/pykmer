import pykmer.sparse as sparse

import array
import random

def test_empty():
    K = 27
    S = sparse.sparse(2*K, array.array('L', []))
    assert S.count() == 0
    assert S.rank(12345) == 0

def test_rank1():
    random.seed(17)
    K = 27
    M = (1 << (2*K)) - 1
    N = 1000
    xs = set([])
    for i in xrange(N):
        xs.add(random.randint(0, M))
    N = len(xs)
    xs = list(xs)
    xs.sort()
    S = sparse.sparse(2*K, array.array('L', xs))
    assert S.count() == N
    for i in xrange(N):
        assert S.rank(xs[i]) == i

def test_rank1():
    random.seed(17)
    K = 27
    M = (1 << (2*K)) - 1
    N = 1000
    xs = set([])
    for i in xrange(N):
        xs.add(random.randint(0, M))
    N = len(xs)
    ys = list(xs)
    ys.sort()
    S = sparse.sparse(2*K, array.array('L', ys))
    assert S.count() == N
    for i in xrange(N):
        r = S.access(ys[i])
        assert r is not None
        assert r == i
        s = S.rank(ys[i] + 1)
        assert s == r + 1

    for i in xrange(N):
        x = random.random(0, M)
        while x in xs:
            x = (x + random.randint(1, M)) & M
        a = S.access(x)
        assert a is None
        r = S.rank(x)
        if r < N:
            assert ys[r] > x
        else:
            assert ys[-1] < x
        if r > 0:
            assert ys[r-1] < x
        else:
            assert ys[0] > x

