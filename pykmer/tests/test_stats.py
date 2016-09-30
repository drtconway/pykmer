import pykmer.stats as ps

import math
import random

def about_equal(x, y, p):
    d = abs(x - y)
    
    if y == 0 and d > 0:
        return -math.log(d) > p
    if d == 0:
        return True
    return -math.log(d/abs(y)) > p

def test_logGamma():
    xs = range(1, 10+1)
    rs = [0.000000000000000000000000,
          0.000000000000000000000000,
          0.693147180559945286226764,
          1.791759469228054957312679,
          3.178053830347945751810812,
          4.787491742782045811566149,
          6.579251212010101212968038,
          8.525161361065414666882134,
          10.604602902745250858629333,
          12.801827480081469090578139]
    for (x,r) in zip(xs, rs):
        v = ps.logGamma(x)
        assert about_equal(v, r, 24)

    assert about_equal(ps.logGamma(1234), 7546.991994272256306430790573, 24)

def test_logFac():
    for n in range(100):
        r = 0.0
        for i in range(1, n+1):
            r += math.log(i)
        v = ps.logFac(n)
        assert about_equal(v, r, 10)

def test_logGamma_logFac_a():
    random.seed(17)
    for n in range(100):
        x = int(2000*random.random() + 1)
        v = ps.logFac(x)
        w = ps.logGamma(x + 1)
        assert about_equal(v, w, 10)

def test_logGamma_logFac_b():
    random.seed(17)
    for n in range(100):
        x = 2000*random.random() + 1
        y = int(math.floor(x))
        z = int(math.ceil(x))
        u = ps.logFac(y)
        v = ps.logFac(z)
        w = ps.logGamma(x + 1)
        assert u <= w
        assert w <= v

def test_logAdd():
    random.seed(17)
    for n in range(100):
        x = random.expovariate(0.01)
        lx = math.log(x)
        y = random.expovariate(0.01)
        ly = math.log(y)
        lz = ps.logAdd(lx, ly)
        z = x + y
        assert about_equal(lz, math.log(z), 24)

def test_logSum():
    random.seed(17)
    xs = [random.expovariate(0.01) for n in range(100)]
    sx = sum(xs)
    lxs = map(math.log, xs)
    lsx = ps.logSum(lxs)
    assert about_equal(lsx, math.log(sx), 24)

def test_logLowerGamma_a():
    a = 20
    xs = range(12, 21)
    rs = [35.4898857353682899429259123,
          36.1855945082210794794264075,
          36.7694842252896876289014472,
          37.2586908322506076274294173,
          37.6672480372498554856974806,
          38.0068586344697649792578886,
          38.2874411225195245833674562,
          38.5175222510225694350083359,
          38.7045203877837309391907183]
    for (x,r) in zip(xs, rs):
        v = ps.logLowerGamma(a, x)
        assert about_equal(v, r, 24)

def test_normalCDF():
    assert about_equal(ps.normalCDF(0), 0.5, 24)
    assert about_equal(ps.normalCDF(0.5), 0.6914624612740130071841804, 24)
    assert about_equal(ps.normalCDF(1.0), 0.8413447460685429257765122, 24)
    assert about_equal(ps.normalCDF(-0.5), 0.3085375387259869373046683, 24)
    assert about_equal(ps.normalCDF(-1.0), 0.1586552539314570464679122, 24)

def test_chi2CDF():
    assert about_equal(ps.chi2CDF(10, 25), 0.0053455054871340661193369, 5)
    assert about_equal(ps.chi2CDF(11, 25), 0.0091166811255269913222277, 5)
    assert about_equal(ps.chi2CDF(12, 25), 0.0148228745974415473951602, 5)

def test_logChi2CDF():
    assert about_equal(ps.logChi2CDF(10, 25), -5.2314991670153032643497681, 5)
    assert about_equal(ps.logChi2CDF(11, 25), -4.6976494528024916874642258, 5)
    assert about_equal(ps.logChi2CDF(12, 25), -4.2115837104847466676460499, 5)
