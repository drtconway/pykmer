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

