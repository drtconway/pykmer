from pykmer.codec8 import encode, decode
from pykmer.exceptions import BadCookie, BadMetaData, MetaDataIncompatible, MetaDataMissing

import sys

cookie = "TCF"

class FileBytes:
    def __init__(self, f):
        self.f = f

    def next(self):
        b = self.f.read(1)
        if len(b) != 1:
            raise StopIteration
        return ord(b[0])

def getBytes(n, itr):
    xs = []
    for i in range(n):
        xs.append(itr.next())
    return xs

def check_cookie(itr):
    c = getBytes(len(cookie), itr)
    c = ''.join(map(chr, c))
    if c != cookie:
        raise BadCookie()

def check_meta(t, m):
    for (k,v) in t.items():
        if k not in m:
            raise MetaDataMissing(k)
        if v is not None and m[k] != v:
            raise MetaDataIncompatible(k, v, m[k])

def getMeta(itr):
    t = chr(itr.next())
    if t == 'Z':
        return decode(itr)
    if t == 'S':
        l = decode(itr)
        xs = getBytes(l, itr)
        return ''.join(map(chr, xs))
    if t == 'T':
        n = decode(itr)
        xs = []
        for i in range(n):
            xs.append(getMeta(itr))
        return tuple(xs)
    if t == 'D':
        n = decode(itr)
        d = {}
        for i in range(n):
            k = getMeta(itr)
            v = getMeta(itr)
            d[k] = v
        return d

def putMeta(f, itm):
    if type(itm) == type(int(1)) or type(itm) == type(long(1)):
        f.write('Z')
        bs = bytearray(encode(itm))
        f.write(bs)
    elif type(itm) == type(''):
        f.write('S')
        bs = bytearray(encode(len(itm)))
        f.write(bs)
        f.write(itm)
    elif type(itm) == type(tuple([])):
        f.write('T')
        bs = bytearray(encode(len(itm)))
        f.write(bs)
        for i in range(len(tim)):
            putMeta(f, itm[i])
    elif type(itm) == type({}):
        f.write('D')
        bs = bytearray(encode(len(itm)))
        f.write(bs)
        for (k,v) in itm.items():
            putMeta(f, k)
            putMeta(f, v)
    else:
        raise BadMetaData(itm)

def probe(fn, t = None):
    f = open(fn, 'rb')
    itr = FileBytes(f)
    check_cookie(itr)
    m = getMeta(itr)
    if t is not None:
        check_meta(t, m)
    return (m, itr)

def make(fn, meta):
    f = open(fn, 'wb')
    f.write(cookie)
    putMeta(f, meta)
    return f
