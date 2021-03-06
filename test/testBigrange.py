import unittest
import itertools
import sys
import nzmath.bigrange as bigrange


class CountTest (unittest.TestCase):
    def testCount(self):
        maxint = sys.maxsize
        from_maxint = [maxint, maxint+1, maxint+2]
        self.assertEqual(from_maxint,
                         [i for i in itertools.islice(bigrange.count(maxint), 3)])
        # otoh, itertools.count raises in Python 2.5 (2.6 doesn't raise)
        if sys.version.startswith('2.5'):
            self.assertRaises(OverflowError,
                          itertools.islice(itertools.count(maxint), 3).__next__)


class ProgressionTest (unittest.TestCase):
    def testArithmeticProgression(self):
        maxint = sys.maxsize
        from_maxint = [maxint, maxint+1, maxint+2]
        self.assertEqual(from_maxint,
                         [i for i in itertools.islice(bigrange.arithmetic_progression(maxint, 1), 3)])

    def testGeometricProgression(self):
        self.assertEqual([3, 6, 12, 24],
                         [i for i in itertools.islice(bigrange.geometric_progression(3, 2), 4)])


class MultirangeTest (unittest.TestCase):
    def testBasic(self):
        it = bigrange.multirange([(1, 10, 3), (1, 10, 4)])
        self.assertEqual((1, 1), next(it))
        self.assertEqual((1, 5), next(it))
        self.assertEqual((1, 9), next(it))
        self.assertEqual((4, 1), next(it))
        self.assertEqual((4, 5), next(it))
        self.assertEqual((4, 9), next(it))
        self.assertEqual((7, 1), next(it))
        self.assertEqual((7, 5), next(it))
        self.assertEqual((7, 9), next(it))

class MultirangeRestrictionsTest (unittest.TestCase):
    def testBasic(self):
        it = bigrange.multirange_restrictions([(1, 10, 3), (1, 10, 4)], ascending=(1,))
        self.assertEqual((1, 1), next(it))
        self.assertEqual((1, 5), next(it))
        self.assertEqual((1, 9), next(it))
        self.assertEqual((4, 5), next(it))
        self.assertEqual((4, 9), next(it))
        self.assertEqual((7, 9), next(it))


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
