def uniq(xs):
    """Remove duplicates from a sorted list in place."""
    if len(xs) < 2:
        return
    i = 1
    for j in xrange(1, len(xs)):
        if xs[j] != xs[j - 1]:
            if i != j:
                xs[i] = xs[j]
            i += 1
    del xs[i:]
