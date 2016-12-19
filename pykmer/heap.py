"""
This module provides a heap/priority-queue data structure.
"""

__docformat__ = 'restructuredtext'

class heap:
    def __init__(self, xs = []):
        """
        Create an empty heap. If given, `xs` should be a list of items
        to become the body of the heap, to be reordered according to
        the heap invariant.
        """
        self.xs = xs
        self.heapify()

    def __len__(self):
        """
        Return the length of (number of items in) the heap.
        """
        return len(self.xs)

    def heapify():
        """
        Modify the data structure to impose the heap invariant.

        This will typically be invoked after a series of calls to
        `append`.
        """
        z = len(self.xs) + 1
        for i in xrange(1, z):
            self.upheap(i)

    def append(self, x):
        """
        Append the item `x` to the heap.

        This may violate the heap invariant, so after one or more calls to
        `append`, the method `heapify` should be invoked before calls to
        `push`, `pop`, or `modify`, to re-establish the heap invariant.
        """
        self.xs.append(x)

    def push(self, x):
        """
        Add the item `x` to the heap, and tweak the heap to re-establish
        the heap invariant.
        """
        self.xs.append(x)
        self.upheap(len(self))

    def pop(self):
        """
        Pop the smallest item off the heap, and rearrange the heap to
        re-establish the heap invariant.

        It is a fatal error to invoke `pop` on an empty heap.
        """
        assert len(self.xs) > 0
        x = self.xs[0]
        y = self.xs.pop()
        if len(self.xs) > 0:
            self.modify(y)
        return x

    def front(self):
        """
        Return the smallest item on the heap without removing it.
        If the object is mutable, and the caller modifies it, it is
        encumbant on the caller to also call `modifyfront` or `pop`
        to ensure that the heap invariant is re-established.

        It is an error to invoke this method on an empty heap.
        """
        assert len(self.xs) > 0
        return self.xs[0]

    def modifyfront(self, x = None):
        """
        Update the heap after changing the smallest item. If the parameter
        `x` is supplied and is not None, the smallest item in the heap
        is replaced with `x`, and in either case, the heap invariant
        is re-established.

        It is an error to invoke this method on an empty heap.
        """
        assert len(self.xs) > 0
        self.xs[0] = x
        self.downheap(1)

    def upheap(self, i):
        "upheap is for internal use only."
        p = i // 2
        while p >= 1:
            if self.xs[i - 1] < self.xs[p - 1]:
                t = self.xs[i - 1]
                self.xs[i - 1] = self.xs[p - 1]
                self.xs[p - 1] = t
                i = p
                p = i // 2
            else:
                break

    def downheap(self, p):
        "downheap is for internal use only."
        z = len(self.xs)
        c = 2*p
        while c <= z:
            if c < z and self.xs[c] < self.xs[c - 1]:
                c += 1
            if self.xs[c - 1] < self.xs[p - 1]:
                t = self.xs[c - 1]
                self.xs[c - 1] = self.xs[p - 1]
                self.xs[p - 1] = t
                p = c
                c = 2*p
            else:
                break
