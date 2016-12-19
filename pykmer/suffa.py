
class SuffixArray:
    def __init__(self, seq):
        self.seq = seq
        self.suffs = [i for i in range(len(seq))]
        self.suffs.sort(self.cmp)

    def __len__(self):
        return len(self.suffs)

    def suff(self, a):
        i = self.suffs[a]
        return i

    def __getitem__(self, a):
        i = self.suffs[a]
        return self.seq[i:]

    def cmp(self, a, b):
        i = a
        j = b
        while i < len(self.seq) and j < len(self.seq):
            if self.seq[i] < self.seq[j]:
                return -1
            if self.seq[i] > self.seq[j]:
                return 1
            i += 1
            j += 1
        if i < len(self.seq):
            return -1
        else:
            return 1

    def cmp_str(self, s, b):
        i = 0
        j = b
        while i < len(s) and j < len(self.seq):
            if s[i] < self.seq[j]:
                return -1
            if s[i] > self.seq[j]:
                return 1
            i += 1
            j += 1
        if i < len(s):
            return -1
        elif j < len(self.seq):
            return 1
        else:
            return 0

    def lcp_suff(self, s, b):
        i = 0
        j = b
        while i < len(s) and j < len(self.seq):
            if s[i] != self.seq[j]:
                return i
            i += 1
            j += 1
        return i

    def lcp(self, s):
        l = 0
        h = len(self.suffs)
        while l < h:
            m = (l + h) // 2
            c = self.cmp_str(s, self.suffs[m])
            if c == 0:
                return len(s)
            if c < 0:
                h = m - 1
            else:
                l = m + 1
        if l == 0:
            return (self.lcp_suff(s, self.suffs[l]), self.suffs[l])
        if l == len(self.suffs):
            return (self.lcp_suff(s, self.suffs[l - 1]), self.suffs[l - 1])
        r1 = self.lcp_suff(s, self.suffs[l - 1])
        r2 = self.lcp_suff(s, self.suffs[l])
        if r1 >= r2:
            return (r1, self.suffs[l - 1])
        else:
            return (r1, self.suffs[l])

def make(seq):
    return SuffixArray(seq)
