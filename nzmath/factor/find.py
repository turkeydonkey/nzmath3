"""
All methods defined here returns one of a factor of given integer.
When 1 is returned, the method has failed to factor,
but 1 is a factor anyway.

'verbose' boolean flag can be specified for verbose reports.
"""

import arith1
#import nzmath.arith1 as arith1
import nzmath.bigrandom as bigrandom
import nzmath.gcd as gcd
import nzmath.prime as prime

# Pollard's rho method
def rhomethod(n, **options):
    """
    Find a non-trivial factor of n using Pollard's rho algorithm.
    The implementation refers the explanation in C.Pomerance's book.
    """
    # verbosity
    verbose = options.get('verbose', False)

    if n <= 3:
        return 1

    g = n
    while g == n:
        a = bigrandom.randrange(1, n-2)
        s = bigrandom.randrange(0, n-1)
        u = v = s
        g = gcd.gcd((v**2 + v + a) % n - u, n)
        while g == 1:
            u = (u**2 + a) % n
            v = ((pow(v, 2, n) + a)**2 + a) % n
            g = gcd.gcd(v - u, n)
    return g

# p-1 method
def pmom(n, **options):
    """
    This program tries to find a non-trivial factor of N using
    Algorithm 8.8.2 (p-1 first stage) of Cohen's book.
    In case of N = pow(2,i), this program will not terminate.
    """
    # verbosity
    verbose = options.get('verbose', False)

    # initialize
    x , B = 2 , 10000001
    y = x
    primes = []

    for q in prime.generator():
        primes.append(q)
        if q > B:
            if gcd.gcd(x-1, n) == 1:
                return 1
            x = y
            break
        q1 = q
        l = B//q
        while q1 <= l:
            q1 *= q
        x = pow(x, q1, n)
        if len(primes) >= 20:
            if gcd.gcd(x-1, n) == 1:
                primes, y = [], x
            else:
                x = y
                break

    for q in primes:
        q1 = q
        while q1 <= B:
            x = pow(x, q, n)
            g = gcd.gcd(x-1, n)
            if g != 1:
                if g == n:
                    return 1
                return g
            q1 *= q

def trialDivision(n, **options):
    """
    Return a factor of given integer by trial division.

    options can be either:
    1) 'start' and 'stop' as range parameters.
    2) 'iterator' as an iterator of primes.
    If both options are not given, prime factor is searched from 2
    to the square root of the given integer.
    """
    if 'start' in options and 'stop' in options:
        if 'step' in options:
            trials = range(options['start'], options['stop'], options['step'])
        else:
            trials = range(options['start'], options['stop'])
    elif 'iterator' in options:
        trials = options['iterator']
    elif n < 1000000:
        trials = prime.generator_eratosthenes(arith1.floorsqrt(n))
    else:
        trials = prime.generator()
    # verbosity
    verbose = options.get('verbose', False)

    for p in trials:
        if not (n % p):
            return p
        if p ** 2 > n:
            break
    return 1
