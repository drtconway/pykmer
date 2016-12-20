"""
This module provides a collection of useful statistical functions.

In most cases, they produce logarithmic results. This is useful, because
for many applications in genomic analysis, the numbers (dimensions,
sample sizes, multiple testing, etc) become large, and we need to use
the extreme tails of the distributions where the values are extreme.

Many of the implementations here were inspired by
http://www.fysik.su.se/~walck/suf9601.pdf
"""
import math
import sys

def log1mexp(a):
    """
    return log(1 - exp(a))
    """
    if a < 0.6931472:
        return math.log(-math.expm1(a))
    else:
        return math.log1p(-math.exp(a))

def factorial(n):
    """
    return n!
    """
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
    """
    return log(gamma(x))
    """
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
    """
    return log(n!)
    """
    if n < len(small):
        return small[n]
    return n * math.log(n) - n + math.log(n*(1+4*n*(1+2*n)))/6.0 + math.log(math.pi)/2.0

def logAdd(a, b):
    """
    return log(exp(a) + exp(b))
    """
    x = max(a, b)
    y = min(a, b)
    w = y - x
    return x+math.log1p(math.exp(w))

def logSum(xs):
    """
    return log(sum([exp(x) for x in xs]))
    """
    assert len(xs) > 0
    y = xs[0]
    for x in xs[1:]:
        y = logAdd(y, x)
    return y

def logChoose(n, k):
    """
    Combinatoric choice.
    Returns log(n! / ((n-k)!*k!))
    """
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
    """
    Compute the log of the nomalized lower incomplete gamma function

    P(a, x) = lowerGamma(a, x)/gamma(a)
    """
    return logLowerGamma(a, x) - logGamma(a)

def gammaP(a, x):
    """
    Compute the nomalized lower incomplete gamma function

    P(a, x) = lowerGamma(a, x)/gamma(a)
    """
    return math.exp(logGammaP(a, x))

def logGammaQ(a, x):
    """
    Compute the log of the nomalized upper incomplete gamma function

    P(a, x) = upperGamma(a, x)/gamma(a)
    """
    return log1mexp(logGammaP(a, x))

def gammaQ(a, x):
    """
    Compute the nomalized upper incomplete gamma function

    P(a, x) = upperGamma(a, x)/gamma(a)
    """
    return math.exp(logGammaQ(a, x))

def logBeta(a, b):
    """
    Compute the log of the beta function beta(`a`, `b`). 
    """
    return logGamma(a) + logGamma(b) - logGamma(a + b)

def logBinEq(p, n, k):
    """
    Compute the log of the binomial probability 

        Bin(p, n, X = k)
    """
    lp = math.log(p)
    l1mp = math.log1p(-p)
    return logChoose(n, k) + lp*k + l1mp*(n - k)

def logBinLe(p, n, k):
    """
    Compute the log of the binomial probability 

        Bin(p, n, X <= k)
    """
    lp = math.log(p)
    l1mp = math.log1p(-p)
    v = logChoose(n, k) + lp*k + l1mp*(n - k)
    for j in xrange(1, k+1):
        i = k - j
        w = logChoose(n, i) + lp*i + l1mp*(n - i)
        v = logAdd(v, w)
    return v

def logBinGe(p, n, k):
    """
    Compute the log of the binomial probability 

        Bin(p, n, X >= k)
    """
    lp = math.log(p)
    l1mp = math.log1p(-p)
    v = logChoose(n, k) + lp*k + l1mp*(n - k)
    for j in xrange(k+1, n+1):
        w = logChoose(n, j) + lp*j + l1mp*(n - j)
        v = logAdd(v, w)
    return v

def pdf2cdf(xs):
    """
    Convert the PDF P(X==i) to the CDF P(X<i)
    """
    t = 0
    ys = []
    for x in xs:
        ys.append(t)
        t += x
    return ys

def counts2pdf(xs):
    """
    Convert the vector of counts `xs` to a discrete PDF.
    """
    n = sum(xs)
    return [float(x)/n for x in xs]

def counts2cdf(xs):
    """
    Convert the vector of counts `xs` to a discrete CDF.
    """
    return pdf2cdf(counts2pdf(xs))

def klDivergence(e, d):
    """
    return the Kullback-Leibler divergence between the two PDFs.
    """
    v = 0
    for (x, y) in zip(e, d):
        if y == 0:
            continue
        v += y * math.log(y/x)
    return v

def ksDistance(l, r):
    """
    return the Kolmogorov-Smirnov distance between to CDFs
    """
    assert len(l) == len(r)
    d = 0
    for (x, y) in zip(l, r):
        d = max(d, abs(x - y))
    return d

def ksDistance2(l, r):
    """
    return the 2 1-sided Kolmogorov-Smirnov distances between to CDFs
    """
    assert len(l) == len(r)
    dl = 0
    dr = 0
    for (x, y) in zip(l, r):
        dl = max(dl, x - y)
        dr = max(dr, y - x)
    return (dl, dr)

