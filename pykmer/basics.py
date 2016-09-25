from pykmer.bits import rev, popcnt, ffs

nuc = { 'A':0, 'a':0, 'C':1, 'c':1, 'G':2, 'g':2, 'T':3, 't':3 }

def kmer(seq):
    "Turn a string in to an integer k-mer"
    r = 0
    for c in seq:
        if c not in nuc:
            return None
        r = (r << 2) | nuc[c]
    return r

def render(k, x):
    "Turn an integer k-mer in to a string"
    r = []
    for i in range(k):
        r.append("ACGT"[x&3])
        x >>= 2
    return ''.join(r[::-1])

def rc(k, x):
    "Compute the reverse complement of a k-mer"
    return rev(~x) >> (64 - 2*k)

def ham(x, y):
    "Compute the hamming distance between two k-mers."
    z = x ^ y
    # NB: if k > 32, the constant below will need extending.
    v = (z | (z >> 1)) & m1
    return popcnt(v)


def lcp(k, x, y):
    "Find the length of the common prefix between 2 k-mers"
    z = x ^ y
    if z == 0:
        return k
    v = 1 + ffs(z) // 2
    return k - v

def kmers(k, str, bothStrands=False):
    "Extract k-mers from a string sequence"
    for i in range(len(str) - k + 1):
        x = kmer(str[i:i+k])
        if x:
            yield x
            if bothStrands:
                yield rc(k, x)

