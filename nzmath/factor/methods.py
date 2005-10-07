"""
factor.method -- provide factoring methods.
"""

import arith1
#import nzmath.arith1 as arith1
import nzmath.prime as prime
import util
import find
from mpqs import mpqsfind

class DefaultMethod (util.FactoringMethod):
    """
    A factor method used as the default.

    It tries the trial division method first, then the p-1 method,
    and finally calls the MPQS.
    """
    def __init__(self):
        util.FactoringMethod.__init__(self)

    def factor(self, number, **options):
        """
        Factor the given positive integer.
        The returned value must be in the form of [(p1, e1), ..., (pn, en)].
        """
        if not self.validate_input_number(number):
            return []

        # backup
        original_return_type = options.get('return_type', '')

        # trial division first
        trial = TrialDivision()
        trial.verbose = self.verbose
        if number < 1000000:
            return trial.factor(number, **options)
        options['return_type'] = 'tracker'
        options['eratosthenes'] = options.get('eratosthenes', 100000)
        tracker = trial.factor(number, **options)

        # try p-1 method
        pmom = PMinusOneMethod()
        pmom.verbose = self.verbose
        tracker = pmom.continue_factor(tracker, **options)

        # finally mpqs
        options['return_type'] = original_return_type
        mpqs = MPQSMethod()
        mpqs.verbose = self.verbose
        return mpqs.continue_factor(tracker, **options)


class TrialDivision (util.FactoringMethod):
    """
    Class for trial division method.
    """

    def __init__(self):
        util.FactoringMethod.__init__(self)

    def factor(self, number, **options):
        """
        Factor the given integer by trial division.

        options for the trial sequence can be either:
        1) 'start' and 'stop' as range parameters.
        2) 'iterator' as an iterator of primes.
        3) 'eratosthenes' as an upper bound to make prime sequence by sieve.
        If none of the options above are given, prime factor is
        searched from 2 to the square root of the given integer.

        an option 'return_type' is for the returned type, whose value can be:
        1) 'list' for default type [(p1, e1), ..., (pn, en)].
        2) 'tracker' for alternative type FactoringInteger.
        """
        return util.FactoringMethod.factor(self, number, **options)

    def continue_factor(self, tracker, **options):
        """
        Continue factoring and return the result of factorization.

        The argument 'tracker' should be an instance of FactoringInteger.
        The returned type is FactoringInteger.

        options is the same for factor, but the default value for
        'return_type' is 'tracker'.
        """
        if not hasattr(self, 'primeseq'):
            try:
                options['n'] = tracker.getNextTarget()
            except LookupError:
                raise
            self.primeseq = self._parse_seq(options)
        return_list = (options.get('return_type', '') == 'list')

        while True:
            try:
                target = tracker.getNextTarget()
            except LookupError:
                # factored completely
                break
            p = self.find(target)
            if 1 < p < target:
                # factor found
                tracker.register(p, True)
            elif p == 1:
                # trial sequence exhausts
                break
        if return_list:
            return tracker.getResult()
        else:
            return tracker

    def _parse_seq(self, options):
        """
        Parse 'options' to define trial sequaence.
        """
        if 'start' in options and 'stop' in options:
            if 'step' in options:
                trials = iter(range(options['start'], options['stop'], options['step']))
            else:
                trials = iter(range(options['start'], options['stop']))
        elif 'iterator' in options:
            trials = options['iterator']
        elif 'eratosthenes' in options:
            trials = prime.generator_eratosthenes(options['eratosthenes'])
        elif options['n'] < 1000000:
            trials = prime.generator_eratosthenes(arith1.floorsqrt(options['n']))
        else:
            trials = prime.generator()
        return trials

    def find(self, target):
        """
        Return the minimum factor of 'target' in the sequence.
        """
        for p in self.primeseq:
            if not (target % p):
                return p
            if p ** 2 > target:
                break
        return 1


class PMinusOneMethod (util.FactoringMethod):
    """
    Class for p-1 method.
    """

    def __init__(self):
        util.FactoringMethod.__init__(self)

    def find(self, target):
        """
        Find a factor from the target number.
        """
        return find.pmom(target, verbose = self.verbose)


class RhoMethod (util.FactoringMethod):
    """
    Class for Pollard's rho method.
    """

    def __init__(self):
        util.FactoringMethod.__init__(self)

    def find(self, target):
        """
        Find a factor from the target number.
        """
        return find.rhomethod(target, verbose = self.verbose)


class MPQSMethod (util.FactoringMethod):
    """
    Class for Multi-Polynomial Quadratic Sieve method.
    """


    def __init__(self):
        util.FactoringMethod.__init__(self)

    def find(self, target):
        """
        Find a factor from the target number.
        """
        return mpqsfind(target, verbose = self.verbose)

def trialDivision(n, **options):
    """
    Factor the given integer by trial division.

    options for the trial sequence can be either:
    1) 'start' and 'stop' as range parameters.
    2) 'iterator' as an iterator of primes.
    3) 'eratosthenes' as an upper bound to make prime sequence by sieve.
    If none of the options above are given, prime factor is
    searched from 2 to the square root of the given integer.
    """
    method = TrialDivision()
    options['return_type'] = 'list'
    return method.factor(n, **options)

def pmom(n, **options):
    """
    Factor the given integer by Pollard's p-1 method.
    """
    method = PMinusOneMethod()
    options['return_type'] = 'list'
    return method.factor(n, **options)

def rhomethod(n, **options):
    """
    Factor the given integer by rho method.
    """
    method = RhoMethod()
    options['return_type'] = 'list'
    return method.factor(n, **options)

def mpqs(n, **options):
    """
    Factor the given integer by multi-polynomial quadratic sieve method.
    """
    method = MPQSMethod()
    options['return_type'] = 'list'
    return method.factor(n, **options)

def factor(n, method = 'default', **options):
    """
    Factor the given integer.

    By default, use several methods internally.
    Optional argument 'method' can be:
      'mpqs': use MPQSMethod.
      'pmom': use PMinusOneMethod.
      'rhomethod': use RhoMethod.
      'trialDivision': use TrialDivision.
    (In fact, its initial letter suffice to specify.)
    """
    method_table = {'d': DefaultMethod,
                    'm': MPQSMethod,
                    'p': PMinusOneMethod,
                    'r': RhoMethod,
                    't': TrialDivision}
    try:
        chosen_method = method_table[method[0]]()
    except KeyError:
        chosen_method = DefaultMethod()
    options['return_type'] = 'list'
    return chosen_method.factor(n, **options)