from pykmer.file import tmpfile
import pykmer.container as container
import pykmer.container.vectors as vecs
import pykmer.container.std as std

import math
import os
import random
import pytest

def test_rw_0():
    K = 27
    M = (1 << (2*K)) - 1
    N = 100000
    random.seed(17)
    xs = [random.randint(0, M) for i in xrange(N)]
    nm = tmpfile()
    with container.container(nm, 'w') as z:
        with vecs.writer64(z, "wibble") as w:
            for x in xs:
                w.append(x)
    with container.container(nm, 'r') as z:
        ys = list(vecs.read64(z, 'wibble', N))

    assert len(ys) == N
    for i in xrange(N):
        assert xs[i] == ys[i]

    os.remove(nm)

def test_rw_1():
    K = 27
    M = (1 << (2*K)) - 1
    N = 100000
    random.seed(17)
    xs = [random.randint(0, M) for i in xrange(N)]
    nm = tmpfile()
    with container.container(nm, 'w') as z:
        vecs.write64(z, xs, "wibble")
    with container.container(nm, 'r') as z:
        ys = list(vecs.read64(z, 'wibble', N))

    assert len(ys) == N
    for i in xrange(N):
        assert xs[i] == ys[i]

    os.remove(nm)

def test_rw_2():
    K = 27
    M = (1 << (2*K)) - 1
    N = 100000
    random.seed(17)
    xs = [random.randint(0, M) for i in xrange(N)]
    nm = tmpfile()
    with container.container(nm, 'w') as z:
        w = vecs.writer64(z, "wibble")
        for x in xs:
            w.append(x)
    with pytest.raises(KeyError):
        with container.container(nm, 'r') as z:
            ys = list(vecs.read64(z, 'wibble', N))

    os.remove(nm)

def pois(lam):
    lam = float(lam)
    x = 0
    p = math.exp(-lam)
    s = p
    u = random.random()
    while u > s:
        x += 1
        p *= lam/x
        s += p
    return x

def test_std_0():
    K = 27
    M = (1 << (2*K)) - 1
    N = 100000
    random.seed(17)
    xs = [(random.randint(0, M), pois(10)) for i in xrange(N)]
    nm = tmpfile()
    with container.container(nm, 'w') as z:
        std.writeKmersAndCounts(K, xs, z, 'wibble')
    with container.container(nm, 'r') as z:
        ys = list(std.readKmersAndCounts(z, 'wibble'))

    assert len(ys) == N
    for i in xrange(N):
        assert xs[i] == ys[i]

    os.remove(nm)

