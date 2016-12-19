"""
This module provides a collection of low level bit manipulation functions.
Some, such as `popcnt` and `ffs` can actually be evaluated with single
machine instructions, but unfortunately these are not exposed at the
Python language level. However, the implementations below have been
tuned somewhat and with pypy run pretty fast.

Most of the functions are adaptions of those at
https://graphics.stanford.edu/~seander/bithacks.html
"""

__docformat__ = 'restructuredtext'

# Some useful constants
m1 = 0x5555555555555555 # 01010101...
m2 = 0x3333333333333333 # 00110011...
m3 = 0x0F0F0F0F0F0F0F0F # 00001111...
m4 = 0x00FF00FF00FF00FF # {0^8}{1^8}...
m5 = 0x0000FFFF0000FFFF # {0^16}{1^16}...
m6 = 0x00000000FFFFFFFF # {0^32}{1^32}

def rev(x):
    """
    Reverse the bit-pairs in the 64-bit integer `x`.
    """
    x = ((x >> 2) & m2) | ((x & m2) << 2)
    x = ((x >> 4) & m3) | ((x & m3) << 4)
    x = ((x >> 8) & m4) | ((x & m4) << 8)
    x = ((x >> 16) & m5) | ((x & m5) << 16)
    x = ((x >> 32) & m6) | ((x & m6) << 32)
    return x

def popcnt(x):
    """
    Compute the number of set bits (i.e 1s) in the 64-bit integer `x`.
    """
    x = (x & m1) + ((x >> 1) & m1)
    x = (x & m2) + ((x >> 2) & m2)
    x = (x & m3) + ((x >> 4) & m3)
    x = (x & m4) + ((x >> 8) & m4)
    x = (x & m5) + ((x >> 16) & m5)
    x = (x & m6) + ((x >> 32) & m6)
    return x & 0x7F

def ffs0(x):
    r = (x > 0xFFFFFFFF) << 5
    x >>= r
    s = (x > 0xFFFF) << 4
    x >>= s
    r |= s
    s = (x > 0xFF) << 3
    x >>= s
    r |= s
    s = (x > 0xF) << 2
    x >>= s
    r |= s
    s = (x > 0x3) << 1
    x >>= s
    r |= s
    r |= (x >> 1)
    return r

ffsBits = [ffs0(i) for i in xrange(256)]

def ffs(x):
    """
    Find the position of the most significant set bit (i.e. 1)
    in the 64-bit integer `x`.
    """
    x32 = x >> 32
    if x32 > 0:
        x48 = x >> 48
        if x48 > 0:
            x56 = x >> 56
            if x56 > 0:
                return ffsBits[x56] + 56
            else:
                return ffsBits[x48] + 48
        else:
            x40 = x >> 40
            if x40 > 0:
                return ffsBits[x40] + 40
            else:
                return ffsBits[x32] + 32
    else:
        x16 = x >> 16
        if x16 > 0:
            x20 = x >> 20
            if x20 > 0:
                return ffsBits[x20] + 20
            else:
                return ffsBits[x16] + 16
        else:
            x8 = x >> 8
            if x8 > 0:
                return ffsBits[x8] + 8
            else:
                return ffsBits[x]
