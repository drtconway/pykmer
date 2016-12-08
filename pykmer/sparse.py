
class sparse:
    def __init__(self, z, xs):
        self.z = z
        self.xs = xs

    def size(self):
        return self.z

    def count(self):
        return len(self.xs)

    def rank(self, x):
        l = 0
        h = len(self.xs) - 1
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

    def select(self, i):
        assert 0 <= i
        assert i < self.count()
        return self.xs[i]
