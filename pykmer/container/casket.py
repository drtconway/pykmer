"""
The casket module provides an alternative container format to zipfile.
The motivation for an alternative container format is twofold:

* It is not possible to stream data in to a zip file in the API.
The work-around we have of creating a temporary file and copying
it in works, but is quite slow.

* When reading from a zip file, the data is copied out and the
file object refers to that copy.

The casket module addresses these with a similar container format,
but with an API that addresses these issues. There is no compression
built in to the container API - this is pushed to the client.

The format of a casket is that it has data, followed by a table of
contents (TOC).  The TOC is a dictionary mapping in-container file
name to a list of <offset, length> pairs which refer to the absolute
position and length of copies of that file. This is stored in the
casket as a JSON string followed by a 64-bit integer (Intel byte
order) containing the length of the JSON string.

The casket objects act as context managers.

Files in the casket may be opened for reading with the `open()`
method which creates a wrapper object supporting `read()` which
will read the appropriate region directly from the casket.

There are several ways to add files to a casket:

* An existing file on disk may be added with the `add_file()` method.
* A new file with string content may be added with the `add_content()`
method.
* A new file may be streamed in with the `add_stream()` method.

The `add_stream()` method returns a file-like object supporting
`write()` in to which the content of the file may be written. The
file object acts as a context manager. If a stream is open, then
no other file may be written until it is closed.
"""

import json
import os
import struct

class MultipleOpenFiles(Exception):
    def __init__(self):
        super(MultipleOpenFiles, elf).__init__('cannot add to archive while streaming object open')

_block_size_ = 1024*1024 # 1MB

class CasketReader(object):
    def __init__(self, fo, p, l):
        self.fo = fo
        self.p = p
        self.l = l
        self.o = 0

    def read(self, z = None):
        """
        Read content from a casket object. The parameter `z` is the
        number of bytes to read. If `z` is None, then the rest of
        the file is read.
        """
        if z is None:
            z = self.l - self.o
        z = min(z, self.l - self.o)

        if z == 0:
            return ''

        self.fo.seek(self.p + self.o, os.SEEK_SET)
        w = self.fo.read(z)
        assert len(w) == z
        self.o += z

        return w

class CasketStreamWriter(object):
    def __init__(self, ar, afn):
        self.ar = ar
        self.afn = afn
        self.ar.fo.seek(0, os.SEEK_END)
        self.p = self.ar.fo.tell()
        self.l = 0
        self.closed = False

    def write(self, dat):
        """
        Write content in to a casket file.
        """
        self.l += len(dat)
        self.ar.fo.write(dat)

    def close(self):
        """
        Close a stream writing in to a casket.
        """
        assert not self.closed
        self.ar.updateToc(self.afn, self.p, self.l)
        self.ar.fip = None

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        if not self.closed:
            self.close()
        return True

class casket(object):
    def __init__(self, fn, mode='r'):
        self.fn = fn
        self.mode = mode
        if mode == 'r':
            self.fo = open(fn, mode)
            self.toc = {}
            self._readToc()
            self.stale = False
            self.fip = None
        elif mode == 'w':
            self.fo = open(fn, mode)
            self.toc = {}
            self.stale = True
            self.fip = None
        print fn, self.toc

    def list(self):
        """
        Return a list of the files in a casket.  If there are
        multiple versions, only the most recent one is returned.
        """
        xs = self.toc.items()
        xs.sort()
        r = []
        for (nm, ys) in xs:
            r.append((nm, ys[-1][1]))
        return r

    def add_file(self, afn, fn):
        assert self.mode == 'w'

        if self.fip is not None:
            raise MultipleOpenFiles

        self.fo.seek(0, os.SEEK_END)
        p = self.fo.tell()

        with open(fn, 'r') as f:
            l = 0
            w = f.read(_block_size_)
            while len(w) > 0:
                l += len(w)
                self.fo.write(w)
                w = f.read(_block_size_)

        self.updateToc(afn, p, l)

    def add_content(self, afn, data):
        assert self.mode == 'w'

        if self.fip is not None:
            raise MultipleOpenFiles

        self.fo.seek(0, os.SEEK_END)
        p = self.fo.tell()
        l = len(data)
        self.fo.write(data)

        self.updateToc(afn, p, l)

    def add_stream(self, afn):
        assert self.mode == 'w'

        if self.fip is not None:
            raise MultipleOpenFiles

        self.fip = CasketStreamWriter(self, afn)
        return self.fip

    def open(self, afn):
        assert self.mode == 'r'

        (p, l) = self.toc[afn][-1]

        return CasketReader(self.fo, p, l)

    def updateToc(self, afn, p, l):
        if afn not in self.toc:
            self.toc[afn] = []
        self.toc[afn].append((p, l))
        self.stale = True

    def flush(self):
        pass

    def close(self):
        if not self.stale:
            self.fo.close()
            self.fo = None
            return
        
        self.flush()
        self._writeToc()
        self.fo.close()
        self.fo = None
        self.stale = False

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        self.close()
        return True

    def _readToc(self):
        self.fo.seek(-8, os.SEEK_END)
        w = self.fo.read(8)
        z = struct.unpack('Q', w)[0]
        self.fo.seek(-(8+z), os.SEEK_END)
        w = self.fo.read(z)
        self.toc = json.loads(w)

    def _writeToc(self):
        w = json.dumps(self.toc)
        z = len(w)
        self.fo.seek(0, os.SEEK_END)
        self.fo.write(w)
        w = struct.pack('Q', z)
        self.fo.write(w)
        self.fo.flush()
