from codec8 import encode, decode
import pykmer.container as container
from pykmer.exceptions import MetaDataIncompatible

meta = {
    'type' : 'k-mer set',
    'version' : 20160930,
    'K' : None
}

def write(K, xs, nm, extra = None):
    "write a sorted sequence of kmers in a compressed format"
    m = meta.copy()
    m['K'] = K
    if extra is not None:
        for (k, v) in extra.items():
            if k in m and m[k] != v:
                raise MetaDataIncompatible(k, m[k], v)
            m[k] = v
    f = container.make(nm, m)
    p = 0
    for x in xs:
        assert x == 0 or p < x
        d = x - p
        bs = bytearray(encode(d))
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

def read(nm):
    "read a sorted sequence of kmers from a compressed format"
    (m, itr) = container.probe(nm, meta)
    return (m, read0(itr))

def probeK(nm):
    (m, itr) = container.probe(nm, meta)
    return m['K']
