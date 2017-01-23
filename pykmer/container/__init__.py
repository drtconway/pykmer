"""
A container format for storing k-mers, counts and associated information.

The container format of the container is a ZIP file. A container always
containts at least the two following files:
`__meta__`
    which is a pickle format dictionary of meta-data. The user level
    container object represents this at runtime as the member
    variable `meta`.

The container may also contain additional files corresponding to
data objects that belong together. In practice this typically means
files containing k-mers, counts, and other related items.

The principle functionality offered by the container class over a
straight ZIP file or tar file is the ability to transparently stream
data in to the container. This is done with an additional object
which creates a temporary file, and on closing moves it in to the
container.

"""

__docformat__ = 'restructuredtext'

from pykmer.file import tmpfile

import cPickle
import os
import types
import warnings
import zipfile

class SelfZippingFile:
    def __init__(self, z, zfn, comp):
        self.z = z
        self.zfn = zfn
        self.comp = comp
        self.tfn = tmpfile('.szf')
        self.tf = open(self.tfn, 'w')

    def __enter__(self):
        return self.tf

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        self.close()
        return True

    def close(self):
        self.tf.close()
        comp = zipfile.ZIP_STORED
        if self.comp:
            comp = zipfile.ZIP_DEFLATED
        self.z.write(self.tfn, self.zfn, comp)
        os.remove(self.tfn)

    def write(self, x):
        self.tf.write(x)

class container:
    def __init__(self, nm, mode):
        self.nm = nm
        self.mode = mode
        self.z = None
        self.meta = None

        if self.mode == 'r':
            self.z = zipfile.ZipFile(self.nm, self.mode, allowZip64=True)
            self.meta = cPickle.load(self.z.open('__meta__'))
        elif self.mode == 'a':
            with zipfile.ZipFile(self.nm, 'r') as z:
                self.meta = cPickle.load(z.open('__meta__'))
            self.z = zipfile.ZipFile(self.nm, self.mode, allowZip64=True)
        else:
            self.z = zipfile.ZipFile(self.nm, self.mode, allowZip64=True)
            self.meta = {}

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        if self.z is not None:
            self.close()
        return t is not None

    def creat(self, fn, comp = False):
        assert self.z is not None
        return SelfZippingFile(self.z, fn, comp)

    def add(self, fn, bytes):
        assert self.z is not None
        self.z.writestr(fn, bytes)

    def open(self, fn):
        return self.z.open(fn)

    def close(self):
        assert self.z is not None
        if (self.mode == 'w' or self.mode == 'a'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.z.writestr('__meta__', cPickle.dumps(self.meta))
        self.z.close()
