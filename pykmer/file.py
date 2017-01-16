"""
This module provides simple parsers for the FASTA and FASTQ sequence
data formats.

The FASTQ parser is not strictly conformant since it assumes the input
to be in a line oriented form (which is usually true).
"""

__docformat__ = 'restructuredtext'

import subprocess

def readFasta(file):
    """
    Read textual input from the file object `file`, which is assumed to
    be in FASTA format.  Yields the sequence of (name, sequence) tuples.
    """
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
    """
    Read textual input from the file object `file`, which is assumed
    to be in line-oriented FASTQ format (not full multi-line FASTQ).
    Yields the sequence of (name, sequence, label, quality) tuples.
    """
    grp = []
    for l in file:
        l = l.strip()
        grp.append(l)
        if len(grp) == 4:
            yield tuple(grp)
            grp = []
    if grp == 4:
        yield tuple(grp)

def openFile(fn):
    if fn == "-":
        return sys.stdin
    if fn.endswith(".gz"):
        p = subprocess.Popen(['gunzip', '-c', fn], stdout=subprocess.PIPE)
        return p.stdout
    if fn.endswith(".bz2"):
        p = subprocess.Popen(['bunzip2', '-c', fn], stdout=subprocess.PIPE)
        return p.stdout
    return open(fn, 'rb')

