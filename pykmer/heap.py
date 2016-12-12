
class heap:
    def __init__(self, xs = []):
        self.xs = xs

    def __len__(self):
        return len(self.xs)

    def push(self, x):
        self.xs.append(x)
        self.upheap(len(self))

    def pop(self):
        x = self.xs[0]
        y = self.xs.pop()
        if len(self.xs) > 0:
            self.modify(y)
        return x

    def front(self):
        return self.xs[0]

    def modify(self, x):
        self.xs[0] = x
        self.downheap(1)

    def upheap(self, i):
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

    def heapify():
        z = len(self.xs) + 1
        for i in xrange(1, z):
            self.upheap(i)

