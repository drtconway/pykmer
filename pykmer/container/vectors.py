"""
This module provides functions for reading and writing sorted sequences
of *k*-mers in a compressed representation.
"""

__docformat__ = 'restructuredtext'

import array

def write64(z, xs, nm):
    """
    """
    N = 65536
    n = 0
    with z.creat(nm, True) as f:
        a = array.array('L', [])
        i = 0
        for x in xs:
            a.append(x)
            n += 1
            i += 1
            if i == N:
                a.tofile(f)
                a = array.array('L', [])
                i = 0
        a.tofile(f)
    return n

def write32(z, xs, nm):
    """
    """
    N = 65536
    n = 0
    with z.creat(nm, True) as f:
        a = array.array('I', [])
        i = 0
        for x in xs:
            a.append(x)
            n += 1
            i += 1
            if i == N:
                a.tofile(f)
                a = array.array('I', [])
                i = 0
        a.tofile(f)
    return n

def write16(z, xs, nm):
    """
    """
    N = 65536
    n = 0
    with z.creat(nm, True) as f:
        a = array.array('H', [])
        i = 0
        for x in xs:
            a.append(x)
            n += 1
            i += 1
            if i == N:
                a.tofile(f)
                a = array.array('H', [])
                i = 0
        a.tofile(f)
    return n

def read64(z, nm, n):
    """
    """
    N = 65536
    with z.open(nm) as f:
        while n > N:
            a = array.array('L', [])
            a.fromfile(f, N)
            i = 0
            while i < N:
                yield a[i]
            n -= N

        if n > 0:
            a = array.array('L', [])
            a.fromfile(f, n)
            i = 0
            while i < n:
                yield a[i]

def read32(z, nm, n):
    """
    """
    N = 65536
    with z.open(nm) as f:
        while n >= N:
            a = array.array('I', [])
            a.fromfile(f, N)
            i = 0
            while i < N:
                yield a[i]
            n -= N

        if n > 0:
            a = array.array('I', [])
            a.fromfile(f, n)
            i = 0
            while i < n:
                yield a[i]

def read16(z, nm, n):
    """
    """
    N = 65536
    with z.open(nm) as f:
        while n >= N:
            a = array.array('H', [])
            a.fromfile(f, N)
            i = 0
            while i < N:
                yield a[i]
            n -= N

        if n > 0:
            a = array.array('H', [])
            a.fromfile(f, n)
            i = 0
            while i < n:
                yield a[i]
