"""
This module provides a simple rank/select interface to a sorted list/array
of integers.

See https://en.wikipedia.org/wiki/Succinct_data_structure for more
general information about the API.
"""

__docformat__ = 'restructuredtext'

import array

class sparse:
    """
    The sparse class is for presenting a sparse set of integers through
    a rank/select interface.
    """

    def __init__(self, B, xs):
        """
        Create a new sparse set object.

        The parameter `B` is the width of the elements in bits. It is
        an error to attempt to include elements >= 2**B.

        The parameter `xs` gives the elements of the set. These must be
        in sorted order, and the type of `xs` must be a list/array or some
        other object which supports ordinal access in the same manner.
        """
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
        """
        Return the number of possible elements in the set.  That is,
        the size of the domain.
        """
        return 1 << self.B

    def count(self):
        """
        Return the number of elements in the set.
        """
        return len(self.xs)

    def rank(self, x):
        """
        The `rank` method returns, given `x`, the rank of `x` in the set,
        which is the number of elements in the set which are strictly
        less than `x`.

        It is an error for `x` to be outside the interval [0, 2**B).
        """
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
        """
        Perform `rank` operations on x0 and x1. Equivalent to
            return(rank(x0), rank(x1)),
        but assumes that x1 has a nearby rank.

        It is an error if x1 <= x0.
        """
        assert x0 <= x1
        r0 = self.rank(x0)
        r1 = len(self.xs)
        for r1 in xrange(r0, len(self.xs)):
            if self.xs[r1] >= x1:
                break
        return (r0, r1)


    def select(self, i):
        """
        The `select` method returns, given `i`, the ith smallest item
        in the set.

        Given the set s, is an error for `i` to be outside the interval
        [0, s.count()).
        """
        assert 0 <= i
        assert i < self.count()
        return self.xs[i]
