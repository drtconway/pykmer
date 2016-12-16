import array

class sparse:
    def __init__(self, B, xs):
        self.B = B
        self.S = B - 10
        self.xs = xs
        self.toc = array.array('I', [0 for i in xrange(1024+1)])
        for x in xs:
            v = x >> self.S
            self.toc[v+1] += 1
        t = 0
        for i in xrange(1024+1):
            t += self.toc[i]
            self.toc[i] = t

    def size(self):
        return 1 << self.B

    def count(self):
        return len(self.xs)

    def rank(self, x):
        v = x >> self.S
        l = self.toc[v]
        h = self.toc[v+1] - 1
        while h >= l:
            m = (h + l) // 2
            y = self.xs[m]
            if y == x:
                return m
            if y < x:
                l = m + 1
            else:
                h = m - 1
        return l

    def rank2(self, x0, x1):
        r0 = self.rank(x0)
        r1 = len(self.xs)
        for r1 in xrange(r0, len(self.xs)):
            if self.xs[r1] >= x1:
                break
        return (r0, r1)


    def select(self, i):
        assert 0 <= i
        assert i < self.count()
        return self.xs[i]
