import sets
import rational

"""

rational functions and fields of rational functions

"""

class RationalFunctionField:
    """

    The class for rational function fields.

    """
    def __init__(self, field, vars):
        self.coefficientField = field
        if isinstance(vars, str):
            self.vars = sets.Set((vars,))
        else:
            self.vars = sets.Set(vars)

    def __str__(self):
        retval = str(self.coefficientField)
        retval += "("
        for v in self.vars:
            retval += str(v) + ", "
        retval = retval[:-2] + ")"
        return retval


    def __eq__(self, other):
        if not isinstance(other, RationalFunctionField):
            return False
        if self.coefficientField == other.coefficientField and self.vars == other.vars:
            return True
        elif isinstance(self.coefficientField, RationalFunctionField):
            return self.unnest() == other
        elif isinstance(other.coefficientField, RationalFunctionField):
            return self == other.unnest()
        return False

    def __contains__(self, element):
        try:
            if element.getRing().issubring(self):
                return True
        except:
            if rational.isIntegerObject(element) and rational.theIntegerRing.issubring(self):
                return True
        return False

    def getQuotientField(self):
        return self

    def issubring(self, other):
        if isinstance(other, RationalFunctionField) and self.vars.issubset(other.vars):
            return True
        return False

    def issuperring(self, other):
        if isinstance(other, RationalFunctionField) and self.vars.issuperset(other.vars):
            return True
        elif self.coefficientField.issuperring(other):
            return True
        else:
            try:
                if self.issuperring(other.getQuotientField()):
                    return True
            except:
                pass
        return False

    def createElement(self, *seedarg, **seedkwd):
        return RationalFunction(*seedarg, **seedkwd)

    def unnest(self):
        """

        if self is a nested RationalFunctionField i.e. its
        coefficientField is also a RationalFunctionField, then the
        function returns one level unnested RationalFunctionField.

        For example:
        RationalFunctionField(RationalFunctionField(Q, "x"), "y").unnest()
        returns
        RationalFunctionField(Q, sets.Set(["x","y"])).

        """
        return RationalFunctionField(self.coefficientField.coefficientField, self.coefficientField.vars | self.vars)

class RationalFunction:
    """

    The class of rational functions.

    """
    def __init__(self, *arg, **kwd):
        if len(arg) == 1:
            if isinstance(arg[0], RationalFunction):
                self.numerator = arg[0].numerator
                self.denominator = arg[0].denominator
            else:
                self.numerator = arg[0]
                if "denominator" in kwd:
                    self.denominator = kwd["denominator"]
                else:
                    self.denominator = rational.Integer(1)
        elif len(arg) == 2:
            self.numerator = arg[0]
            self.denominator = arg[1]
        elif len(kwd) > 0:
            try:
                self.numerator = kwd["numerator"]
            except:
                raise ValueError, "numerator must be specified."
            try:
                self.denominator = kwd["denominator"]
            except:
                self.denominator = rational.Integer(1)
        else:
            raise ValueError, "numerator must be specified."