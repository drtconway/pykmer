"""
This module provides a collection functions for estimating the *distance*
between *k*-mer spectra or *k*-mer sets.

All the distance functions take a Boolean parameter which is used to
distinguish between the *k*-mer spectrum form (a vector of 4**k frequency
values) and the set form (a list/array of *k*-mer values).

The distance functions were taken from
https://arxiv.org/pdf/1604.02412.pdf Table 1.
"""

__docformat__ = 'restructuredtext'

import math

def brayCurtis(xs, ys, vec=False):
    """
    Compute the Bray-Curtis distance between `xs` and `ys`.

    If `vec` is True, the result is the quantitative Bray-Curtis distance;
    otherwise it is the qualitative Bray-Curtis distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        assert len(xs) == len(ys)
        Z = len(xs)
        cx = float(sum(xs))
        cy = float(sum(ys))
        sxy = float(cx+cy)
        s = 0
        for i in xrange(Z):
            s += float(min(xs[i], ys[i]))/sxy
        return 1 - 2*s
    else:
        (a, b, c) = split(xs, ys)
        return float(b + c) / float(2*a + b + c)


def chord(xs, ys, vec=False):
    """
    Compute the Chord distance between `xs` and `ys`.

    If `vec` is True, the result is the quantitative Chord distance;
    otherwise it is the qualitative Chord/Hellinger distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        assert len(xs) == len(ys)
        Z = len(xs)
        cx = sum(xs)
        cy = sum(ys)
        cxy = float(cx*cy)
        s = 0
        for i in xrange(Z):
            s += (xs[i]*ys[i])/cxy
        return math.sqrt(2 - 2*s)
    else:
        (a, b, c) = split(xs, ys)
        return math.sqrt(2*(1 - a/math.sqrt((a + b)*(a + c))))

def hellinger(xs, ys, vec=False):
    """
    Compute the Chord distance between `xs` and `ys`.

    If `vec` is True, the result is the quantitative Hellinger distance;
    otherwise it is the qualitative Chord/Hellinger distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        assert len(xs) == len(ys)
        Z = len(xs)
        cx = sum(xs)
        cy = sum(ys)
        cxy = math.sqrt(cx*cy)
        s = 0
        for i in xrange(Z):
            s += math.sqrt(xs[i]*ys[i])/cxy
        return math.sqrt(2 - 2*s)
    else:
        (a, b, c) = split(xs, ys)
        return math.sqrt(2*(1 - a/math.sqrt((a + b)*(a + c))))

def jaccard(xs, ys, vec=False):
    """
    Compute the Jaccard distance between `xs` and `ys`.

    If `vec` is True, the result is the abundance-based Jaccard distance;
    otherwise it is the qualitative Jaccard distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        (u, v) = decompose(xs, ys)
        return 1 - u*v/(u + v - u*v)
    else:
        (a, b, c) = split(xs, ys)
        return float(b + c) / float(a + b + c)

def jensenShannon(xs, ys, vec=False):
    """
    Compute the Jensen-Shannon distance between `xs` and `ys`.

    If `vec` is True, the result is the quantitative Jesen-Shannon distance;
    if `vec` is not True, an exception is raised.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        assert len(xs) == len(ys)
        Z = len(xs)
        cx = float(sum(xs))
        cy = float(sum(ys))
        cxy = float(cx*cy)
        sxy = float(cx+cy)
        s = 0
        for i in xrange(Z):
            if xs[i] == 0 or ys[i] == 0:
                continue
            s += xs[i]/cx*math.log(2*cy*xs[i]/(cy*xs[i] + cx*ys[i]))
            s += ys[i]/cy*math.log(2*cx*ys[i]/(cx*ys[i] + cy*xs[i]))
        return math.sqrt(0.5*s)
    else:
        raise "Jensen-Shannon cannot be computed over k-mer lists"

def kulczynski(xs, ys, vec=False):
    """
    Compute the Kulczyski distance between `xs` and `ys`.

    If `vec` is True, the result is the quantitative Kulczyski distance;
    otherwise it iss the qualitative Kulczyski distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        assert len(xs) == len(ys)
        Z = len(xs)
        cx = sum(xs)
        cy = sum(ys)
        cxy = float(cx*cy)
        sxy = float(cx+cy)
        s = 0
        for i in xrange(Z):
            s += sxy*min(xs[i], ys[i])/cxy
        return 1 - 0.5*s
    else:
        (a, b, c) = split(xs, ys)
        a = float(a)
        b = float(b)
        c = float(c)
        return 1 - 0.5*(a/(a+b) + a/(a+c))

def ochiai(xs, ys, vec=False):
    """
    Compute the Ochiai distance between `xs` and `ys`.

    If `vec` is True, the result is the abundance-based Ochiai distance;
    otherwise it iss the qualitative Ochiai distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        (u, v) = decompose(xs, ys)
        return 1 - math.sqrt(u*v)
    else:
        (a, b, c) = split(xs, ys)
        return 1 - a/math.sqrt((a + b)*(a + c))

def sorensen(xs, ys, vec=False):
    """
    Compute the Sorensen distance between `xs` and `ys`.

    If `vec` is True, the result is the abundance-based Sorensen distance;
    otherwise it iss the qualitative Sorensen distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        (u, v) = decompose(xs, ys)
        return 1 - 2*u*v/(u+v)
    else:
        (a, b, c) = split(xs, ys)
        return float(b + c) / float(2*a + b + c)

def whittaker(xs, ys, vec=False):
    """
    Compute the Whittaker distance between `xs` and `ys`.

    If `vec` is True, the result is the quantitative Whittaker distance;
    otherwise it iss the qualitative Whittaker distance.

    If `vec` is True, `xs` and `ys` are assumed to be *k*-mer frequency
    spectra - lists/arrays of 4**k elements giving the frequency of each
    possible *k*-mer; if `vec` is false, they are assumed to be sets of
    *k*-mers represented as sorted lists/arrays.
    """
    if vec:
        assert len(xs) == len(ys)
        Z = len(xs)
        cx = sum(xs)
        cy = sum(ys)
        cxy = float(cx*cy)
        s = 0
        for i in xrange(Z):
            s += abs(xs[i] - ys[i])/cxy
        return 0.5*s
    else:
        (a, b, c) = split(xs, ys)
        a = float(a)
        b = float(b)
        c = float(c)
        return 0.5*(b/(a+b) + c/(a+c) + abs(a/(a+b) - a/(a+c)))

def split(xs, ys):
    xz = len(xs)
    yz = len(ys)
    i = 0
    j = 0
    dx = 0
    dy = 0
    b = 0
    while i < xz and j < yz:
        x = xs[i]
        y = ys[j]
        if x < y:
            dx += 1
            i += 1
            continue
        if x > y:
            dy += 1
            j += 1
            continue
        b += 1
        i += 1
        j += 1
    dx += xz - i
    dy += yz - j
    return (b, dx, dy)

def decompose(xs, ys):
    assert len(xs) == len(ys)
    Z = len(xs)
    yxy = 0
    yyx = 0
    cx = 0
    cy = 0
    for i in xrange(Z):
        if xs[i] > 0 and ys[i] > 0:
            yxy += xs[i]
            yyx += ys[i]
        cx += xs[i]
        cy += ys[i]
    return (float(yxy)/float(cx), float(yyx)/float(cy))

