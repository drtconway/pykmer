from pykmer.bits import ffs, rev, popcnt, m1

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
    for i in xrange(k):
        r.append("ACGT"[x&3])
        x >>= 2
    return ''.join(r[::-1])

fas = [
    '*', # 0000
    'A', # 0001
    'C', # 0010
    'M', # 0011
    'G', # 0100
    'R', # 0101
    'S', # 0110
    'V', # 0111
    'T', # 1000
    'W', # 1001
    'Y', # 1010
    'H', # 1011
    'K', # 1100
    'D', # 1101
    'B', # 1110
    'N'  # 1111
]

def fasta(ind):
    """Convert a 4-bit indicator variable representation
     of a base combination to the 16-letter FASTA alphabet"""
    return fas[ind]

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

def fnv(x, s):
    "Compute a FNV hash of a k-mer, returning least significant 61 bits"
    h = s + 0xcbf29ce484222325
    for i in xrange(8):
        h ^= (x & 0xff)
        h *= 0x100000001b3
        x >>= 8
    return h & 0x1FFFFFFFFFFFFFFF

def can(k, x):
    "Return the canonical form of x"
    xh = fnv(x, 17)
    xb = rc(k, x)
    xbh = fnv(xb, 17)
    if xh <= xbh:
        return x
    else:
        return xb

def kmers(k, seq, bothStrands=False):
    "Extract k-mers from a string sequence"
    z = len(seq)
    msk = (1 << (2*k)) - 1
    i = 0
    j = 0
    x = 0
    while i + k <= z:
        while i + j < z and j < k:
            b = nuc.get(seq[i+j], 4)
            if b == 4:
                i += j + 1
                j = 0
                x = 0
            else:
                x = (x << 2) | b
                j += 1
        if j == k:
            x &= msk
            yield x
            if bothStrands:
                yield rc(k, x)
            j -= 1
        i += 1

def kmersWithPos(k, seq, bothStrands=False):
    "Extract k-mers and positions (1-based, negative denoting rc-strand) from a string sequence"
    z = len(seq)
    msk = (1 << (2*k)) - 1
    i = 0
    j = 0
    x = 0
    while i + k <= z:
        while i + j < z and j < k:
            b = nuc.get(seq[i+j], 4)
            if b == 4:
                i += j + 1
                j = 0
                x = 0
            else:
                x = (x << 2) | b
                j += 1
        if j == k:
            x &= msk
            yield (x, i+1)
            if bothStrands:
                yield (rc(k, x), -(i+1))
            j -= 1
        i += 1

