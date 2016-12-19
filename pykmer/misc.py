def uniq(xs):
    """
    Remove duplicates from the sorted list `xs`, in place.

    If `xs` is not sorted, this has undefined behaviour.
    """
    if len(xs) < 2:
        return
    i = 1
    for j in xrange(1, len(xs)):
        if xs[j] != xs[j - 1]:
            if i != j:
                xs[i] = xs[j]
            i += 1
    del xs[i:]
