"""
This module provides an API for reading and writing sets (sorted lists)
of *k*-mers in an uncompressed form using the builtin Python array type.

It is good for small sets of *k*-mers, where the compression/decompression
overhead outweighs the space benefits.
"""

__docformat__ = 'restructuredtext'

import array
import struct

def write(k, xs, nm):
    """
    Write the sorted array of *k*-mers `xs` to the file named `nm`.
    """
    with open(nm, 'wb') as f:
        s = struct.pack('QQ', k, len(xs))
        f.write(s)
        xs.tofile(f)

def read(nm):
    """
    Open the file `nm` and read from it a sorted array of *k*-mers,
    and return the metadata (i.e. K), and the array of *k*-mers.
    """
    with open(nm, 'rb') as f:
        s = f.read(16)
        (k, n) = struct.unpack('QQ', s)
        meta = {'K':k}
        a = array.array('L', [])
        a.fromfile(f, n)
        return (meta, a)
