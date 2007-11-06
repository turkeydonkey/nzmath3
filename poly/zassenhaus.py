from __future__ import division
import random
import operator
import nzmath.arith1 as arith1
import nzmath.prime as prime
import nzmath.rational as rational
import nzmath.combinatorial as combinatorial
import nzmath.integerResidueClass as integerResidueClass
import nzmath.finitefield as finitefield
import nzmath.poly.uniutil as uniutil


uniutil.special_ring_table[finitefield.FinitePrimeField] = uniutil.FinitePrimeFieldPolynomial


def zassenhaus(f):
    """
    zassenhaus(f) -> list of factors of f.

    Factor a squarefree monic integer coefficient polynomial f with
    Berlekamp-Zassenhaus method.
    """
    p, fp_factors = padicFactorization(f)
    if len(fp_factors) == 1:
        return [f]
    # lift to Mignotte bound
    blm = upperBoundOfCoefficient(f)
    q = p
    while q < 2*blm:
        fp_factors = padicLiftList(f, fp_factors, p, q)
        q *= p
    return bruteForceSearch(f, fp_factors, q)

def padicFactorization(f):
    """
    padicFactorization(f) -> p, factors

    Return a prime p and a p-adic factorization of given integer
    coefficient squarefree polynomial f. The result factors have
    integer coefficients, injected from F_p to its minimum absolute
    representation. The prime is chosen to be 1) f is still squarefree
    mod p, 2) the number of factors is not greater than with the
    successive prime.
    """
    num_factors = f.degree()
    stock = None
    for p in prime.generator():
        fmodp = uniutil.polynomial(
            f.terms(),
            finitefield.FinitePrimeField.getInstance(p))
        g = fmodp.getRing().gcd(fmodp,
                                fmodp.differentiate())
        if g.degree() == 0:
            fp_factors = fmodp.factor()
            if not stock or num_factors > len(fp_factors):
                stock = (p, fp_factors)
                if len(fp_factors) == 1:
                    return stock
                num_factors = len(fp_factors)
            else:
                break
    p = stock[0]
    fp_factors = []
    for (fp_factor, m) in stock[1]:
        assert m == 1 # since squarefree
        fp_factors.append(minimumAbsoluteInjection(fp_factor))
    return (p, fp_factors)

def bruteForceSearch(f, fp_factors, q):
    """
    bruteForceSearch(f, fp_factors, q) -> [factors]

    Find the factorization of f by searching a factor which is a
    product of some combination in fp_factors.  The combination is
    searched by brute force.
    """
    factors = []
    d, r = 1, len(fp_factors)
    while 2*d <= r:
        found, combination = findCombination(f, d, fp_factors, q)
        if found:
            factors.append(found)
            for picked in combination:
                fp_factors.remove(picked)
            f = f.pseudo_floordiv(found)
            r -= d
        else:
            d += 1
    factors.append(f)
    return factors

def padicLiftList(f, factors, p, q):
    """
    padicLift(f, factors, p, q) -> lifted_factors

    Find a lifted integer coefficient polynomials such that:
      f = G1*G2*...*Gm (mod q*p),
      Gi = gi (mod q),
    from f and gi's of integer coefficient polynomials such that:
      f = g1*g2*...*gm (mod q),
      gi's are pairwise coprime
    with positive integers p dividing q.
    """
    ZpZx = uniutil.PolynomialRingAnonymousVariable(
        integerResidueClass.IntegerResidueClassRing.getInstance(p))
    gg = reduce(operator.mul, factors, 1)
    h = ZpZx.createElement([(d, c // q) for (d, c) in (f - gg).iterterms()])
    lifted = []
    for g in factors:
        gg = gg.pseudo_floordiv(g)
        g_mod = ZpZx.createElement(g)
        if gg.degree() == 0:
            break
        u, v, w = extgcdp(g, gg, p)
        if w.degree() > 0:
            raise ValueError("factors must be pairwise coprime.")
        v_mod = ZpZx.createElement(v)
        t = v_mod * h // g_mod
        lifted.append(g + minimumAbsoluteInjection(v_mod * h - g_mod * t)*q)
        u_mod = ZpZx.createElement(u)
        gg_mod = ZpZx.createElement(gg)
        h = u_mod * h + gg_mod * t
    lifted.append(g + minimumAbsoluteInjection(h)*q)
    return lifted

def extgcdp(f, g, p):
    """
    extgcdp(f,g,p) -> u,v,w

    Find u,v,w such that f*u + g*v = w = gcd(f,g) mod p.
    """
    zpz = integerResidueClass.IntegerResidueClassRing.getInstance(p)
    f_zpz = uniutil.polynomial(f, zpz)
    g_zpz = uniutil.polynomial(g, zpz)
    zero, one = f_zpz.getRing().zero, f_zpz.getRing().one
    u, v, w, x, y, z = one, zero, f_zpz, zero, one, g_zpz
    while z:
        q = w // z
        u, v, w, x, y, z = x, y, z, u - q*x, v - q*y, w - q*z
    if w.degree() == 0 and w[0] != zpz.one:
        u = u.scalar_exact_division(w[0]) # u / w
        v = v.scalar_exact_division(w[0]) # v / w
        w = w.getRing().one # w / w
    u = minimumAbsoluteInjection(u)
    v = minimumAbsoluteInjection(v)
    w = minimumAbsoluteInjection(w)
    return u, v, w

def minimumAbsoluteInjection(f):
    """
    minimumAbsoluteInjection(f) -> F

    Return an integer coefficient polynomial F by injection of a Z/pZ
    coefficient polynomial f with sending each coefficient to minimum
    absolute representatives.
    """
    coefficientRing = f.getCoefficientRing()
    if isinstance(coefficientRing, integerResidueClass.IntegerResidueClassRing):
        p = coefficientRing.m
    elif isinstance(coefficientRing, finitefield.FinitePrimeField):
        p = coefficientRing.getCharacteristic()
    else:
        raise TypeError("unknown ring (%s)" % repr(coefficientRing))
    half = p // 2
    g = {}
    for i, c in f.iterterms():
        if c.n > half:
            g[i] = c.n - p
        else:
            g[i] = c.n
    return uniutil.polynomial(g, rational.theIntegerRing)


def upperBoundOfCoefficient(f):
    """
    upperBoundOfCoefficient(polynomial) -> int

    Compute Landau-Mignotte bound of coefficients of factors, whose
    degree is no greater than half of the given polynomial.  The given
    polynomial must have integer coefficients.
    """
    weight = 0
    for c in f.itercoefficients():
        weight += abs(c)**2
    weight = arith1.floorsqrt(weight) + 1
    degree = f.degree()
    lc = f[degree]
    m = degree // 2 + 1
    bound = 1
    for i in range(1, m):
        b = combinatorial.binomial(m - 1, i) * weight + \
            combinatorial.binomial(m - 1, i - 1) * lc
        if bound < b:
            bound = b
    return bound

def findCombination(f, d, factors, q):
    """
    findCombination(f, d, factors, q) -> g, list

    Find a combination of d factors which divides f (or its
    complement).  The returned values are: the product g of the
    combination and a list consisting of the combination itself.
    If there is no combination, return (0,[]).
    """
    if d == 1:
        for g in factors:
            if divisibilityTest(f, g):
                return (g, [g])
    else:
        ZqZ = integerResidueClass.IntegerResidueClassRing.getInstance(q)
        ZqZX = uniutil.PolynomialRingAnonymousVariable.getInstance(ZqZ)
        for idx in combinatorial.combinationIndexGenerator(len(factors), d):
            picked = [factors[i] for i in idx]
            product = reduce(operator.mul, picked, 1)
            product = minimumAbsoluteInjection(ZqZX.createElement(product))
            if divisibilityTest(f, product):
                return (product, picked)
    return 0, [] # nothing found

def divisibilityTest(f, g):
    """
    Return boolean value whether f is divisible by g or not, for polynomials.
    """
    if g[0] and f[0] % g[0]:
        return False
    if isinstance(f, uniutil.FieldPolynomial) and f % g:
        return False
    elif isinstance(f, uniutil.UniqueFactorizationDomainPolynomial) and f.pseudo_mod(g):
        return False
    return True

def complexRootAbsoluteUpperBound(f):
    """
    complexRootAbsoluteUpperBound(f) -> m

    Return an upper bound of absolute value of complex root of given
    (complex coefficient) polynomial f.
    """
    n = 0
    for i, c in f.coefficient.iteritems():
        if i == f.degree():
            d = abs(c)
        elif n < abs(c):
            n = abs(c)
    return int(2 + n/d)
