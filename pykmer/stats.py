import math

def factorial(n):
    r = 1
    for i in range(2, n+1):
        r *= i
    return r

small = [math.log(factorial(n)) for n in range(25)]

def logGamma(n):
    return n * math.log(n) - n - 0.5*math.log(n/(2*math.pi)) + 1.0/(12*n) - 1.0/(360*n*n*n) + 1.0/(1260*math.pow(n,5))

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

def chi2LogPval(n, x):
    x = float(x)
    if n & 1:
        # odd...
        raise "xxx"
    else:
        # even...
        m = n/2 - 1
        lu = 0.0
        ls = None
        for i in range(1, m+1):
            lu += math.log(x/(2*i))
            if ls is None:
                ls = lu
            else:
                ls = logAdd(ls, lu)
        return ls - x/2

def chi2Pval(n, x):
    return math.exp(chi2LogPval(n, x))
