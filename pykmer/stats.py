import math

def factorial(n):
    r = 1
    for i in range(2, n):
        r *= i
    return r

small = [math.log(n) for n in range(25)]

def logFac(n):
    if n < len(small):
        return small[n]
    return n * math.log(n) - n + math.log(n*(1+4*n*(1+2*n)))/6.0 + math.log(math.pi)/2.0

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
