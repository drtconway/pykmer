
def encode(x):
    "encode an integer using a 7-bit+continuation-bit encodeing"
    r = []
    while True:
        r.append(x & 127)
        x >>= 7
        if x == 0:
            break
    r = r[::-1]
    for i in range(len(r) - 1):
        r[i] |= 128
    return r

def decode(itr):
    "dencode an integer from a 7-bit+continuation-bit encodeing"
    r = 0
    x = itr.next()
    r = (x & 127)
    while x & 128:
        x = itr.next()
        r = (r << 7) | (x & 127)
    return r

