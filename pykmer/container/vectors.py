"""
This module provides functions for reading and writing sorted sequences
of *k*-mers in a compressed representation.
"""

__docformat__ = 'restructuredtext'

import array
import struct

blockSize = 65536

class GenericWriter:
    def __init__(self, z, nm, w):
        self.w = w
        self.f = z.creat(nm, True)
        self.a = array.array(self.w)
        self.n = 0
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        self.close()
        return True

    def close(self):
        if len(self.a) > 0:
            self.flush()
        self.f.close()
        self.closed = True

    def append(self, x):
        self.n += 1
        self.a.append(x)
        if len(self.a) == blockSize:
            self.flush()

    def flush(self):
        s = self.a.tostring()
        v = struct.pack('L', len(s))
        self.f.write(v)
        self.f.write(s)
        self.a = array.array(self.w, [])

    def __del__(self):
        assert self.closed == True

def writer64(z, nm):
    return GenericWriter(z, nm, 'L')

def writer32(z, nm):
    return GenericWriter(z, nm, 'I')

def writer16(z, nm):
    return GenericWriter(z, nm, 'H')

def writeGeneric(z, xs, nm, w):
    """
    """
    n = 0
    with z.creat(nm, True) as f:
        a = array.array(w, [])
        i = 0
        for x in xs:
            a.append(x)
            n += 1
            i += 1
            if i == blockSize:
                s = a.tostring()
                v = struct.pack('L', len(s))
                f.write(v)
                f.write(s)
                a = array.array(w, [])
                i = 0
        s = a.tostring()
        v = struct.pack('L', len(s))
        f.write(v)
        f.write(s)
    return n

def write64(z, xs, nm):
    return writeGeneric(z, xs, nm, 'L')

def write32(z, xs, nm):
    return writeGeneric(z, xs, nm, 'I')

def write32s(z, xs, nm):
    return writeGeneric(z, xs, nm, 'i')

def write16(z, xs, nm):
    return writeGeneric(z, xs, nm, 'H')

def readGeneric(z, nm, n, w):
    """
    """
    W = struct.calcsize('L')
    with z.open(nm) as f:
        while n > 0:
            v = f.read(W)
            if len(v) != W:
                break
            l = struct.unpack('L', v)[0]
            s = f.read(l)
            assert len(s) == l
            a = array.array(w, [])
            a.fromstring(s)
            m = len(a)
            i = 0
            while i < m:
                yield a[i]
                i += 1
            n -= m

def read64(z, nm, n):
    return readGeneric(z, nm, n, 'L')

def read32(z, nm, n):
    return readGeneric(z, nm, n, 'I')

def read32s(z, nm, n):
    return readGeneric(z, nm, n, 'i')

def read16(z, nm, n):
    return readGeneric(z, nm, n, 'H')

