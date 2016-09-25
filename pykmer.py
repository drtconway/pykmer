
def readFasta(file):
    "Read a FASTA file, and generate (name, sequence) tuples"
    nm = None
    seq = []
    for l in file:
        l = l.strip()
        if len(l) and l[0] == '>':
            if nm is not None:
                yield (nm, ''.join(seq))
            nm = l[1:].strip()
            seq = []
        else:
            seq.append(l)
    if nm is not None:
        yield (nm, ''.join(seq))

def readFastq(file):
    "Read a FASTQ file, and generate (id, sequence, id2, quality) tuples"
    grp = []
    for l in file:
        l = l.strip()
        grp.append(l)
        if len(grp) == 4:
            yield tuple(grp)
            grp = []
    if grp == 4:
        yield tuple(grp)

nuc = { 'A':0, 'a':0, 'C':1, 'c':1, 'G':2, 'g':2, 'T':3, 't':3 }

def make_kmer(seq):
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
    y = 0
    x = ~x
    for i in range(k):
        y = (y << 2) | (x & 3)
        x >>= 2
    return y

def popcount(x):
    "Population counting the slow way"
    c = 0
    while x > 0:
        c += (x & 1)
        x >>= 1
    return c

pops = bytearray([popcount(i) for i in range(65536)])

def popcnt(x):
    "Faster population counting"
    c = 0
    while x > 0:
        c += pops[x & 65535]
        x >>= 16
    return c

def ham(x, y):
    "Compute the hamming distance between two k-mers."
    z = x ^ y
    # NB: if k > 32, the constant below will need extending.
    v = (z | (z >> 1)) & 0x5555555555555555
    return popcnt(v)

def ffs(x):
    "Find the position of the most significant bit"
    l = 0
    h = 63
    while l < h:
        m = (l + h) // 2
        y = (x >> m)
        if y > 0:
            l = m + 1
        else:
            h = m
    return l

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
        x = make_kmer(str[i:i+k])
        if x:
            yield x
            if bothStrands:
                yield rc(k, x)

