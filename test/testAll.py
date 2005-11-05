import unittest
import testArith1
import testBigrandom
import testCombinatorial
import testElliptic
import testEquation
import testFactorUtil
import testFactorMpqs
import testFactorMethods
import testFactorMisc
import testFiniteField
import testGcd
import testImaginary
import testIntegerResidueClass
import testLattice
import testMatrix
import testPolynomial
import testPrime
import testRational
import testRationalFunction
import testReal
import testRing
import testVector
import testMultiplicative
import testZassenhaus

def suite():
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.startswith("test"):
            suite.addTest(all_names[name].suite())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
