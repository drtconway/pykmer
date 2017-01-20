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

def openFile(fn, mode='r'):
    """
    Open a file "cleverly".

    If the file name ends with ".gz" or ".bz2", it is compressed
    or uncompressed on the fly (according to the mode).

    In read mode (mode='r'), the filename '-' is interpreted as stdin.

    In write mode (mode='w'), the filename '-' is interpreted as stdout.
    """
    if mode == 'r':
        if fn == "-":
            return sys.stdin
        if fn.endswith(".gz"):
            p = subprocess.Popen(['gunzip', '-c', fn],
                                 stdout=subprocess.PIPE)
            return p.stdout
        if fn.endswith(".bz2"):
            p = subprocess.Popen(['bunzip2', '-c', fn],
                                 stdout=subprocess.PIPE)
    if mode == 'w':
        if fn == "-":
            return sys.stdout
        if fn.endswith(".gz"):
            p = subprocess.Popen(['gzip', '-9', '-', '>', fn],
                                 stdin=subprocess.PIPE,
                                 shell=True)
            return p.stdin
        if fn.endswith(".bz2"):
            p = subprocess.Popen(['bzip2', '-9', '-', '>', fn],
                                 stdout=subprocess.PIPE,
                                 shell=True)
        return p.stdin
    return open(fn, mode)

