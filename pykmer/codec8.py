
def encode(x):
    "encode an integer using a 7-bit+continuation-bit encodeing"
    r = []
    while True:
        r.append(x & 127)
        x >>= 7
        if x == 0:
            break
    r = r[::-1]
    n = len(r) - 1
    i = 0
    while i < n:
        r[i] |= 128
        i += 1
    return r

def encodeInto(x, r):
    "encode an integer using a 7-bit+continuation-bit encodeing into an existing list"
    n = 0
    y = x
    while True:
        n += 1
        y >>= 7
        r.append(0)
        if y == 0:
            break
    v = n
    i = -1
    m = 0
    while n > 0:
        r[i] = (x & 127) | m
        x >>= 7
        i -= 1
        m = 128
        n -= 1

def decode(itr):
    "dencode an integer from a 7-bit+continuation-bit encodeing"
    r = 0
    x = itr.next()
    r = (x & 127)
    while x & 128:
        x = itr.next()
        r = (r << 7) | (x & 127)
    return r

