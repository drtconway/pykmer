
def encode(x):
    "encode an integer using a 15-bit+continuation-bit encodeing"
    r = []
    while True:
        r.append(x & 32767)
        x >>= 15
        if x == 0:
            break
    r = r[::-1]
    n = len(r) - 1
    i = 0
    while i < n:
        r[i] |= 32768
        i += 1
    return r

def encodeInto(x, r):
    "encode an integer using a 7-bit+continuation-bit encodeing into an existing list"
    n = 0
    y = x
    while True:
        n += 1
        y >>= 15
        r.append(0)
        if y == 0:
            break
    v = n
    i = -1
    m = 0
    while n > 0:
        r[i] = (x & 32767) | m
        x >>= 15
        i -= 1
        m = 32768
        n -= 1

def decode(itr):
    "dencode an integer from a 7-bit+continuation-bit encodeing"
    r = 0
    x = itr.next()
    r = (x & 32767)
    while x & 32768:
        x = itr.next()
        r = (r << 15) | (x & 32767)
    return r

