import unittest
import logging

from nzmath import *

from . import testAlgfield
from . import testAlgorithm
from . import testArith1
from . import testArygcd
from . import testBigrandom
from . import testBigrange
from . import testCombinatorial
from . import testCompatibility
from . import testCubic_root
from . import testEcpp
from . import testElliptic
from . import testEquation
from . import testFiniteField
from . import testGcd
from . import testGroup
from . import testImaginary
from . import testIntresidue
#import testIntegerResidueClass deprecated
from . import testLattice
from . import testMatrix
from . import testModule
from . import testMultiplicative
from . import testPermute
#import testPolynomial deprecated
from . import testPlugins
from . import testPrime
from . import testPrime_decomp
from . import testQuad
from . import testRational
#import testRationalFunction deprecated
from . import testReal
from . import testRing
from . import testRound2
from . import testSequence
from . import testSquarefree
from . import testVector
#import testZassenhaus deprecated
# nzmath.factor
from . import testFactorUtil
from . import testFactorMpqs
from . import testFactorEcm
from . import testFactorMethods
from . import testFactorMisc
# nzmath.poly
from . import testFormalsum
from . import testTermOrder
from . import testUnivar
from . import testUniutil
from . import testMultivar
from . import testMultiutil
from . import testPolyFactor
from . import testPolyHensel
from . import testPolyRing
from . import testRatfunc
from . import testGroebner


def suite():
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.startswith("test"):
            suite.addTest(all_names[name].suite())
    return suite


if __name__ == '__main__':
    logging.basicConfig()
    runner = unittest.TextTestRunner()
    runner.run(suite())
