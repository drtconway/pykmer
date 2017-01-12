import array

class bitvec:
    def __init__(self, n):
        self.size = n
        self.words = (n + 63) // 64
        self.data = array.array('L', [0 for i in xrange(self.words)])

    def __len__(self):
        return self.size

    def __getitem__(self, i):
        w = i // 64
        b = i & 63
        return (self.data[w] >> b) & 1

    def __setitem__(self, i, x):
        w = i // 64
        b = i & 63
        self.data[w] &= 0xFFFFFFFFFFFFFFFF - (1 << b)
        self.data[w] |= (x & 1) << b

