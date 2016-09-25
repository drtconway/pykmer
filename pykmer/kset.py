from codec8 import encode, decode

def write(k, xs, f):
    bs = bytearray(encode(k))
    f.write(bs)
    p = 0
    for x in xs:
        assert p < x
        d = x - p
        bs = bytearray(encode(x))
        f.write(bs)
        p = x

def read0(itr):
    x = 0
    while True:
        try:
            x += decode(itr)
            yield x
        except StopIteration:
            return

def read(f):
    bs = bytearray(f.read())
    itr = bs.__iter__()
    k = decode(itr)
    return (k, read0(itr))

