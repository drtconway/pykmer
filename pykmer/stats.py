import math
import sys

def factorial(n):
    r = 1
    for i in xrange(2, n+1):
        r *= i
    return r

small = [math.log(factorial(n)) for n in xrange(25)]

B2k = {0:   1.0,
       1:   -0.5,
       2:   1.0/6.0,
       4:   -1.0/30.0,
       6:   1.0/42.0,
       8:   -1.0/30.0,
       10:  5.0/66.0,
       12:  -691.0/2730.0,
       14:  7.0/6.0,
       16:  -3617.0/510.0,
       18:  43867.0/798.0,
       20:  -174611.0/330.0}

def logGamma(x):
    if x < 0:
        return math.log(math.pi) + logGamma(1 - x) - math.log(math.sin(math.pi*x))
    if x < 7:
        n = 7 - int(x)
        p = 1
        for k in xrange(0, n):
            p *= (x + k)
        return logGamma(x + n) - math.log(p)
    s = 0
    for k in xrange(1, 11):
        s += B2k[2*k] / (2*k * (2*k - 1)) * math.pow(x, -2*k)
    return (x - 0.5)*math.log(x) - x + 0.5*math.log(2*math.pi) + x*s

def logFac(n):
    if n < len(small):
        return small[n]
    return n * math.log(n) - n + math.log(n*(1+4*n*(1+2*n)))/6.0 + math.log(math.pi)/2.0

def logAdd(a, b):
    x = max(a, b)
    y = min(a, b)
    w = y - x
    return x+math.log1p(math.exp(w))

def logSum(xs):
    assert len(xs) > 0
    y = xs[0]
    for x in xs[1:]:
        y = logAdd(y, x)
    return y

def logChoose(n, k):
    if k == 0 or k == n:
        return 0
    return logFac(n) - (logFac(n - k) + logFac(k))

def logLowerGamma(a, x):
    lx = math.log(x)
    ls = None
    for n in xrange(2000):
        if ls is None:
            ls = n*lx + logGamma(a) - logGamma(a + n + 1)
        else:
            v = n*lx + logGamma(a) - logGamma(a + n + 1)
            if ls - v > 50:
                break
            ls = logAdd(ls, v)
    return a*lx + ls - x

def logGammaP(a, x):
    return logLowerGamma(a, x) - logGamma(a)

def gammaP(a, x):
    return math.exp(logGammaP(a, x))

def logGammaQ(a, x):
    return math.log1p(-gammaP(a, x))

def gammaQ(a, x):
    return 1 - gammaP(a, x)

def normalCDF(x):
    if x == 0:
        return 0.5
    elif x > 0:
        return 0.5 + 0.5 * gammaP(0.5, 0.5*x*x)
    else:
        return 0.5 - 0.5 * gammaP(0.5, 0.5*x*x)

def pdf2cdf(xs):
    "Convert the PDF P(X==i) to the CDF P(X<i)"
    t = 0
    ys = []
    for x in xs:
        ys.append(t)
        t += x
    return ys

def counts2pdf(xs):
    n = sum(xs)
    return [float(x)/n for x in xs]

def counts2cdf(xs):
    return pdf2cdf(counts2pdf(xs))

def ksDistance(l, r):
    "return the Kolmogorov-Smirnov distance between to CDFs"
    assert len(l) == len(r)
    d = 0
    for (x, y) in zip(l, r):
        d = max(d, abs(x - y))
    return d

def ksDistance2(l, r):
    "return the 2 1-sided Kolmogorov-Smirnov distances between to CDFs"
    assert len(l) == len(r)
    dl = 0
    dr = 0
    for (x, y) in zip(l, r):
        dl = max(dl, x - y)
        dr = max(dr, y - x)
    return (dl, dr)

def logChi2CDF(n, x):

    if n < 10:
        lcdf = min(0, logLowerGamma(n/2.0, x/2.0) - logGamma(n/2.0))
        if lcdf < -1e-12:
            return math.log1p(-math.exp(lcdf))

    x = float(x)
    if n & 1:
        # odd...
        m = (n - 1)/2
        lu = 0
        ls = None
        i = 0
        while i <= m - 1:
            if ls is None:
                ls = lu
            else:
                ls = logAdd(ls, lu)
            i += 1
            lu += math.log(x/(2*i + 1))
        s = math.exp(ls)
        return logAdd(math.log(2 - 2*normalCDF(math.sqrt(x))), math.log(math.sqrt(2*x/math.pi)) + ls - x/2)
    else:
        # even...
        m = n/2 - 1
        lu = 0.0
        ls = None
        i = 0
        while i <= m:
            if ls is None:
                ls = lu
            else:
                ls = logAdd(ls, lu)
            i += 1
            lu += math.log(x/(2*i))
        return min(0, ls - x/2)

def chi2CDF(n, x):
    x = float(x)
    if n & 1:
        # odd...
        m = (n - 1)/2
        u = 1.0
        s = 0
        for i in xrange(1, m):
            u *= x/(2*i + 1)
            s += u
        return 2 - 2*normalCDF(math.sqrt(x)) \
                 + math.sqrt(2*x/math.pi) * math.exp(-x/2.0) * s
    else:
        # even...
        m = n/2 - 1
        u = 1.0
        s = 0
        for i in xrange(1, m+1):
            u *= x/(2*i)
            s += u
        return s * math.exp(-x/2.0)

def logChi2Crit(n, conf):
    h = 2 * n
    while True:
        pv0 = logChi2CDF(n, h)
        if pv0 < conf:
            break
        h *= 2
    l = 0
    j = 0
    while l < h:
        m = (l + h) / 2.0
        pv0 = logChi2CDF(n, m)
        if pv0 < conf:
            h = m - 0.001
        else:
            l = m + 0.001
        j += 1
        if j > 100:
            raise StopIteration
    return l
