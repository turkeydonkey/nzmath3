"""
Groebner basis
"""


import nzmath.compatibility
import nzmath.ring as ring


def s_polynomial(f, g, order):
    """
    Return S-polynomial of f and g with respect to the order.

    S(f, g) = (lc(g)*T/lb(f))*f - (lc(f)*T/lb(g))*g,
    where T = lcm(lb(f), lb(g)).
    """
    f_lb, f_lc = order.leading_term(f) # term = (base, coeff)
    g_lb, g_lc = order.leading_term(g)
    t = f_lb.lcm(g_lb)
    return f.term_mul((t - f_lb, g_lc)) - g.term_mul((t - g_lb, f_lc))

def step_reduce(reducee, reducer, order):
    """
    Return the reduced polynomial of reducee by reducer.  That is, if
    one of reducee's bases is divisible by the leading base of reducer
    with respect to the order, the returned polynomial is the result
    of canceling out the term.
    """
    lb, lc = order.leading_term(reducer) # term = (base, coeff)
    for b, c in reducee.iterterms():
        if b.lcm(lb) == b:
            return reducee + reducer.term_mul((b - lb, -c / lc)), True
    return reducee, False

def reduce_closure(f, reducers, order):
    """
    Return normalized form of f with respect to reducer, a set of
    polynomials, and order.
    """
    while True:
        for reducer in reducers:
            f, reduced = step_reduce(f, reducer, order)
            if reduced:
                break
        else:
            return f

def buchberger(generating, order):
    """
    Return a Groebner basis of the ideal generated by given generating
    set of polynomials with respect to the order.

    Be careful, this implementation is very naive.
    """
    pairs = []
    for f in generating:
        for g in generating:
            if f is g:
                continue
            pairs.append((f, g))
    groebner = list(generating)

    # main loop
    while pairs:
        f, g = pairs.pop()
        h = reduce_closure(s_polynomial(f, g, order), groebner, order)
        if h:
            for f in groebner:
                pairs.append((f, h))
            groebner.append(h)

    # finish
    return groebner

def reduce_groebner(gbasis, order):
    """
    Return the reduced Groebner basis constructed from a Groebner
    basis.

    1) lb(f) divides lb(g) => g is not in reduced Groebner basis
    2) monic
    """
    reduced_basis = []
    lb_rel = dict([(order.leading_term(g)[0], g) for g in gbasis])
    lbs = sorted([order.leading_term(g)[0] for g in gbasis])[::-1]
    for i, lbi in enumerate(lbs):
        for lbj in lbs[(len(lbs) - 1):i:-1]:
            if lbi == lbj.lcm(lbi):
                # divisor found
                break
        else:
            g = lb_rel[lbi]
            if g[lbi] != ring.getRing(g[lbi]).one:
                # make it monic
                g = g.scalar_mul(ring.inverse(g[lbi]))
            reduced_basis.append(g)
    return reduced_basis

def normal_strategy(generating, order):
    """
    Return a Groebner basis of the ideal generated by given generating
    set of polynomials with respect to the order.

    This function uses the 'normal strategy'.
    """
    groebner = list(generating) # omit reduction
    pairs, lcms = [], []
    treat = set()
    for i, f in enumerate(groebner):
        lb_f = order.leading_term(f)[0]
        for j, g in enumerate(groebner):
            if j <= i:
                continue
            lb_g = order.leading_term(g)[0]
            lcm_f_g = lb_f.lcm(lb_g)
            if lcm_f_g == lb_f + lb_g: # disjoint
                treat.add((i, j))
                treat.add((j, i))
            else:
                # keep lcms sorted, and so pairs in paralell
                k = order.bisect(lcms, lcm_f_g)
                pairs.insert(k, (i, j))
                lcms.insert(k, lcm_f_g)

    # main loop
    while pairs:
        i, j = pairs.pop(0)
        lcm_f_g = lcms.pop(0)
        treat.add((i, j))
        for p in range(len(groebner)):
            if (i, p) in treat and (p, j) in treat:
                pivot = order.leading_term(groebner[p])[0]
                if pivot.lcm(lcm_f_g) == lcm_f_g:
                    break
        else:
            f, g = groebner[i], groebner[j]
            h = reduce_closure(s_polynomial(f, g, order), groebner, order)
            if h:
                lb_h = order.leading_term(h)[0]
                hindex = len(groebner)
                for i, f in enumerate(groebner):
                    lb_f = order.leading_term(f)[0]
                    lcm_f_h = lb_f.lcm(lb_h)
                    if lcm_f_h == lb_f + lb_h: # disjoint
                        treat.add((i, hindex))
                    else:
                        k = order.bisect(lcms, lcm_f_h)
                        pairs.insert(k, (i, hindex))
                        lcms.insert(k, lcm_f_h)
                groebner.append(h)

    # finish
    return groebner
