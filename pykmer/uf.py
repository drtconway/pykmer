"""
This module provides an implementation of the disjoint-set data structure
(also called the union-find data structure).

For general information on this data structure see
https://en.wikipedia.org/wiki/Disjoint-set_data_structure
"""

__docformat__ = 'restructuredtext'

class uf:
    """
    This class implements the disjoint-set/union-find data structure.

    Unlike some implementations, it does not need initialization with
    the full domain of labels in advance. The labels may be any type
    that can be used as a key to a standard Python dictionary.
    """
    def __init__(self):
        """
        Create a new disjoint-set data structure.
        """
        self.parent = {}
        self.rank = {}

    def find(self, x):
        """
        Return the label of the partition to which `x` belongs.

        If `x` has not previously been added as a label to the
        disjoint-set, it is added and becomes a singleton partition.
        """
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            return x
        xp = self.parent[x]
        if xp != x:
            self.parent[x] = self.find(xp)
        return self.parent[x]

    def union(self, x, y):
        """
        Merge two partitions in the disjoint-set data structure.
        The two partitions are which ever partition `x` and `y` belong
        to, respectively.

        If `x` and `y` are already in the same partition, this operation
        has no effect.
        """
        xr = self.find(x)
        yr = self.find(y)

        if xr == yr:
            return

        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1

