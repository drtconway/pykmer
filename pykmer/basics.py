"""
Basic functions for *k*-mer manipulations.

The elementary functions `kmer` converts string representations of DNA
sequences (using ACG&T) in to a compact 2-bit/base integer representation,
and `render` converts this representation back to a string.

An additional encoding for single bases is used by the function `fasta`
where 4 indicator bits are used to represent a nucleotide in the extended
form where the least significant bit indicates the presence of an A, the
second least significant bit, a C, and so on, so that all 16 combinations
can be represented, and the function converts that representation in to
the standard FASTA form.

The functions `kmers` and `kmersWithPos` return the sequence of *k*-mers
from sliding a window over the given sequence, optionally including
reverse complement *k*-mers as well. The latter function also includes
position information. Positions are numbered from 1, not 0, and the
positions of *k*-mers from the reverse complement strand are given
negative positions (from -1).

The basic manipulation and comparison functions included in this module are:

`rc`
    for computing the reverse complement of a *k*-mer
`fnv`
    for computing the Fowler-Noll-Vo (FNV) hash of a *k*-mer
`can` 
    for computing the canonical choice between a *k*-mer and its reverse
    complement.
`ham`
    for computing the Hamming distance (number of substitutions) between
    two *k*-mers
`lcp`
    for computing longest common matchinng prefix betwen two *k*-mers
"""

__docformat__ = 'restructuredtext'

from pykmer.bits import ffs, rev, popcnt, m1

nuc = { 'A':0, 'a':0, 'C':1, 'c':1, 'G':2, 'g':2, 'T':3, 't':3, 'U':3, 'u':3 }

def kmer(seq):
    "Turn a string `seq` into an integer k-mer"
    r = 0
    for c in seq:
        if c not in nuc:
            return None
        r = (r << 2) | nuc[c]
    return r

def render(k, x):
    "Turn an integer k-mer `x` into a string"
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

def fasta(x):
    """Convert a 4-bit indicator variable `x` representation
     of a base combination to the 16-letter FASTA alphabet.
     
     The indicator bit representation is the bitwise OR of:

     ====   ==============
     Base   Representation
     ====   ==============
     A      1
     C      2
     G      4
     T/U    8
     """
    return fas[ind]

def rc(k, x):
    """
    Compute the reverse complement of a *k*-mer `x`.

    Values of `k` > 30 are not guaranteed to work.
    """
    return rev(~x) >> (64 - 2*k)

def ham(x, y):
    """
    Compute the Hamming distance between two k-mers `x` and `y`.

    Although *k* is not a parameter, *k*-mers longer than 30bp are not
    guaranteed to produce correct results.
    """
    z = x ^ y
    # NB: if k > 32, the constant below will need extending.
    v = (z | (z >> 1)) & m1
    return popcnt(v)


def lcp(k, x, y):
    """
    Find the length of the common matching prefix between 2 k-mers `x` and `y`.

    Values of `k` > 30 are not guaranteed to work.
    """
    z = x ^ y
    if z == 0:
        return k
    v = 1 + ffs(z) // 2
    return k - v

def fnv(x, s):
    """
    Compute a Fowler-Noll-Vo (FNV) hash of a *k*-mer `x` with the seed
    `s`, returning least significant 61 bits.

    We recommend this for hashing *k*-mers over Python's builtin `hash`
    function, for most uses. Python's builtin hash function returns the
    value of the integer as its hash, which for many *k*-mer methods is
    undesirable.

    Although *k* is not a parameter, *k*-mers longer than 30bp are not
    guaranteed to produce correct results.
    """
    h = s + 0xcbf29ce484222325
    for i in xrange(8):
        h ^= (x & 0xff)
        h *= 0x100000001b3
        x >>= 8
    return h & 0x1FFFFFFFFFFFFFFF

def can(k, x):
    """
    Return a canonical choice between `x` and its reverse complement.

    Some implementations just choose the lexicographically less of the
    two. For reasons of robustness, this method returns the *k*-mer with
    the smaller FNV (see `fnv`) hash. This results in an approximately
    uniform distribution of canonical *k*-mers, rather than the highly
    skewed distribution that results from a lexicographically determined
    choice.

    Values of `k` > 30 are not guaranteed to work.
    """
    xh = fnv(x, 17)
    xb = rc(k, x)
    xbh = fnv(xb, 17)
    if xh <= xbh:
        return x
    else:
        return xb

def kmers(k, seq, bothStrands=False):
    """
    Extract *k*-mers from a string nucleotide sequence `seq`.
    The parameter `bothStrands` determines whether the sequence of
    result *k*-mers should include the reverse complement of each *k*-mer
    extracted from the string.

    The *k*-mers are extracted using a *sliding* window, not a *tiling*
    window.  This means that the results include the *k*-mer starting
    at each position in the string: 0, 1, 2, ...., len(str) - k + 1.

    Any *k*-mers overlaying characters *other* than AaCcGgTtUu are skipped.

    Values of `k` > 30 are not guaranteed to work.
    """
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
    """
    Extract *k*-mers from a string nucleotide sequence `seq`.
    The parameter `bothStrands` determines whether the sequence of
    result *k*-mers should include the reverse complement of each *k*-mer
    extracted from the string.

    The *k*-mers are returned in a tuple with the position in the sequence
    of the left-most base (i.e. most significant bits). Positions on
    the forward strand are numbered from 1. Positions on the reverse
    complement strand are numbered from -1.

    The *k*-mers are extracted using a *sliding* window, not a *tiling*
    window.  This means that the results include the *k*-mer starting
    at each position in the string: 0, 1, 2, ...., len(str) - k + 1.

    Any *k*-mers overlaying characters *other* than AaCcGgTtUu are skipped.

    Values of `k` > 30 are not guaranteed to work.
    """
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

