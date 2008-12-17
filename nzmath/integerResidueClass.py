import warnings
import nzmath.gcd as gcd
import nzmath.rational as rational
import nzmath.ring as ring
import nzmath.prime as prime


warnings.warn(DeprecationWarning("use intresidue instead"))


class IntegerResidueClass (ring.CommutativeRingElement):
    """
    A class for integer residue class.
    """
    def __init__(self, representative, modulus):
        ring.CommutativeRingElement.__init__(self)
        if modulus == 0:
            raise ValueError("modulus can not be zero")
        elif modulus < 0:
            modulus = -modulus
        self.m = modulus
        if isinstance(representative, rational.Rational):
            t = IntegerResidueClass(representative.denominator, self.m).inverse().getResidue()
            self.n = representative.numerator * t % self.m
        else:
            self.n = representative % self.m

    def __repr__(self):
        return "IntegerResidueClass(%d, %d)" % (self.n, self.m)

    def __mul__(self, other):
        if isinstance(other, IntegerResidueClass):
            if self.m == other.m:
                return self.__class__(self.n * other.n, self.m)
            if self.m % other.m == 0:
                return IntegerResidueClass(self.n * other.n, other.m)
            elif other.m % self.m == 0:
                return IntegerResidueClass(self.n * other.n, self.m)
            else:
                raise ValueError("incompatible modulus: %d and %d" % (self.m, other.m))
        try:
            return self.__class__(self.n * other, self.m)
        except:
            return NotImplemented

    __rmul__ = __mul__

    def __div__(self, other):
        try:
            return self * other.inverse()
        except AttributeError:
            pass
        try:
            return self * self.__class__(other, self.m).inverse()
        except (ValueError, NotImplementedError):
            return NotImplemented

    __floordiv__ = __truediv__ = __div__

    def __mod__(self, other):
        """
        Return zero if division by other is allowed
        """
        return self - (self // other) * other

    def __divmod__(self, other):
        return (self // other, self % other)

    def __rdiv__(self, other):
        if not other:
            return self.__class__(0, self.m)
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, IntegerResidueClass):
            if self.m == other.m:
                return self.__class__(self.n + other.n, self.m)
            if self.m % other.m == 0:
                return IntegerResidueClass(self.n + other.n, other.m)
            elif other.m % self.m == 0:
                return IntegerResidueClass(self.n + other.n, self.m)
            else:
                raise ValueError("incompatible modulus: %d and %d" % (self.m, other.m))
        try:
            return self.__class__(self.n + other, self.m)
        except:
            return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, IntegerResidueClass):
            if self.m == other.m:
                return self.__class__(self.n - other.n, self.m)
            if self.m % other.m == 0:
                return IntegerResidueClass(self.n - other.n, other.m)
            elif other.m % self.m == 0:
                return IntegerResidueClass(self.n - other.n, self.m)
            else:
                raise ValueError("incompatible modulus: %d and %d" % (self.m, other.m))
        try:
            return self.__class__(self.n - other, self.m)
        except:
            return NotImplemented

    def __rsub__(self, other):
        try:
            return self.__class__(other - self.n, self.m)
        except:
            return NotImplemented

    def __pow__(self, other):
        if other < 0:
            inverse = self.inverse()
            return self.__class__(pow(inverse.n, -other, self.m), self.m)
        elif other == 0:
            return self.__class__(1, self.m)
        else:
            return self.__class__(pow(self.n, other, self.m), self.m)

    def __neg__(self):
        return self.__class__(-self.n, self.m)

    def __pos__(self):
        return self.__class__(+self.n, self.m)

    def __nonzero__(self):
        return bool(self.n)

    def __eq__(self, other):
        if not other and self.n == 0:
            return True
        if isinstance(other, IntegerResidueClass):
            if other.m == self.m and other.n == self.n:
                return True
            else:
                return False
        return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def inverse(self):
        t = gcd.extgcd(self.n, self.m)
        if t[2] != 1:
            raise ValueError("No inverse of %s." % self)
        return self.__class__(t[0], self.m)

    def getModulus(self):
        return self.m

    def getResidue(self):
        return self.n

    def toInteger(self):
        """
        Return the smallest non-negative representative element of the
        residue class.
        """
        return rational.Integer(self.n % self.m)

    def getRing(self):
        return IntegerResidueClassRing.getInstance(self.m)


class IntegerResidueClassRing (ring.CommutativeRing):
    """IntegerResidueClassRing is also known as Z/mZ."""

    _instances = {}

    def __init__(self, modulus):
        """
        The argument modulus m specifies an ideal mZ.
        """
        ring.CommutativeRing.__init__(self)
        self.m = modulus

    def __repr__(self):
        return "IntegerResidueClassRing(%d)" % self.m

    def __str__(self):
        return "Z/%dZ" % self.m

    def __hash__(self):
        return self.m & 0xFFFFFFFF

    def card(self):
        """
        Return the cardinality of the ring.
        """
        return self.m

    @classmethod
    def getInstance(cls, modulus):
        """
        getInstance returns an instance of the class of specified
        modulus.
        """

        if modulus not in cls._instances:
            anInstance = IntegerResidueClassRing(modulus)
            cls._instances[modulus] = anInstance
        return cls._instances[modulus]

    def createElement(self, seed):
        if isinstance(seed, IntegerResidueClass) and seed.m % self.m == 0:
            return IntegerResidueClass(seed.n, self.m)
        try:
            return IntegerResidueClass(seed, self.m)
        except:
            raise ValueError("%s can not be converted to an IntegerResidueClass object." % seed)

    def getCharacteristic(self):
        """
        The characteristic of Z/mZ is m.
        """
        return self.m

    def __contains__(self, elem):
        if isinstance(elem, IntegerResidueClass) and \
           elem.getModulus() == self.m:
            return True
        return False

    def isfield(self):
        """
        isfield returns True if the modulus is prime, False if not.
        Since a finite domain is a field, other ring property tests
        are merely aliases of isfield.
        """
        if None == self.properties.isfield():
            if prime.primeq(self.m):
                self.properties.setIsfield(True)
            else:
                self.properties.setIsdomain(False)
        return self.properties.isfield()

    isdomain = isfield
    isnoetherian = isfield
    isufd = isfield
    ispid = isfield
    iseuclidean = isfield

    def __eq__(self, other):
        if isinstance(other, IntegerResidueClassRing) and self.m == other.m:
            return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def issubring(self, other):
        if self == other:
            return True
        else:
            return False

    def issuperring(self, other):
        if self == other:
            return True
        else:
            return False

    def _getOne(self):
        "getter for one"
        if self._one is None:
            self._one = IntegerResidueClass(1, self.m)
        return self._one

    one = property(_getOne, None, None, "multiplicative unit.")

    def _getZero(self):
        "getter for zero"
        if self._zero is None:
            self._zero = IntegerResidueClass(0, self.m)
        return self._zero

    zero = property(_getZero, None, None, "additive unit.")
