import cPickle
import os
import types
import zipfile

class SelfZippingFile:
    def __init__(self, z, zfn, comp):
        self.z = z
        self.zfn = zfn
        self.comp = comp
        self.tfn = None
        self.tf = None

    def __enter__(self):
        self.tfn = os.tmpnam()
        self.tf = open(self.tfn, 'w')
        return self.tf

    def __exit__(self, t, v, tb):
        if t is not None:
            return False

        self.tf.close()
        comp = zipfile.ZIP_STORED
        if self.comp:
            comp = zipfile.ZIP_DEFLATED
        self.z.write(self.tfn, self.zfn, comp)

        return True

class container:
    def __init__(self, nm, mode):
        self.nm = nm
        self.mode = mode
        self.z = None
        self.meta = None

    def __enter__(self):
        if self.mode == 'r':
            self.z = zipfile.ZipFile(self.nm, self.mode)
            self.meta = cPickle.load(self.z.open('__meta__'))
            self.manifest = cPickle.load(self.z.open('__manifest__'))
        elif self.mode == 'a':
            with zipfile.ZipFile(self.nm, 'r') as z:
                self.meta = cPickle.load(z.open('__meta__'))
                self.manifest = cPickle.load(z.open('__manifest__'))
            self.z = zipfile.ZipFile(self.nm, self.mode)
        else:
            self.z = zipfile.ZipFile(self.nm, self.mode)
            self.meta = {}
            self.meta['version'] = '20170109a'
            self.manifest = {}
        return self

    def __exit__(self, t, v, tb):
        if t is not None:
            return False
        if self.z is not None:
            if self.mode == 'w' and t is None:
                self.z.writestr('__meta__', cPickle.dumps(self.meta))
                self.z.writestr('__manifest__', cPickle.dumps(self.manifest))
            self.z.close()
        return t is not None

    def creat(self, fn, comp = False):
        assert self.z is not None
        assert fn not in self.manifest
        self.manifest[fn] = {}
        return SelfZippingFile(self.z, fn, comp)

    def add(self, fn, bytes):
        assert self.z is not None
        assert fn not in self.manifest
        self.manifest[fn] = {}
        self.z.writestr(fn, bytes)

    def open(self, fn):
        return self.z.open(fn)

    def find(self,  **qry):
        cand = self.manifest.keys()
        for (var, val) in qry.iteritems():
            next = []
            for c in cand:
                if var not in self.manifest[c]:
                    continue
                if type(val) is list or type(val) is tuple:
                    found = False
                    for v in val:
                        if self.manifest[c][var] == v:
                            found = True
                            break
                    if not found:
                        continue
                else:
                    if self.manifest[c][var] != val:
                        continue
                next.append(c)
            cand = next
        return cand

