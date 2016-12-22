"""
This module provides some adaptors for converting between
different data formats:

`k2kf`
    Convert a sequence of k-mers to k-mer frequency pairs

`kf2k`
    Convert a sequence of k-mer frequency pairs to k-mers


`keyedKs`
    Provide keyed access to a sequence of k-mers

`keyedKFs`
    Provide keyed access to a sequence of k-mer frequency pairs
"""

def k2kf(xs, f=1):
    for x in xs:
        yield (x, f)

def kf2k(xs):
    for (x, _) in xs:
        yield x

class keyedKs:
    def __init__(self, itr):
        self.itr = itr
        self.more = True
        self.next()

    def valid(self):
        return self.more

    def kmer(self):
        assert self.valid()
        return self.curr

    def item(self):
        assert self.valid()
        return self.curr

    def next(self):
        assert self.valid()
        try:
            self.curr = self.itr.next()
        except StopIteration:
            self.more = False

class keyedKfs:
    def __init__(self, itr):
        self.itr = itr
        self.more = True
        self.next()

    def valid(self):
        return self.more

    def kmer(self):
        assert self.valid()
        return self.curr[0]

    def item(self):
        assert self.valid()
        return self.curr

    def next(self):
        assert self.valid()
        try:
            self.curr = self.itr.next()
        except StopIteration:
            self.more = False

