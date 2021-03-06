import unittest
from nzmath.poly.array import *


class ArrayPolyArithmeticTest(unittest.TestCase):
    def setUp(self):
        self.f = ArrayPoly([1, 2, 0, 0, 3])
        self.g = ArrayPoly([0, -1, 0, 2])
        self.h = ArrayPoly([1, 2, 3, 4, 0])

    def testCheckZeroPoly(self):
        self.assertTrue(check_zero_poly([0, 0, 0]))
        self.assertFalse(check_zero_poly([0, 0, 1]))

    def testArrangeCoefficients(self):
        self.assertEqual([0], arrange_coefficients([0, 0, 0]))
        self.assertEqual([1, 2, 0, 3], arrange_coefficients([1, 2, 0, 3, 0]))

    def testInit(self):
        self.assertEqual([1, 2, 0, 0, 3], self.f.coefficients)
        self.assertEqual(4, self.f.degree)
        self.assertEqual([1, 2, 3, 4], self.h.coefficients)
        self.assertEqual(3, self.h.degree)

    def testCoefficientsToDict(self):
        self.assertEqual({1 : -1, 3 : 2}, self.g.coefficients_to_dict())
        self.assertEqual({0 : 0}, ArrayPoly([0]).coefficients_to_dict())

    def testAdd(self):
        t = ArrayPoly([1, 1, 0, 2, 3])
        self.assertEqual(t, self.f + self.g)
        self.assertEqual(t, self.g + self.f)

    def testSub(self):
        t = ArrayPoly([1, 3, 0, -2, 3])
        self.assertEqual(t, self.f - self.g)

    def testScalarMul(self):
        t = ArrayPoly([3, 6, 0, 0, 9])
        self.assertEqual(t, self.f.scalar_mul(3))

    def testUpshiftDegree(self):
        t1 = ArrayPoly([1, 2, 0, 0, 3])
        t2 = ArrayPoly([0, 0, 0, 1, 2, 0, 0, 3])
        self.assertEqual(t1, self.f.upshift_degree(0))
        self.assertEqual(t2, self.f.upshift_degree(3))

    def testDownshiftDegree(self):
        t1 = ArrayPoly([1, 2, 0, 0, 3])
        t2 = ArrayPoly([0])
        t3 = ArrayPoly([0, 3])
        self.assertEqual(t1, self.f.downshift_degree(0))
        self.assertEqual(t2, self.f.downshift_degree(10))
        self.assertEqual(t3, self.f.downshift_degree(3))

    def testEq(self):
        t = ArrayPoly([1, 2, 0, 0, 3])
        self.assertTrue(t == self.f)

    def testNe(self):
        t = ArrayPoly([1, 2, 0, 0, 3])
        self.assertTrue(t != self.g)

    def testMul(self):
        t = ArrayPoly([0, -1, -2, 2, 4, -3, 0, 6])
        self.assertEqual(t, self.f * self.g)
        self.assertEqual(t, self.g * self.f)

    def testPower(self):
        t = ArrayPoly([1, 4, 4, 0, 6, 12, 0, 0, 9])
        self.assertEqual(t, self.f.power())

    def testSplitAt(self):
        t1 = ArrayPoly([0, -1])
        t2 = ArrayPoly([0, 0, 0, 2])
        self.assertEqual((ArrayPoly([0]), self.g), self.g.split_at(0))
        self.assertEqual((self.g, ArrayPoly([0])), self.g.split_at(10))
        self.assertEqual((t1, t2), self.g.split_at(2))

    def testFFTMul(self):
        t = ArrayPoly([0, -1, -2, 2, 4, -3, 0, 6])
        self.assertEqual(t, self.f.FFT_mul(self.g))
        self.assertEqual(t, self.g.FFT_mul(self.f))

    def testFFT(self):
        self.assertEqual([6, 53, 777, 12305, 30, 17, 64898, 53506, 516, 1073, 2817, 16385, 8190, 16337, 32001, 53249, 2, 45, 761, 12273, 65503, 65426, 64642, 52994, 65029, 64562, 64258, 8193, 57343, 49106, 32002, 53251], FFT(self.f, 32))

    def testReverseFFT(self):
        values = [6, 742, 96348, 12501880, 245280, 1113568, 4248547570, 3496349570, 33420804, 65376817, 89425665, 1040332805, 503463870, 941027537, 1638483201, 2617348097, 131072, 2948535, 49779293, 791866233, 3757317583, 2159058, 4654224, 10174848, 49942272, 297501696, 2171406336, 16746492, 233041952, 389705216, 458780672, 872464384]
        total = [0, -1, -2, 2, 4, -3, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(total, reverse_FFT(values, 32))

    def testMinAbsMod(self):
        self.assertEqual(-4, min_abs_mod(7, 11))

    def testBitReverse(self):
        self.assertEqual(13, bit_reverse(11, 10))

    def testPerfectShuffle(self):
        self.assertEqual([1, 5, 3, 7, 2, 6, 4, 8], perfect_shuffle([1, 2, 3, 4, 5, 6, 7, 8]))

        

class ArrayPolyModArithmeticTest(unittest.TestCase):
    def setUp(self):
        self.f = ArrayPolyMod([1, 2, 0, 0, 3], 11)
        self.g = ArrayPolyMod([0, -1, 0, 2], 11)
        self.h = ArrayPolyMod([12, 13, 14], 11)

    def testInit(self):
        self.assertEqual([1, 2, 0, 0, 3], self.f.coefficients)
        self.assertEqual(4, self.f.degree)
        self.assertEqual([1, 2, 3 ], self.h.coefficients)
        self.assertEqual(2, self.h.degree)

    def testMul(self):
        t = ArrayPolyMod([0, -1, -2, 2, 4, -3, 0, 6], 11)
        self.assertEqual(t, self.f * self.g)
        self.assertEqual(t, self.g * self.f)

    def testPower(self):
        t = ArrayPolyMod([1, 4, 4, 0, 6, 1, 0, 0, 9], 11)
        self.assertEqual(t, self.f.power())

    def testSplitAt(self):
        t1 = ArrayPolyMod([0, -1], 11)
        t2 = ArrayPolyMod([0, 0, 0, 2], 11)
        self.assertEqual((ArrayPolyMod([0], 11), self.g), self.g.split_at(0))
        self.assertEqual((self.g, ArrayPolyMod([0], 11)), self.g.split_at(10))
        self.assertEqual((t1, t2), self.g.split_at(2))

    def testFFTMul(self):
        t = ArrayPolyMod([0, -1, -2, 2, 4, -3, 0, 6], 11)
        self.assertEqual(t, self.f.FFT_mul(self.g))
        self.assertEqual(t, self.g.FFT_mul(self.f))


def suite(suffix="Test"):
    suite = unittest.TestSuite()
    all_names = globals()
    for name in all_names:
        if name.endswith(suffix):
            suite.addTest(unittest.makeSuite(all_names[name], "test"))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
