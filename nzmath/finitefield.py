"""

finite fields.

"""
import gcd
import prime
import rational
import ring

class FiniteField (ring.Field):
    def __len__(self):
        "Cardinality of the field"
        raise NotImplementedError

    def __nonzero__(self):
        return True

class FiniteFieldElement (ring.FieldElement):
    pass

import integerResidueClass

class FinitePrimeFieldElement (integerResidueClass.IntegerResidueClass, FiniteFieldElement):
    def __init__(self, representative, modulus):
        if modulus < 0:
            modulus = -modulus
        if prime.primeq(modulus):
            self.m = modulus
        else:
            raise ValueError, "modulus must be a prime."
        if isinstance(representative, rational.Rational):
            t = gcd.extgcd(representative.denominator, self.m)
            if t[2] != 1:
                raise ValueError, "No inverse of %s." % representative
            self.n = (representative.numerator * t[0]) % self.m
        elif isinstance(representative, (int, long)):
            self.n = representative % self.m
        elif isinstance(representative, integerResidueClass.IntegerResidueClass):
            assert representative.m == modulus
            self.n = representative.n
        else:
            raise NotImplementedError, repr(representative)

    def __repr__(self):
        return "FinitePrimeFieldElement(%d, %d)" % (self.n, self.m)

    def __str__(self):
        return "%d in F_%d" % (self.n, self.m)

    def getRing(self):
        return FinitePrimeField(self.m)

class FinitePrimeField (FiniteField):
    """

    FinitePrimeField is also known as F_p or GF(p).

    """
    def __init__(self, characteristic):
        self.char = characteristic
        self.properties = ring.CommutativeRingProperties()
        self.properties.setIsfield(True)

    def getCharacteristic(self):
        """

        Return the characteristic of the field.

        """
        return self.char

    def __eq__(self, other):
        if isinstance(other, FinitePrimeField) and self.char == other.char:
            return True
        return False

    def issubring(self, other):
        """

        Report whether another ring contains the field as a subring.

        """
        if self == other:
            return True
        elif isinstance(other, FiniteField) and other.getCharacteristic() == self.char:
            return True
        return False

    def issuperring(self, other):
        """

        Report whether the field is a superring of another ring.
        Since the field is a prime field, it can be a superring of
        itself only.

        """
        if self == other:
            return True
        return False

    def __contains__(self, elem):
        if isinstance(elem, FinitePrimeFieldElement) and elem.getModulus() == self.char:
            return True
        return False

    def createElement(self, seed):
        return FinitePrimeFieldElement(seed, self.char)

    def __len__(self):
        "Cardinality of the field"
        return self.char

    def __nonzero__(self):
        return True

import arith1
import bigrandom
import polynomial

class FiniteExtendedField (FiniteField):
    """

    FiniteExtendedField is a class for finite field, whose cardinality
    q = p**n with a prime p and n>1. It is usually called F_q or GF(q).

    """
    def __init__(self, characteristic, n_or_modulus):
        """

        FiniteExtendedField(p, n_or_modulus) creates a finite field.
        characteristic must be prime. n_or_modulus can be:
          1) an integer greater than 1, or
          2) a polynomial in a polynomial ring of F_p with degree
             greater than 1.
          3) an ideal of the polynomial ring F_p[#1] with degree
             greater than 1.

        """
        if prime.primeq(characteristic):
            self.char = characteristic
        else:
            raise ValueError, "characteristic must be a prime."
        if isinstance(n_or_modulus, (int,long)):
            if n_or_modulus <= 1:
                raise ValueError, "degree of extension must be > 1."
            self.degree = n_or_modulus
            # randomly chosen irreducible polynomial
            seed = bigrandom.randrange(self.char ** self.degree)
            cand = polynomial.OneVariableDensePolynomial(arith1.expand(seed, self.char), "#1", FinitePrimeField(self.char))
            while not cand.isIrreducible():
                seed = bigrandom.randrange(self.char ** self.degree)
                cand = polynomial.OneVariableDensePolynomial(arith1.expand(seed, self.char), "#1", FinitePrimeField(self.char))
            self.modulus = cand
        elif isinstance(n_or_modulus, polynomial.OneVariablePolynomial):
            if isinstance(n_or_modulus.getCoefficientRing(), FinitePrimeField):
                if n_or_modulus.degree() > 1 and n_or_modulus.isIrreducible():
                    self.degree = n_or_modulus.degree()
                    self.modulus = polynomial.OneVariablePolynomialIdeal(
                        n_or_modulus("#1"),
                        n_or_modulus("#1").getRing())
                else:
                    raise ValueError, "modulus must be of degree greater than 1."
            else:
                raise TypeError, "modulus must be F_p polynomial."
        elif isinstance(n_or_modulus, polynomial.OneVariablePolynomialIdeal):
            if n_or_modulus.ring == polynomial.PolynomialRing(FinitePrimeField(self.characteristic), ["#1"]):
                if n_or_modulus.generators[0].degree() > 1:
                    self.modulus = n_or_modulus
                    self.degree = self.modulus.generators[0].degree()
                else:
                    raise ValueError, "modulus must be of degree greater than 1."
            else:
                raise TypeError, "modulus must be in F_p[#1]"
        else:
            raise TypeError, "degree or modulus must be supplied."

    def getCharacteristic(self):
        """

        Return the characteristic of the field.

        """
        return self.char

    def __len__(self):
        """

        Return the cardinality of the field

        """
        return self.char ** self.degree

    def createElement(self, seed):
        if isinstance(seed, (int, long)):
            expansion = arith1.expand(seed, self.char)
            return FiniteExtendedFieldElement(
                polynomial.OneVariableDensePolynomial(
                expansion, "#1", FinitePrimeField(self.char)),
                self)
        elif isinstance(seed, polynomial.OneVariablePolynomial):
            return FiniteExtendedFieldElement(seed("#1"), self)

class FiniteExtendedFieldElement (FiniteFieldElement):
    """

    FiniteExtendedFieldElement is a class for an element of F_q.

    """
    def __init__(self, representative, field):
        """

        FiniteExtendedFieldElement(representative, field) creates
        an element of the finite extended field.

        The argument representative must be an F_p polynomial.

        Another argument field mut be an instance of
        FiniteExtendedField.

        """
        if isinstance(field, FiniteExtendedField):
            self.field = field
        else:
            raise TypeError, "wrong type argument for field."
        if (isinstance(representative, polynomial.OneVariablePolynomial) and
            isinstance(representative.getCoefficientRing(), FinitePrimeField)):
            self.rep = self.field.modulus.reduce(representative)
        else:
            raise TypeError, "wrong type argument for representative."

    def getRing(self):
        return self.field

    def __add__(self, other):
        assert self.field == other.field
        sum = self.field.modulus.reduce(self.rep + other.rep)
        return self.__class__(sum, self.field)

    def __sub__(self, other):
        assert self.field == other.field
        dif = self.field.modulus.reduce(self.rep - other.rep)
        return self.__class__(dif, self.field)

    def __mul__(self, other):
        assert self.field == other.field
        prod = self.field.modulus.reduce(self.rep * other.rep)
        return self.__class__(prod, self.field)

    def __truediv__(self, other):
        return self * other.inverse()

    __div__ = __truediv__

    def inverse(self):
        if not self:
            raise ZeroDivisionError, "There is no inverse of zero."
        return self ** (len(self.field)-2)

    def __pow__(self, index):
        while index < 0:
            index += self.field.getCharacteristic()
        return self.field.modulus.reduce(self.rep ** index) # slow

    def __eq__(self, other):
        if self.field == other.field:
            if not self.field.modulus.reduce(self.rep - other.rep):
                return True
        return False

    def __ne__(self, other):
        return not (self == other)

    def __nonzero__(self):
        return self.rep.__nonzero__()
