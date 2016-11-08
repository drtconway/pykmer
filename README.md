# pykmer
A pure Python toolkit for k-mer manipulation.

It runs under the standard Python interpreter, but we recommend using it
with the pypy JIT compiling implementation (http:://pypy.org/).  The pypy
implementation deals well with the blocks of bit-fiddling code which
tend to be in the inner loops, whereas the standard Python is pretty slow.

Installing pykmer
-----------------

Installing under the standard Python environment should be easy:

    $ sudo pip install setuptools
    $ sudo pip install docopt
    $ python setup.py build
    $ python setup.py test
    $ sudo python setup.py install

It's a bit trickier under the Pypy environment because you might
need to install pip under pypy:

    $ wget https://bootstrap.pypa.io/get-pip.py
    $ sudo pypy get-pip.py
    $ sudo pypy -m pip install setuptools
    $ sudo pypy -m pip install docopt
    $ pypy setup.py build
    $ pypy setup.py test
    $ sudo pypy setup.py install

What is pykmer?
---------------

Pykmer is a pure Python for implementing bioinformatic analysis
with k-mer methods. The functionality includes
    * parsing FASTA and FASTQ files
    * extracting k-mers from reads
    * basic computations on k-mers including
        - reverse complements
        - longest common prefixes
        - Hamming distances
    * compressed files of k-mers
    * compressed files of (k-mer, frequency) pairs
    * some generally useful statistical functions

Why Pure Python?
----------------

Good question. Glad you asked!

The point of the pykmer library is partly as a teaching aid for
bioinformatics teaching, and partly as a very portable platform for
bacterial genomics.

Python is a pretty nice language for writing genomics analysis
code. Generators, list support, and so on make it easy to throw together
methods. Combining these things with the computational tricks available
when representing k-mers as integers, makes for a nice expressive
programming environment.

One problem is that scipy/numpy is not available under pypy at the
current time, however, we mostly don't need the features available in
numpy, so this isn't too much of a problem. The one glaring missing
thing however, is an efficient sort() method for builtin array objects,
analogous to list.sort().
