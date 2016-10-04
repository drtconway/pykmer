
class BadCookie(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'bad cookie'

class BadMetaData(Exception):
    def __init__(self, itm):
        self.itm = itm

    def __str__(self):
        return 'bad metadata: %s' % (repr(self.itm))

class MetaDataMissing(Exception):
    def __init__(self, nm):
        self.nm = nm

    def __str__(self):
        return 'missing metadata: %s' % (repr(self.nm))

class MetaDataIncompatible(Exception):
    def __init__(self, nm, v0, v1):
        self.nm = nm
        self.v0 = v0
        self.v1 = v1

    def __str__(self):
        return 'incompatible metadata: %s - %s / %s' % (self.nm, self.v0, self.v1)

class MismatchedK(Exception):
    def __init__(self, k1, k2):
        self.k1 = k1
        self.k2 = k2

    def __str__(self):
        return 'incompatible values of K: %d & %d' % (self.k1, self.k2)

