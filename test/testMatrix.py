
import unittest
from nzmath.matrix import *
import nzmath.vector as vector
import nzmath.rational as rational
import nzmath.poly.uniutil as uniutil

Ra = rational.Rational
Poly = uniutil.polynomial
Int = rational.theIntegerRing

# sub test
try:
    from test.testMatrixFiniteField import *
except:
    try:
        from nzmath.test.testMatrixFiniteField import *
    except:
        from .testMatrixFiniteField import *

## for RingMatrix
a1 = createMatrix(1, 2, [3, 2])
a2 = Matrix(1, 2, [5, -6])
a3 = createMatrix(3, 2, [7, 8]+[3, -2]+[0, 10])
a4 = Matrix(3, 2, [21, -12]+[1, -1]+[0, 0])
a5 = createMatrix(1, 2, [Poly({0:3, 1:5}, Int), Poly({1:2}, Int)])

## for RingSquareMatrix
b1 = createMatrix(2, 2, [1, 2]+[3, 4])
b2 = Matrix(2, 2, [0, -1]+[1, -2])
b3 = createMatrix(3, 3, [0, 1, 2]+[5, 4, 6]+[7, 9, 8])
b4 = Matrix(3, 3, [1, 2, 3]+[0, 5, -2]+[7, 1, 9])
b5 = createMatrix(3, 3, [1, 3, 2, 4, 6, 5, 6, 8, 9])
b6 = createMatrix(3, 3, [1, 2, 4, 0, 3, 5, 0, 0, 0])
b7 = createMatrix(3, 3, [1, 0, 0, 9, 1, 0, 5, 6, 1])
b8 = Matrix(3, 3, [3, 15, 12]+[2,7,5]+[1,-4,-2])

## for FieldMatrix
c1 = createMatrix(1, 2, [Ra(3), Ra(2)])
c2 = createMatrix(4, 5, \
[Ra(0), 0, 1, 2, -1]+[0, 0, 5, 12, -2]+[0, 0, 1, 3, -1]+[0, 0, 1, 2, 0])
c3 = createMatrix(3, 2, [Ra(1), 2]+[2, 5]+[6, 7])

## for FieldSquareMatrix
d1 = createMatrix(2, 2, [Ra(1), Ra(2)]+[Ra(3), Ra(4)])
d2 = createMatrix(3, 3, [Ra(1), 2, 3]+[4, 5, 6]+[5, 7, 9])
d3 = Matrix(3, 3, \
[Ra(1), Ra(2), Ra(3)]+[Ra(0), Ra(5), Ra(-2)]+[7, 1, 9])
d4 = createMatrix(6, 6, \
[Ra(4), 2, 5, 0, 2, 1]+[5, 1, 2, 5, 1, 1]+[90, 7, 54, 8, 4, 6]+\
[7, 5, 0, 8, 2, 5]+[8, 2, 6, 5, -4, 2]+[4, 1, 5, 6, 3, 1])
d5 = createMatrix(4, 4, \
[Ra(2), -1, 0, 0]+[-1, 2, -1, 0]+[0, -1, 2, -1]+[0, 0, -1, 2])
d6 = createMatrix(4, 4, \
[Ra(1), 2, 3, 4]+[2, 3, 4, 5]+[3, 4, 5, 6]+[4, 5, 6, 7])
d7 = Matrix(3, 3, \
[Ra(1, 2), Ra(2, 3), Ra(1, 5)]+[Ra(3, 2), Ra(1, 3), Ra(2, 5)]+[Ra(-1, 2), Ra(4, 3), Ra(3, 5)])

## other objects
v1 = vector.Vector([1, 4])
v2 = vector.Vector([8])
v3 = vector.Vector([0, 0, 1])

class MatrixTest(unittest.TestCase):
    def testInit(self):
        lst_lst = Matrix(3, 2, [[21, -12], [1, -1], [0, 0]])
        self.assertEqual(a4, lst_lst)
        lst_tuple = Matrix(3, 2, [(21, 1, 0), (-12,  -1, 0)])
        self.assertEqual(a4, lst_tuple)
        lst_vect = Matrix(3, 2, [vector.Vector([21, 1, 0]), vector.Vector([-12,  -1, 0])])
        self.assertEqual(a4, lst_vect)

    def testGetitem(self):
        self.assertEqual(2, a1[1, 2])
        self.assertEqual(-2, b2[2, 2])
        self.assertRaises(IndexError, a1.__getitem__, "wrong")
        self.assertEqual(vector.Vector([21, 1, 0]), a4[1])

    def testEqual(self):
        self.assertTrue(a1 == Matrix(1, 2, [3, 2]))
        self.assertTrue(isinstance(a1 == a1, bool))

    def testNonZero(self):
        self.assertTrue(not zeroMatrix(2, 3))

    def testContains(self):
        self.assertTrue(5 in a2)

    def testCall(self):
        call = createMatrix(1, 2, [13, 4])
        self.assertEqual(call, a5(2))

    def testMap(self):
        pow_two = createMatrix(1, 2, [9, 4])
        self.assertEqual(pow_two, a1.map(lambda n : n ** 2))

    def testReduce(self):
        self.assertEqual(-2, a3.reduce(min))

    def testGetRow(self):
        row1 = vector.Vector([3, -2])
        self.assertEqual(row1, a3.getRow(2))
        row2 = vector.Vector([1, 2])
        self.assertEqual(row2, b1.getRow(1))

    def testGetColumn(self):
        col1 = vector.Vector([-12, -1, 0])
        self.assertEqual(col1, a4.getColumn(2))
        col2 = vector.Vector([1, 3])
        self.assertEqual(col2, b1.getColumn(1))

    def testTranspose(self):
        trans = createMatrix(2, 3, [7, 3, 0]+[8, -2, 10])
        self.assertEqual(trans, a3.transpose())

    def testGetBlock(self):
        block = Matrix(2, 3, [4, 6, 5, 6, 8, 9])
        self.assertEqual(block, b5.getBlock(2, 1, 2, 3))

    def testSubMatrix(self):
        sub1 = createMatrix(2, 1, [-12, 0])
        self.assertEqual(sub1, a4.subMatrix(2, 1))
        sub2 = createMatrix(2, 2, [4, 5, 6, 9])
        self.assertEqual(sub2, b5.subMatrix([2, 3], [1, 3]))


class SquareMatrixTest(unittest.TestCase):
    def testIsUpperTriangularMatrix(self):
        UT = createMatrix(4, 4, \
           [1, 2, 3, 4]+[0, 5, 6, 7]+[0, 0, 8, 9]+[0, 0, 0, 1])
        notUT = createMatrix(4, 4, \
           [1, 2, 3, 4]+[0, 5, 6, 7]+[0, 0, 8, 9]+[0, 0, 1, 1])
        assert UT.isUpperTriangularMatrix()
        assert not notUT.isUpperTriangularMatrix()

    def testIsLowerTriangularMatrix(self):
        LT = createMatrix(4, 4, \
           [1, 0, 0, 0]+[2, 3, 0, 0]+[4, 5, 6, 0]+[7, 8, 9, 10])
        notLT = createMatrix(4, 4, \
           [1, 0, 0, 0]+[2, 3, 1, 0]+[4, 5, 6, 0]+[7, 8, 9, 10])
        assert LT.isLowerTriangularMatrix()
        assert not notLT.isLowerTriangularMatrix()

    def testIsDiagonalMatrix(self):
        diag = createMatrix(2, 2, [-3, 0, 0, 5])
        assert diag.isDiagonalMatrix()

    def testIsScalarMatrix(self):
        scaler = createMatrix(2, 2, [10, 0, 0, 10])
        assert scaler.isScalarMatrix()

    def testIsSymmetricMatrix(self):
        symmetric = createMatrix(2, 2, [2, 3, 3, 5])
        assert symmetric.isSymmetricMatrix()

class RingMatrixTest(unittest.TestCase):
    def testAdd(self):
        sum1 = createMatrix(1, 2, [8, -4])
        self.assertEqual(sum1, a1 + a2)
        sum2 = createMatrix(2, 2, [1, 1, 4, 2])
        self.assertEqual(sum2, b1 + b2)

    def testSub(self):
        sub1 = createMatrix(1, 2, [-2, 8])
        self.assertEqual(sub1, a1 - a2)
        sub2 = createMatrix(2, 2, [1, 3, 2, 6])
        self.assertEqual(sub2, b1 - b2)

    def testMul(self):
        mul1 = createMatrix(1, 2, [2, -7])
        self.assertEqual(mul1, a1 * b2)
        mul2 = createMatrix(3, 2, [-15, -6]+[-2, -2]+[0, 0])
        self.assertEqual(mul2, a4 * b1)
        mul3 = createMatrix(3, 2, [1, -1]+[109, -64]+[156, -93])
        self.assertEqual(mul3, b3 * a4)

    def testScalarMul(self):
        mul = createMatrix(1, 2, [15, 10])
        self.assertEqual(mul, 5 * a1)

    def testVectorMul(self):
        mul = vector.Vector([9, 19])
        self.assertEqual(mul, b1 * v1)

    def testMod(self):
        mod1 = createMatrix(3, 2, [1, 2]+[0, 1]+[0, 1])
        self.assertEqual(mod1, a3 % 3)

    def testNeg(self):
        neg = createMatrix(2, 2, [0, 1, -1, 2])
        self.assertEqual(neg, -b2)

    def testHermiteNormalForm(self):
        already = createMatrix(4, 3, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1])
        h = already.hermiteNormalForm()
        self.assertEqual(h, already)
        
        lessrank = createMatrix(2, 3, [1, 0, 0, 0, 1, 0])
        h = lessrank.hermiteNormalForm()
        self.assertEqual(h.row, lessrank.row)
        self.assertEqual(h.column, lessrank.column)
        zerovec = vector.Vector([0, 0])
        self.assertEqual(zerovec, h.getColumn(1))
        
        square = createMatrix(3, 3, [1, 0, 0, 0, 1, 1, 0, 1, 1])
        h = square.hermiteNormalForm()
        self.assertEqual(h.row, square.row)
        self.assertEqual(h.column, square.column)
        hermite = createMatrix(3, 3, [0, 1, 0, 0 ,0, 1, 0, 0, 1])
        self.assertEqual(hermite, h)

    def testExtHermiteNormalForm(self):
        already = createMatrix(4, 3, [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1])
        U_1, h_1 = already.exthermiteNormalForm()
        self.assertEqual(h_1, already)
        self.assertEqual(already * U_1, h_1)

        lessrank = createMatrix(2, 3, [1, 0, 0, 0, 1, 0])
        U_2, h_2 = lessrank.exthermiteNormalForm()
        self.assertEqual(h_2.row, lessrank.row)
        self.assertEqual(h_2.column, lessrank.column)
        self.assertEqual(lessrank * U_2, h_2)

    def testKernelAsModule(self):
        ker_1 = a1.kernelAsModule()
        self.assertEqual(a1 * ker_1[1], vector.Vector([0]))

        #zero test
        ker_2 = b1.kernelAsModule()
        self.assertEqual(ker_2, None)

class RingSquareMatrixTest(unittest.TestCase):

    def testPow(self):
        pow1 = createMatrix(2, 2, [7, 10, 15, 22])
        self.assertEqual(pow1, b1 ** 2)
        pow2 = createMatrix(2, 2, [1, 0, 0, 1])
        self.assertEqual(pow2, b2 ** 0)

    def testIsOrthogonalMatrix(self):
        orthogonal = createMatrix(2, 2, [Ra(3, 5), Ra(4, 5), Ra(-4, 5), Ra(3, 5)])
        assert orthogonal.isOrthogonalMatrix()

    def testIsAlternatingMatrix(self):
        alternate1 = createMatrix(2, 2, [0, 2, -2, 0])
        assert alternate1.isAlternatingMatrix()
        alternate2 = createMatrix(2, [1, 2, -2, 0])
        assert not alternate2.isAntisymmetricMatrix()

    def testIsSingular(self):
        assert b6.isSingular()

    def testTrace(self):
        self.assertEqual(15, b4.trace())

    def testDeterminant(self):
        self.assertEqual(-2, b1.determinant())
        #sf.bug #1914349
        self.assertTrue(isinstance(b3.determinant(), int))
        self.assertEqual(36, b3.determinant())

    def testCofactor(self):
        self.assertEqual(-6, b5.cofactor(1, 2))

    def testCommutator(self):
        commutator = createMatrix(2, 2, [5, -1, 9, -5])
        self.assertEqual(commutator, b1.commutator(b2))

    def testCharacteristicMatrix(self):
        charMat = createMatrix(2, 2, \
        [Poly({0:-1,1:1}, Int), Poly({0:-2}, Int)]+[Poly({0:-3}, Int), Poly({0:-4,1:1}, Int)])
        self.assertEqual(charMat, b1.characteristicMatrix())

    def testCharacteristicPolynomial(self):
        assert d1.characteristicPolynomial() == d1.characteristicMatrix().determinant()

    def testAdjugateMatrix(self):
        adjugate = createMatrix(3, 3, [47, -15, -19, -14, -12, 2, -35, 13, 5])
        self.assertEqual(adjugate, b4.adjugateMatrix())
        assert d1 * d1.adjugateMatrix() == d1.determinant() * unitMatrix(d1.row)

    def testCofactorMatrix(self):
        cofact = d5.cofactorMatrix()
        self.assertEqual(d5.cofactor(2, 3), cofact[2, 3])

    def testSmithNormalForm(self):
        self.assertEqual([12, 1, 1], b5.smithNormalForm())
        self.assertRaises(ValueError, b6.smithNormalForm)
        self.assertEqual([1, 1, 1], b7.smithNormalForm())
        self.assertEqual([9, 3, 1], b8.smithNormalForm())

    def testExtSmithNormalForm(self):
        smith1 = Matrix(3, 3, [12, 0, 0, 0, 1, 0, 0, 0, 1])
        U_1, V_1, M_1 = b5.extsmithNormalForm()
        self.assertEqual(smith1, M_1)
        self.assertEqual(M_1, U_1 * b5 * V_1)
        smith2 = Matrix(3, 3, [9, 0, 0, 0, 3, 0, 0, 0, 1])
        U_2, V_2, M_2 = b8.extsmithNormalForm()
        self.assertEqual(smith2, M_2)
        self.assertEqual(M_2, U_2 * b8 * V_2)

class FieldMatrixTest(unittest.TestCase):
    def testDiv(self):
        div = createMatrix(1, 2, [1, Ra(2, 3)])
        self.assertEqual(div, c1 / 3)

    def testKernel(self):
        ker = c2.kernel()
        self.assertTrue(not c2 * ker)

    def testImage(self):
        img = createMatrix(4,3,[1,2,-1]+[5,12,-2]+[1,3,-1]+[1,2,0])
        self.assertEqual(img, c2.image())

    def testRank(self):
        self.assertEqual(3, c2.rank())
        self.assertEqual(3, d3.rank())

    def testInverseImage(self):
        self.assertEqual(d6, d5 * d5.inverseImage(d6))
        self.assertRaises(NoInverseImage, d2.inverseImage, unitMatrix(3))

    def testSolve(self):
        for i in range(1, d6.column+1):
            self.assertEqual(d6[i], d5 * d5.solve(d6[i])[0])
        sol1 = c1.solve(v2)
        for i in range(len(sol1[1])):
            self.assertEqual(v2, c1 * (sol1[0]+sol1[1][i]))
        self.assertRaises(NoInverseImage, c3.solve, v3)

    def testColumnEchelonForm(self):
        echelon = createMatrix(4, 5,\
        [Ra(0), 0, 1, 0, 0]+[0, 0, 0, 2, 3]+[0, 0, 0, 1, 0]+[0, 0, 0, 0, 1])
        self.assertEqual(echelon, c2.columnEchelonForm())

class FieldSquareMatrixTest(unittest.TestCase):
    def testPow(self):
        pow3 = createMatrix(2, 2, [Ra(11, 2), Ra(-5, 2), Ra(-15, 4), Ra(7, 4)])
        self.assertEqual(pow3, d1 ** (-2))

    def testTriangulate(self):
        triangle = createMatrix(3, 3, \
        [Ra(1, 1), 2, 3]+[0, 5, -2]+[0, 0, Ra(-86, 5)])
        self.assertEqual(triangle, d3.triangulate())

    def testDeterminant(self):
        self.assertEqual(Ra(-7, 15), d7.determinant())

    def testInverse(self):
        cinverse = createMatrix(3, 3)
        cinverse.set([Ra(-47, 86), Ra(15, 86), Ra(19, 86)]+\
        [Ra(7, 43), Ra(6, 43), Ra(-1, 43)]+[Ra(35, 86), Ra(-13, 86), Ra(-5, 86)])
        self.assertEqual(cinverse, d3.inverse())
        self.assertRaises(NoInverse, d2.inverse)
        self.assertEqual(d3.inverse() * c3, d3.inverse(c3))

    def testInverseNoChange(self):
        # sf bug#1849220
        M1 = SquareMatrix(2, 2, [Ra(1, 2), Ra(1, 2), Ra(1, 1), Ra(-3, 2)])
        M1.inverse()
        M2 = SquareMatrix(2, 2, [Ra(1, 2), Ra(1, 2), Ra(1, 1), Ra(-3, 2)])
        self.assertEqual(M2, M1)

    def testHessenbergForm(self):
        pass

    def testLUDecomposition(self):
        L, U = d4.LUDecomposition()
        assert L * U == d4
        assert L.isLowerTriangularMatrix()
        assert U.isUpperTriangularMatrix()


class MatrixRingTest (unittest.TestCase):
    def setUp(self):
        self.m2z = MatrixRing.getInstance(2, Int)

    def testZero(self):
        z = self.m2z.zero
        self.assertEqual(0, z[1, 1])
        self.assertEqual(0, z[1, 2])
        self.assertEqual(0, z[2, 1])
        self.assertEqual(0, z[2, 2])

    def testOne(self):
        o = self.m2z.one
        self.assertEqual(1, o[1, 1])
        self.assertEqual(0, o[1, 2])
        self.assertEqual(0, o[2, 1])
        self.assertEqual(1, o[2, 2])

    def testUnitMatrix(self):
        """
        unitMatrix() is an alias of one.
        """
        self.assertEqual(self.m2z.one, self.m2z.unitMatrix())

    def testRingAPI(self):
        m3z = MatrixRing.getInstance(3, Int)
        m2q = MatrixRing.getInstance(2, rational.theRationalField)
        # issubring
        self.assertFalse(self.m2z.issubring(Int))
        self.assertTrue(self.m2z.issubring(self.m2z))
        self.assertTrue(self.m2z.issubring(m2q))
        self.assertFalse(self.m2z.issubring(m3z))
        # issuperring
        self.assertFalse(self.m2z.issuperring(Int))
        self.assertTrue(self.m2z.issuperring(self.m2z))
        self.assertFalse(self.m2z.issuperring(m2q))
        self.assertFalse(self.m2z.issuperring(m3z))
        # getCommonSuperring
        self.assertRaises(TypeError, self.m2z.getCommonSuperring, Int)


class SubspaceTest(unittest.TestCase):
    def testSupplementBasis(self):
        ba = Subspace(3, 2, [1, 2, 3, 4, 5, 7])
        supbase = createMatrix(3, 3, [1, 2, 0, 3, 4, 0, 5, 7, 1])
        self.assertEqual(supbase, ba.supplementBasis())

    def testSumOfSubspaces(self):
        unit1 = Subspace(3, 1, [1, 0, 0])
        unit2 = Subspace(3, 2, [0, 0]+[1, 0]+[0, 1])
        self.assertEqual(unitMatrix(3), unit1.sumOfSubspaces(unit2))

    def testIntersectionOfSubspace(self):
        unit1 = Subspace(3, 2, [1, 0]+[0, 1]+[0, 0])
        unit2 = unitMatrix(3)
        unit2.toSubspace()
        intersect = Subspace(3, 2, [-1, 0]+[0, -1]+[0, 0])
        self.assertEqual(intersect, unit1.intersectionOfSubspaces(unit2))


class FunctionTest(unittest.TestCase):
    def testCreateMatrix(self):
        Q = rational.theRationalField
        mat1 = createMatrix(2, 3, [[2,3,4], [5,6,7]])
        self.assertEqual(mat1.coeff_ring, Int)
        mat2 = createMatrix(2, 3, [[2,3,4], [5,6,7]], Q)
        self.assertEqual(mat2.coeff_ring, Q)
        mat3 = createMatrix(3, [(1, 2, 3), (4, 5, 6), (7, 8, 9)], Q)
        self.assertTrue(mat3.row == mat3.column)
        self.assertTrue(mat3.__class__, FieldSquareMatrix)
        mat4 = createMatrix(2, [vector.Vector([1, 4]), vector.Vector([6, 8])])
        self.assertEqual(mat4.coeff_ring, Int)
        mat5 = createMatrix(5, 6, Int)
        self.assertTrue(mat5 == 0)
        mat6 = createMatrix(1, 4)
        self.assertTrue(mat6 == 0)
        mat7 = createMatrix(3, Q)
        self.assertTrue(mat7.row == mat7.column)
        self.assertTrue(mat7 == 0)
        self.assertEqual(mat7.coeff_ring, Q)
        mat8 = createMatrix(7)
        self.assertTrue(mat8 == 0)


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
