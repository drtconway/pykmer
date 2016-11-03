from codec8 import encodeInto, decode
import pykmer.container as container
from exceptions import MetaDataIncompatible

import array

meta = {
    'type' : 'k-mer frequency set',
    'version' : 20160930,
    'K' : None
}


def write(k, xs, nm, extra = None):
    "write a sorted sequence of kmer-frequency pairs in a compressed format"
    m = meta.copy()
    m['K'] = k
    if extra is not None:
        for (k, v) in extra.items():
            if k in m and m[k] != v:
                raise MetaDataIncompatible(k, m[k], v)
            m[k] = v
    f = container.make(nm, m)
    p = 0
    for (x,c) in xs:
        assert x == 0 or p < x
        d = x - p
        bs = array.array('B')
        encodeInto(d, bs)
        encodeInto(c, bs)
        bs.tofile(f)
        p = x

def read0(itr):
    x = 0
    while True:
        try:
            x += decode(itr)
            c = decode(itr)
            yield (x,c)
        except StopIteration:
            return

def read(nm):
    "read a sorted sequence of kmer-frequency pairs from a compressed format"
    (m, itr) = container.probe(nm, meta)
    return (m, read0(itr))

def probeK(nm):
    (m, itr) = container.probe(nm, meta)
    return m['K']
