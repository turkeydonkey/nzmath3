import unittest
import math
import real
import rational

class ErrorTest (unittest.TestCase):
    def testRelativeError(self):
        assert real.RelativeError(0,1,2)
        assert isinstance(real.RelativeError(0,1,2).absoluteerror(3,4), real.AbsoluteError)

    def testAbsoluteError(self):
        assert real.AbsoluteError(0,1,2)

    def testRelativeNearlyEqual(self):
        assert real.RelativeError(0,1,2).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.RelativeError(-1,1,2).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert not real.RelativeError(1,1,2).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.RelativeError(1,1,3).nearlyEqual(rational.Rational(1,3), rational.Rational(1,4))

    def testAbsoluteNearlyEqual(self):
        assert real.AbsoluteError(0,1,8).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.AbsoluteError(-1,1,8).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert not real.AbsoluteError(1,1,8).nearlyEqual(rational.Rational(1,4), rational.Rational(1,3))
        assert real.AbsoluteError(1,1,10).nearlyEqual(rational.Rational(1,3), rational.Rational(1,4))

    def testLt(self):
        assert real.RelativeError(0,1,4) < real.RelativeError(0,1,3)
        assert real.AbsoluteError(0,1,4) < real.AbsoluteError(0,1,3)
        assert not real.RelativeError(0,1,4) < real.RelativeError(0,1,5)
        assert not real.AbsoluteError(0,1,4) < real.AbsoluteError(0,1,5)
        assert real.RelativeError(1,1,4) < real.RelativeError(0,1,3)
        assert real.AbsoluteError(1,1,4) < real.AbsoluteError(0,1,3)
        assert not real.RelativeError(1,1,4) < real.RelativeError(-1,1,3)
        assert not real.AbsoluteError(1,1,4) < real.AbsoluteError(-1,1,3)
        assert not real.RelativeError(0,1,4) < real.AbsoluteError(0,1,3)
        assert not real.AbsoluteError(0,1,4) < real.RelativeError(0,1,3)

class NewFunctionTest (unittest.TestCase):
    def setUp(self):
        self.err = real.RelativeError(0, 1, 2**100)
        self.relative = rational.Rational(1 + 2**53, 2**53)
        self.absolute = rational.Rational(1, 2**53)

    def testSqrt(self):
        sqrt0 = real.sqrt(0)
        assert sqrt0 == 0
        sqrt2 = real.sqrt(2)
        assert abs(sqrt2 ** 2 - 2) < self.absolute

    def testExp(self):
        assert 1 == real.exp(0)
        exp1 = real.exp(1)
        exp1e = real.exp(1, self.err)
        assert exp1 < exp1e < exp1 * self.relative
        exp2 = real.exp(2)
        exp2e = real.exp(2, self.err)
        assert exp2 < exp2e < exp2 * self.relative
        assert "2.718281828459045" == exp1.decimalString(15)

    def testLog(self):
        log1 = real.log(1)
        assert 0 == log1
        log2inverse = real.log(.5)
        assert log2inverse < 0
        assert abs(real.log(2) + log2inverse) < self.absolute
        assert abs(real.log(real.exp(1)) - 1)  < 2 * self.absolute
        assert abs(real.log(real.exp(1).trim(2**53)) - 1) < 2 * self.absolute

    def testPiGaussLegendre(self):
        pi = real.pi
        assert rational.Rational(355,113) == pi.trim(365)
        assert abs(pi - real.piGaussLegendre(self.err)) < self.absolute

    def testFloor(self):
        assert 3 == real.floor(3)
        assert -3 == real.floor(-3)
        assert 3 == real.floor(3.5)
        assert -3 == real.floor(-2.5)

    def testCeil(self):
        assert 3 == real.ceil(3)
        assert -3 == real.ceil(-3)
        assert 4 == real.ceil(3.5)
        assert -2 == real.ceil(-2.5)

    def testTranc(self):
        assert 3 == real.tranc(3)
        assert -3 == real.tranc(-3)
        assert 3 == real.tranc(3.3)
        assert -3 == real.tranc(-2.7)

    def testTrigonometric(self):
        assert 0 == real.sin(0)
        assert 1 == real.cos(0)
        assert 0 == real.tan(0)
        pi = real.pi
        assert abs(real.sin(pi)) < self.absolute
        assert -1 <= (real.cos(pi)) < -1 + self.absolute
        assert abs(real.tan(pi)) < self.absolute

    def testHyperbolic(self):
        assert 0 == real.sinh(0)
        assert 1 == real.cosh(0)
        assert 0 == real.tanh(0)

    def testInverseTrigonometric(self):
        assert 0 == real.asin(0)
        assert abs(real.pi / 2 - real.acos(0)) < self.absolute
        assert 0 == real.atan(0)

    def testHypot(self):
        assert abs(real.hypot(3,4) - 5) < self.absolute

class ConstantTest (unittest.TestCase):
    def testToRational(self):
        assert isinstance(real.pi.toRational(), rational.Rational)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ErrorTest, 'test'))
    suite.addTest(unittest.makeSuite(NewFunctionTest, 'test'))
    suite.addTest(unittest.makeSuite(ConstantTest, 'test'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
