# matrix.py

import rational
import ring

class Matrix:

    def __init__(self, row, column):
        "Matrix(row, column)"
        if (    ( isinstance(row, int) or isinstance(row, long) )
            and ( isinstance(column, int) or isinstance(column, long) )
            and row > 0 and column > 0    ): 
            self.row = row
            self.column = column
            self.compo = []
            for i in range(self.row):
                self.compo.append([0] * self.column)
        else:
            raise ValueError, "Arguments are not integers > 0."

    def __getitem__(self, *arg):
        """M[i,j] : Return (i,j)-component of M. 
        M[i] <==> M.get_column(i)"""
        if isinstance(arg[0], tuple):
            return self.compo[ arg[0][0]-1 ][ arg[0][1]-1 ]
        elif isinstance(arg[0], int) or isinstance(arg[0], long): 
            return self.get_column(arg[0])
        else:
            raise IndexError, self.__getitem__.__doc__

    def __setitem__(self, *arg):
        """M[i,j] = a : Substitute a for (i,j)-component of M.
        M[i] = V <==> M.set_column(i, V)"""
        key = arg[0]
        value = arg[1]
        if isinstance(key, tuple):
            self.compo[key[0]-1][key[1]-1] = value
        elif isinstance(key, int) or isinstance(key, long):
            self.set_column(key, value)
        else:
            raise TypeError, self.__setitem__.__doc__

    def __eq__(self, other):
        if isinstance(other, Matrix):
            if (self.row != other.row) or (self.column != other.column):
                return 0
            for i in range(self.row):
                for j in range(self.column):
                    if self.compo[i][j] != other.compo[i][j]:
                        return 0
            return 1
        elif isinstance(other, int):
            if other == 0:
                for i in range(self.row):
                    for j in range(self.column):
                        if self.compo[i][j] != 0:
                            return 0
                return 1 
        else:
            raise TypeError

    def __add__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise MatrixSizeError

        sum = Matrix(self.row, self.column)

        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                sum[i,j] = self[i,j] + other[i,j]

        return sum

    def __sub__(self, other):
        if (self.row != other.row) or (self.column != other.column): 
            raise MatrixSizeError

        diff = Matrix(self.row, self.column)

        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                diff[i,j] = self[i,j] - other[i,j]

        return diff

    def __mul__(self, other):
        """multiplication with a Matrix or a scalar"""
        if isinstance(other, Matrix):
            if self.column != other.row:
                raise MatrixSizeError
            product = Matrix(self.row, other.column) 
            for i in range(1, self.row+1):
                for j in range(1, other.column+1):
                    for k in range(self.column):
                        product[i,j] += self[i,k] * other[k,j]
            return product 
        else:           # product with a scalar
            product = Matrix(self.row, self.column)
            for i in range(1, self.row+1):
                for j in range(1, self.column+1):
                    product[i,j] = self[i,j] * other
            return product

    def __div__(self, other):
        """division by a scalar"""
        return self * (1 / rational.Rational(other)) 

    def __rmul__(self, other):
        product = Matrix(self.row, self.column)
        for i in range(1, self.row+1):
            for j in range(1, self.column+1):
                product[i,j] = self[i,j] * other
        return product

    def __neg__(self):
        return (-1) * self

    def __pow__(self, other):
        if other in ring.theIntegerRing and other >= 0:
            power = unit_matrix(self.row)
            for i in range(other):
                power *= self
            return power
        elif other in ring.theIntegerRing and other < 0:
            return pow(self.inverse(), abs(other))
        else:
            raise TypeError

    def __repr__(self):
        return_str = ""
        width = [1] * self.column      # width of each column
        for j in range(self.column):
            for i in range(self.row):
                if len(`self.compo[i][j]`) > width[j]:
                    width[j] = len(`self.compo[i][j]`)
        for i in range(self.row):
            for j in range(self.column):
                return_str += "%*s " % (width[j], `self.compo[i][j]`)
            return_str += "\n"
        return return_str[:-1]

    __str__ = __repr__ 


# utility methods ----------------------------------------------------

    def copy(self):
        """Create a copy of the instance."""
        copy = Matrix(self.row, self.column)
        copy.row = self.row
        copy.column = self.column
        for i in range(1, self.column+1):
            copy[i] = self[i]
        return copy

    def set(self, list):
        """set(list) : Substitute list for components"""
        for i in range(self.row):
            for j in range( self.column):
                self.compo[i][j] = list[self.column * i + j]

    def set_row(self, m, arg):
        """set_row(m, new_row) : new_row can be a list or a row vector(Matrix)"""
        if isinstance(arg, list):
            self.compo[m-1] = arg[:]
        elif isinstance(arg, Matrix):
            for i in range(self.column):
                self.compo[m-1][i] = arg.compo[0][i]
        else:
            raise TypeError, self.set_row.__doc__
    
    def set_column(self, n, arg):
        """set_column(n, new_column) : new_column can be a list or a column vector(Matrix)"""
        if isinstance(arg, list):
            for i in range(self.row):
                self.compo[i][n-1] = arg[i]
        elif isinstance(arg, Matrix):
            for j in range(self.row):
                self.compo[j][n-1] = arg.compo[j][0]
        else:
            raise TypeError, self.set_column.__doc__

    def get_row(self, i):
        """get_row(i) : Return i-th row in form of Matrix"""
        row = Matrix(1, self.column)
        for k in range(row.column):
            row.compo[0][k] = self.compo[i-1][k]
        return row

    def get_column(self, j):
        """get_column(j) : Return j-th column in form of Matrix"""
        column = Matrix(self.row, 1)
        for k in range(self.row):
            column.compo[k][0] = self.compo[k][j-1]
        return column

    def swap_row(self, m1, m2):
        """swap_row(m1, m2) : Swap self's m1-th row and m2-th row."""
        tmp = self.compo[m1-1][:]
        self.compo[m1-1] = self.compo[m2-1][:]
        self.compo[m2-1] = tmp[:]

    def swap_column(self, n1, n2):
        """swap_column(n1, n2) : Swap self's n1-th column and n2-th column."""
        tmp = self[n1]
        self.set_column(n1, self[n2])
        self.set_column(n2, tmp)

    def insert_row(self, i, arg):
        """insert_row(i, new_row) : new_row can be a list or a Matrix""" 
        if isinstance(arg, list):
            new_row = arg
        elif isinstance(arg, Matrix):
            new_row = arg.compo[0][:]
        else:
            raise TypeError
        self.row += 1
        self.compo.insert(i-1, new_row)

    def insert_column(self, j, arg):
        """insert_column(j, arg) : new_column can be a list or a Matrix"""
        if isinstance(arg, list):
            new_column = arg
        elif isinstance(arg, Matrix):
            new_column = arg[1]
        else:
            raise TypeError
        self.column += 1
        for k in range(self.row):
            self.compo[k].insert(j-1, new_column[k])

    def delete_row(self, i):
        self.row -= 1
        del self.compo[i-1]

    def delete_column(self, j):
        self.column -= 1
        for k in range(self.row):
            del self.compo[k][j-1]

# Mathematical functions ---------------------------------------------

    def transpose(self):
        """Return transposed matrix of self"""
        trans = Matrix(self.column, self.row)
        for i in range(1, trans.row+1):
            for j in range(1, trans.column+1):
                trans[i,j] = self[j,i]
        return trans

    def triangulate(self):
        """Return triangulated matrix of self."""
        triangle = self.copy()
        for i in range(triangle.row):
            if triangle.compo[i][i] == 0:
                for k in range(i+1, triangle.row):
                    if triangle.compo[k][i] != 0:
                        triangle.swap_row(i+1, k+1)
                        for l in range(triangle.column):     # for calculation of determinant
                            triangle.compo[i+1][l] *= -1
                        break        # break the second loop
                else:
                    continue         # the below components are all 0. Back to the first loop
            for k in range(i+1, triangle.row):
                ratio = triangle.compo[k][i] / rational.Rational(triangle.compo[i][i])
                for l in range(i, triangle.column):
                    triangle.compo[k][l] -= rational.Rational(triangle.compo[i][l] * ratio)
            
        return triangle

    def trace(self):
        """Return trace of self."""
        trace = 0
        for i in range(self.row):
            trace += self.compo[i][i]
        return trace

    def determinant(self):
        """Return determinant of self."""
        det = 1
        if self.row != self.column:
            raise MatrixSizeError, "not square matrix"
        triangle = self.triangulate()
        for i in range(self.row):
            det *= triangle.compo[i][i]
        return det

    def submatrix(self, i, j):
        """Return submatrix which deleted i-th row and j-th column from self."""
        sub = self.copy()
        sub.delete_row(i)
        sub.delete_column(j)
        return sub

    def cofactors(self):
        cofactors = Matrix(self.row, self.column)
        for i in range(cofactors.row):
            for j in range(cofactors.column):
                cofactors.compo[j][i] = (-1)**(i+j) * (self.submatrix(i+1, j+1)).determinant()
        return cofactors

    def inverse(self):
        """Return inverse matrix of self,
        or return None if inverse is not exist."""
        det = self.determinant()
        if det == 0:
            return None
        else:
            return self.cofactors() / det 

    def characteristic_polynomial(self):        # using Cohen's Algorithm 2.2.7
        if self.row != self.column:
            raise MatrixSizeError, "not square matrix"
        i = 0
        C = unit_matrix(self.row)
        coeff = [0] * (self.row+1)
        coeff[0] = 1
        for i in range(1, self.row+1):
            C = self * C
            coeff[i] = (-1) * C.trace() / rational.Rational(i, 1)
            C = C + coeff[i] * unit_matrix(self.row)
        return coeff

    def cohens_simplify(self):      # common process of image() and kernel()
        """cohens_simplify is used in image() and kernel()"""
        c = [0] * (self.row + 1)
        d = [-1] * (self.column + 1)
        for k in range(1, self.column+1):
            j = 1
            while j <= self.row:
                if self[j,k] != 0 and c[j] == 0:
                    break
                j = j+1
            else:           # not found j such that m(j,k)!=0 and c[j]==0
                d[k] = 0
                continue
            top = (-1) / rational.Rational(self[j,k])
            self[j,k] = -1
            for s in range(k+1, self.column+1):
                self[j,s] = top * self[j,s] 
            for i in range(1, self.row+1):
                if i == j:
                    continue
                top = self[i,k]
                self[i,k] = 0
                for s in range(k+1, self.column+1):
                    self[i,s] = self[i,s] + top * self[j,s]
            c[j] = k
            d[k] = j
        return (c,d)

    def kernel(self):       # using Cohen's Algorithm 2.3.1
        """Return a Matrix which column vectors are one basis of self's kernel,
        or return None if self's kernel is 0."""
        M = self.copy()
        tmp = M.cohens_simplify()
        c = tmp[0]
        d = tmp[1]
        basis = []
        vector = [0] * (M.column+1)
        for k in range(1, M.column+1):
            if d[k] != 0:
                continue
            for i in range(1, M.column+1):
                if d[i] > 0:
                    vector[i] = M[d[i],k]
                elif i == k:
                    vector[i] = 1
                else:
                    vector[i] = 0
            basis.append(vector[1:])
        if len(basis) == 0:
            return None
        output = Matrix(self.column, len(basis))
        for j in range(1, output.column + 1):
            output.set_column(j, basis[j-1])
        return output

    def image(self):        # using Cohen's Algorithm 2.3.2
        """Return a Matrix which column vectors are one basis of self's image,
        or return None if self's image is 0."""
        M = self.copy()
        tmp = M.cohens_simplify()
        c = tmp[0]
        basis = []
        for j in range(1, M.row+1):
            if c[j] != 0:
                basis.append(self[c[j]])
        output = Matrix(self.row, len(basis))
        for j in range(1, output.column + 1):
            output.set_column(j, basis[j-1])
        return output

    def rank(self):
        """Rerutn self's rank."""
        return len(self.image())

    def inverse_image(self, B):      # using Cohen's Algorithm 2.3.4
        """inverse_image(B) : B can be a list or a column vector(Matrix)
        Return a vector belongs to the inverse image of B,
        or return None if inverse image is not exist."""
        M1 = self.copy()
        M1.insert_column(self.column+1, B)
        V = M1.kernel()
        r = V.column
        for j in range(1, r+1):
            if V[self.column+1, j] != 0:
                break
        else:
            return None
        d = (-1)/rational.Rational(V[self.column+1,j])
        x = []
        for i in range(1, self.column+1):
            x.append(d*V[i,j])
        inverse_image = Matrix(self.column, 1)
        inverse_image.set_column(1, x)
        return inverse_image
        
    # does not work well ???
    def supplement_basis(self):     # using Cohen's Algorithm 2.3.6
        """Return a basis of full space, which including self's column vectors."""
        if self.row < self.column:
            raise MatrixSizeError

        copy = self.copy()
        B = unit_matrix(copy.row)

        for s in range(1,copy.column+1):
            for t in range(s,copy.row+1):
                if copy[t,s] != 0:
                    break
            else:
                raise VectorsNotIndependent
            d = 1 / rational.Rational(copy[t,s])
            if t != s:
                B.set_column(t, B[s])
            B.set_column(s, copy[s])
            print B
            pause()
            for j in range(s+1, copy.column+1):
                tmp = copy[s,j]
                copy[s,j] = copy[t,j]
                copy[t,j] = tmp
                copy[s,j] = d * copy[s,j]
                for i in range(1,copy.row+1):
                    if i != s and i != t:
                        copy[i,j] = copy[i,j] - copy[i,s] * copy[s,j]
        return B

    # does not work well ???
    def hessenberg_form(self):      # using Cohen's Algorithm 2.2.9
        if self.row != self.column:
            raise MatrixSizeError
        H = self.copy()
        for m in range(2, H.row):
            for i in range(m+1, self.row+1):
                if H[i,m-1] != 0:
                    break
            else:
                continue
            if H[m,m-1] != 0:
                i = m
            t = H[i,m-1]
            if i > m:
                for j in range(m-1, H.row+1):
                    tmp = H[i,j]
                    H[i,j] = H[m,j]
                    H[m,j] = tmp
                    tmpvector = H[i]
                    H[i] = H[m]
                    H[m] = tmpvector
            for i in range(m+1,H.row+1):
                if H[i,m-1] != 0:
                    u = H[i,m-1] / rational.Rational(t)
                    for j in range(m,H.row+1):
                        H[i,j] = H[i,j] - u * H[m,j]
                    H.set_column( m, H[m] + u * H[i] )
        return H

    def column_echelon_form(self):  # using Cohen's Algorithm 2.3.11
        """Return a Matrix in column echelon form whose image is equal to the image of self."""
        M = self.copy()
        k = M.column
        i_range = range(1, M.row+1)
        i_range.reverse()
        for i in i_range:
            search_range = range(1, k+1)
            search_range.reverse()
            for j in search_range:
                if M[i,j] != 0:
                    break
            else:
                continue
            d = 1 / rational.Rational(M[i,j])
            for l in range(1, i+1):
                t = d * M[l,j]
                M[l,j] = M[l,k]
                M[l,k] = t
            for j in range(1, M.column+1):
                if j == k:
                    continue
                for l in range(1,i+1):
                    M[l,j] = M[l,j] - M[l,k] * M[i,j]
            k = k-1
        return M 

# the belows are not class methods -----------------------------------
def unit_matrix(size):
    """unit_matrix(n) : Return unit matrix whose size is n * n"""
    unit_matrix = Matrix(size, size)
    for i in range(size):
        unit_matrix.compo[i][i] = 1
    return unit_matrix

def intersection_of_subspaces(M, M_):    # using Cohen's Algorithm 2.3.9
    if M.row != M_.row:
        raise MatrixSizeError
    M1 = Matrix(M.row, M.column + M_.column)
    for j in range(1, M.column+1):
        M1.set_column(j, M[j])
    for j in range(1, M_.column+1):
        M1.set_column(M.column + j, M_[j])
    N = M1.kernel()
    N1 = Matrix(M.column , N.column)    # N.column is dimension of kernel(M1)
    for j in range(1, M.column + 1):
        N1.set_row(j, N.get_row(j))
    M2 = M * N1
    return M2.image()

# define exceptions --------------------------------------------------
class MatrixSizeError(Exception):
    pass

class VectorsNotIndependent(Exception):
    pass

# data for debugging -------------------------------------------------
a=Matrix(5,3)
a.set([0,1,3]+[0,2,2]+[0,0,5]+[0,1,1]+[2,0,0])

b = Matrix(2,2)
b.set([1,2,5,10])

c = Matrix(3,3)
c.set([0,1,1,-1,1,0,2,2,3])

d = Matrix(4,2)
d.set([0,1,0,1]+[2,0,0,3])

e = Matrix(3,2)
e.set([1,0]+[2,1]+[1,1])

f = Matrix(3,2)
f.set([0,1]+[-1,4]+[2,6])

def pause():
    print "--- hit enter key ---"
    raw_input()

if __name__ == '__main__':
    import testMatrix
    runner = testMatrix.unittest.TextTestRunner()
    runner.run(testMatrix.suite())

