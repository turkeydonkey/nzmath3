from nzmath import *
import math

def check_zero_poly( coefficients ):
    """
    This function checks whether all elements of coefficients equal zero or not.
    If all elements of coefficients equal zero , this function returns True .
    Else this function returns False.
    """
    for i in coefficients:
        if i != 0:
            return False
    return True

def arrange_coefficients( coefficients ):
    """
    This function arranges coefficient.
    For example, [1,2,0,3,0] => [1,2,0,3].
    """
    if check_zero_poly( coefficients ):
        return [ 0 ]
    while 1:
        if coefficients[ -1 ] == 0:
            coefficients = coefficients[ : len( coefficients ) - 1 ]
        else:
            break
    return coefficients

class array_poly():
    """
    Polynomial with integer number coefficients.
    Coefficients has to be a initializer for list.
    """

    def __init__( self , coefficients = [ 0 ] ):
        """
        Initialize the polynomial.
        coefficients: initializer for polynomial coefficients
        """
        self.coefficients = arrange_coefficients( coefficients )
        self.degree = len( self.coefficients ) - 1

    def coefficients_to_dict( self ):
        """
        Return coefficients as dict.
        """
        if self.coefficients == [ 0 ]:
            return { 0 : 0 }
        dict_coefficients = {}
        for i in range( self.degree + 1 ):
            if self.coefficients[ i ] != 0:
                dict_coefficients.update( { i : self.coefficients[ i ] } )
        return dict_coefficients

    def __repr__( self ):
        poly_repr = self.coefficients_to_dict()
        return "polynomial: %s" % poly_repr

    def __str__( self ):
        poly_str = self.coefficients_to_dict()
        return "polynomial: %s" % poly_str

    def __add__( self , other ):
        """
        self + other
        """
        add = []
        deg1 = self.degree
        deg2 = other.degree
        if deg1 >= deg2:
            long_coefficients = self.coefficients[ : ]
            short_coefficients = other.coefficients[ : ]
            deg = deg2 + 1
        else:
            long_coefficients = other.coefficients[ : ]
            short_coefficients = self.coefficients[ : ]
            deg = deg1 + 1
        for i in range( deg ):
            add.append( long_coefficients[ i ] + short_coefficients[ i ] )
        add += long_coefficients[ deg : ]
        return array_poly( add )

    def __sub__( self , other ):
        """
        self - other
        """
        sub = []
        deg1 = self.degree
        deg2 = other.degree
        if deg1 >= deg2:
            long_coefficients = self.coefficients[ : ]
            short_coefficients = other.coefficients[ : ]
            deg = deg2 + 1
        else:
            long_coefficients = other.coefficients[ : ]
            short_coefficients = self.coefficients[ : ]
            deg = deg1 + 1
        for i in range( deg ):
            sub.append( long_coefficients[ i ] - short_coefficients[ i ] )
        sub += long_coefficients[ deg : ]
        return array_poly( sub )

    def scalar_mul( self , scalar ):
        """
        Return the result of scalar multiplicaton.
        """
        scalar_mul = [ i * scalar for i in self.coefficients ]
        return array_poly( scalar_mul )

    def upshift_degree( self , slide ):
        """
        Return the polynomial obtained by shifting upward all terms
        with degrees of 'slide'.
        """
        if slide == 0:
            return array_poly( self.coefficients[ : ] )
        up_degree = [ ]
        for i in range( slide ):
            up_degree.append( 0 )
        return array_poly( up_degree + self.coefficients[ : ] )

    def downshift_degree( self , slide ):
        """
        Return the polynomial obtained by shifting downward all terms
        with degrees of 'slide'.
        """
        if slide == 0:
            return array_poly( self.coefficients[ : ] )
        elif slide > self.degree:
            return array_poly(  )
        down_degree= self.coefficients[ slide : ]
        return array_poly( down_degree )

    def __eq__( self , other ):
        """
        self == other
        """
        self_dict_coefficients = self.coefficients_to_dict()
        other_dict_coefficients = other.coefficients_to_dict()
        return self_dict_coefficients == other_dict_coefficients
    
    def __ne__( self , other ):
        """
        self != other
        """
        self_dict_coefficients = self.coefficients_to_dict()
        other_dict_coefficients = other.coefficients_to_dict()
        return self_dict_coefficients == other_dict_coefficients

    def __mul__( self , other ):
        """
        self * other
        """
        total = [ ]
        for i in range( self.degree + other.degree + 1 ):
            total.append( 0 )
        for i in range( self.degree + 1 ):
            for j in range( other.degree + 1 ):
                total[ i + j ] += self.coefficients[ i ] * other.coefficients[ j ]
        return array_poly( total )

    def power( self ):
        """
        self * self
        """
        total = [ ]
        for i in range( self.degree + self.degree + 1 ):
            total.append( 0 )
        for i in range( self.degree + 1 ):
            for j in range( i , self.degree + 1 ):
                if i == j:
                    total[ i + j ] += self.coefficients[ i ] * self.coefficients[ j ]
                else:
                    total[ i + j ] += ( ( self.coefficients[ i ] * self.coefficients[ j ] ) << 1 )
        return array_poly( total )

    def split_at( self , split_point ):
        """
        Return tuple of two polynomials, which are splitted at the
        given degree.  The term of the given degree, if exists,
        belongs to the lower degree polynomial.
        """
        split = self.coefficients[ : ]
        if split_point == 0:
            return ( array_poly(  ) , array_poly( split ) )
        elif split_point >= self.degree:
            return ( array_poly( split ) , array_poly(  ) )
        split1 = split[ : split_point + 1 ]
        split2 = split[ : ]
        for i in range( split_point + 1 ):
            split2[ i ] = 0
        return ( array_poly( split1 ) , array_poly( split2 ) )

    def FFT_mul( self , other ):
        """
        self * other by Fast Fourier Transform.
        """
        coefficients1 = [ abs(i) for i in self.coefficients ]
        coefficients2 = [ abs(i) for i in other.coefficients ]
        bound1 = max( coefficients1 )
        bound2 = max( coefficients2 )
        bound = bound1 * bound2 * ( max( self.degree , other.degree ) + 1 ) 
        bound = int( math.ceil( math.log( bound , 2 ) ) )
        bound = 1 << bound
        if bound < ( self.degree + other.degree + 1 ):
            bound = self.degree + other.degree + 1
            bound = int( math.ceil( math.log( bound , 2 ) ) )
            bound = 1 << bound
        fft1 = array_poly( self.coefficients[ : ] )
        fft2 = array_poly( other.coefficients[ : ] )
        fft_mul1 = FFT( fft1 , bound )
        fft_mul2 = FFT( fft2 , bound )
        fft_mul = [ ]
        for i in range( bound ):
            fft_mul.append( fft_mul1[ i ] * fft_mul2[ i ] )
        print(fft_mul)
        total = reverse_FFT( fft_mul , bound )
        print(total)
        return array_poly( total )


class array_poly_mod(array_poly):
    """
    Polynomial with modulo n coefficients , n is a nutural number.
    Coefficients has to be a initializer for list.
    """

    def __init__( self , coefficients , mod ):
        """
        Initialize the polynomial.
        coefficients: initializer for polynomial coefficients
        mod: initializer for coefficients modulo mod
        """
        if mod <= 0:
            raise ValueError(" Please input a natural number in 'mod'. ")
        mod_coefficients = [ i % mod for i in coefficients ]
        array_poly.__init__( self , mod_coefficients )
        self.mod = mod

    def __repr__( self ):
        poly_repr = self.coefficients_to_dict()
        return "polynomial_mod(%d): %s" % ( self.mod , poly_repr )

    def __str__( self ):
        poly_str = self.coefficients_to_dict()
        return "polynomial_mod(%d): %s" % ( self.mod , poly_repr )

    def __add__( self , other ):
        """
        self + other
        """
        if self.mod != other.mod:
            raise ValueError("  ")
        add = array_poly.__add__( self , other )
        return array_poly_mod(add.coefficients,self.mod)

    def __sub__( self , other ):
        """
        self - other
        """
        if self.mod != other.mod:
            raise ValueError("  ")
        sub = array_poly.__sub__( self , other )
        return array_poly_mod( sub.coefficients , self.mod )

    def scalar_mul( self , scalar ):
        """
        Return the result of scalar multiplicaton.
        """
        scalar_mul = array_poly.scalar_mul( self , scalar )
        return array_poly_mod( scalar_mul.coefficients,self.mod )

    def upshift_degree( self , slide ):
        """
        Return the polynomial obtained by shifting upward all terms
        with degrees of 'slide'.
        """
        up_degree = array_poly.upshift_degree( self , slide )
        return array_poly_mod( up_degree.coefficients , self.mod )

    def downshift_degree( self , slide ):
        """
        Return the polynomial obtained by shifting downward all terms
        with degrees of 'slide'.
        """
        down_degree = array_poly.downshift_degree( self , slide )
        return array_poly_mod( down_degree.coefficients , self.mod )

    def __eq__( self , other ):
        """
        self == other
        """
        if self.mod != other.mod:
            raise ValueError("  ")
        eq = array_poly.__eq__( self , other )
        return eq
    
    def __ne__( self , other ):
        """
        self != other
        """
        if self.mod != other.mod:
            raise ValueError("  ")
        ne = array_poly.__ne__( self , other )
        return ne

    def __mul__( self , other ):
        """
        self * other
        """
        if self.mod != other.mod:
            raise ValueError("  ")
        total = [ ]
        for i in range( self.degree + other.degree + 1 ):
            total.append( 0 )
        for i in range( self.degree + 1 ):
            for j in range( other.degree + 1 ):
                total[ i + j ] = ( total[ i + j ] + self.coefficients[ i ] * other.coefficients[ j ] ) % self.mod
        return array_poly_mod( total , self.mod )

    def power( self ):
        """
        self * self
        """
        total = [ ]
        for i in range( self.degree + self.degree + 1 ):
            total.append( 0 )
        for i in range( self.degree + 1 ):
            for j in range( i , self.degree + 1 ):
                if i == j:
                    total[ i + j ] = ( total[ i + j ] + self.coefficients[ i ] * self.coefficients[ j ] ) % self.mod
                else:
                    total[ i + j ] = (total[ i + j ] + ( ( self.coefficients[ i ] * self.coefficients[ j ] ) << 1 )) % self.mod
        return array_poly_mod( total , self.mod )

    def split_at( self , split_point ):
        """
        Return tuple of two polynomials, which are splitted at the
        given degree.  The term of the given degree, if exists,
        belongs to the lower degree polynomial.
        """
        if split_point == 0:
            return ( array_poly_mod( [0] , self.mod ) , array_poly_mod( self.coefficients , self.mod ) )
        elif split_point >= self.degree:
            return ( array_poly_mod( self.coefficients , self.mod ) , array_poly_mod( [0] , self.mod ) )
        split = array_poly.split_at( self , split_point )
        split1 = split[ 0 ].coefficients
        split2 = split[ 1 ].coefficients
        return ( array_poly_mod( split1 , self.mod ) , array_poly_mod( split2 , self.mod ) )

    def FFT_mul( self , other ):
        """
        self * other by Fast Fourier Transform.
        """
        if self.mod != other.mod:
            raise ValueError("  ")
        bound1 = max( self.coefficients )
        bound2 = max( other.coefficients )
        bound = bound1 * bound2 * ( max( self.degree , other.degree ) + 1 ) 
        bound = int( math.ceil( math.log( bound , 2 ) ) )
        bound = 1 << bound
        if bound < ( self.degree + other.degree + 1 ):
            bound = self.degree + other.degree + 1
            bound = int( math.ceil( math.log( bound , 2 ) ) )
            bound = 1 << bound
        fft1 = array_poly_mod( self.coefficients[ : ] , self.mod )
        fft2 = array_poly_mod( other.coefficients[ : ] , other.mod )
        fft_mul1 = FFT( fft1 , bound )
        fft_mul2 = FFT( fft2 , bound )
        fft_mul = [ ]
        for i in range( bound ):
            fft_mul.append( fft_mul1[ i ] * fft_mul2[ i ] )
        total = reverse_FFT( fft_mul , bound )
        return array_poly_mod( total , self.mod )

"""
Some functions for FFT( Fast Fourier Transform ).
"""
def min_abs_mod(a,b):
    """
    This function returns absolute minimum modulo of a over b.
    """
    if a>=0:
        return a-b*int((a+a+b)/(b+b))
    a=-a
    return -(a-b*int((a+a+b)/(b+b)))

def bit_reverse( n , bound ):
    """
    This function returns the result reversed bit of n.
    bound: number of significant figures of bit.
    """
    bit = [ ]
    while n > 0:
        if n & 1:
            bit.append( 1 )
        else:
            bit.append( 0 )
        n = n >> 1
    bound_bitlen = int( math.ceil( math.log( bound , 2 ) ) )
    if bound_bitlen > len( bit ):
        for i in range( bound_bitlen - len( bit ) ):
            bit.append( 0 )
    bit.reverse()
    total = 0
    count = 0
    for i in bit:
        if i != 0:
            total = total + ( 1 << count )
        count += 1
    return total
        

def perfect_shuffle( List ):
    """
    This function returns list arranged by divide-and-conquer method.
    """
    length = len( List )
    shuffle = [ ]
    for i in range( length ):
        shuffle.append( 0 )
    for i in range( length ):
        rebit = bit_reverse( i , length )
        shuffle[ rebit ] = List[ i ]
    return shuffle

def FFT( f , bound ):
    """
    Fast Fourier Transform.
    This function returns the result of valuations of f by fast fourier transform
    against number of bound different values.
    """
    count = 1 << ( bound >> 1 )
    mod = count + 1
    if ( isinstance( f , array_poly) or isinstance( f , array_poly_mod) ):
        coefficients = f.coefficients[ : ]
    else:
        coefficients = f[ : ]
    for i in range( bound - len( coefficients ) ):
        coefficients.append( 0 )
    shuf_coefficients = perfect_shuffle( coefficients )
    shuf_coefficients = [ min_abs_mod( i , mod ) for i in shuf_coefficients ]
    bound_log = int( math.log( bound , 2 ) )
    for i in range( 1 , bound_log + 1 ):
        m = 1 << i
        wm = count
        wm = wm % mod 
        w = 1
        m1 = m >> 1
        for j in range( m1 ):
            for k in range( j , bound , m ):
                m2 = k + m1
                plus = shuf_coefficients[ k ]
                minus = w * shuf_coefficients[ m2 ]
                shuf_coefficients[ k ] = ( plus + minus ) % mod
                shuf_coefficients[ m2 ] = ( plus - minus ) % mod
            w = w * wm
        shuf_coefficietns = [ min_abs_mod( i , mod ) for i in shuf_coefficients ]
        count = arith1.floorsqrt( count )
    return shuf_coefficients

def reverse_FFT( values , bound ):
    """
    Reverse Fast Fourier Tfransform.
    """
    mod = ( 1 << ( bound >> 1 ) ) + 1
    shuf_values = values[ : ]
    reverse_FFT_coeffficients = FFT( shuf_values , bound )
    inverse = arith1.inverse( bound , mod )
    reverse_FFT_coeffficients = [ min_abs_mod( inverse * i , mod ) for i in reverse_FFT_coeffficients ]
    reverse_FFT_coeffficients1 = reverse_FFT_coeffficients[ : 1 ]
    reverse_FFT_coeffficients2 = reverse_FFT_coeffficients[ 1 : ]
    reverse_FFT_coeffficients2.reverse()
    reverse_FFT_coeffficients_total = reverse_FFT_coeffficients1 + reverse_FFT_coeffficients2
    return reverse_FFT_coeffficients_total
