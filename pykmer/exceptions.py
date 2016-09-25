
class MismatchedK(Exception):
    def __init__(self, k1, k2):
        self.k1 = k1
        self.k2 = k2

    def __str__(self):
        return 'incompatible values of K: %d & %d' % (self.k1, self.k2)

