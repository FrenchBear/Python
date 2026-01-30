# vector_op.py
# Play with operators
# 2021-05-09    PV

# A class can reference itself without using a string

import functools
import math
import operator
from array import array
import numbers
import itertools


class Vector:
    # float.  We don't allow Vectors with complex values.  All other numerical types are converted to float.
    typecode = 'd'
    shortcuts = 'xyzt'

    def __init__(self, *values) -> None:
        if len(values) > 1:
            # Vector(1, 2)
            self._coords = array(self.typecode, values)
        else:
            try:
                _ = iter(values[0])    # test if it's iterable since array contructor need an iterable
                # Vector([1, 2])
                self._coords = array(self.typecode, values[0])
            except TypeError:
                # Vector(1)
                self._coords = array(self.typecode, [values[0]])     # A list of one scalar is an iterable

    def __len__(self) -> int:
        return len(self._coords)

    def __str__(self) -> str:
        return str(tuple(self._coords))

    def __repr__(self) -> str:
        s = str(self._coords)
        return f"{type(self).__name__}({s[s.find('['):-1]})"

    def __iter__(self):
        return iter(self._coords)

    # def __eq__(self, o) -> bool:
    #     return issubclass(type(o), Vector) and len(self) == len(o) and all(a == b for a, b in zip(self, o))

    def __hash__(self) -> int:
        return functools.reduce(operator.xor, map(hash, self._coords), 0)

    def __bool__(self):
        return any(map(bool, self._coords))

    def __abs__(self):
        return math.hypot(*iter(self._coords))

    def __complex__(self):
        if len(self._coords) == 2:
            return complex(self._coords[0], self._coords[1])
        else:
            raise ValueError(f'Complex only supported for a dimension 2 {type(self).__name__}')

    def argument(self):
        if len(self._coords) == 2:
            return math.atan2(self._coords[1], self._coords[0])
        else:
            raise ValueError(f'Argument only supported for a dimension 2 {type(self).__name__}')

    # custom format r (rectangular) and p (polar) for dimension 2 only
    # Possible extensions (mybe later):
    # - cylindrical coordinates for dimension 3
    # - hyperspherical corrdinates
    # See Fluent Python Chap 10 p. 300
    def __format__(self, format_spec: str) -> str:
        if format_spec is None:
            return str(self._coords)
        if format_spec.endswith('r'):
            if len(self._coords) == 2:
                nf = '{:'+format_spec[:-1]+'f}'
                return '('+nf.format(self._coords[0])+', '+nf.format(self._coords[1])+')'
            else:
                raise ValueError(f'Format specifier r only supported for a dimension 2 {type(self).__name__}')
        if format_spec.endswith('p'):
            if len(self._coords) == 2:
                nf = '{:'+format_spec[:-1]+'f}'
                import math
                arg = math.atan2(self._coords[1], self._coords[0])
                mod = math.hypot(self._coords[0], self._coords[1])
                return '('+nf.format(mod)+' ∠'+nf.format(arg)+')'
            else:
                raise ValueError(f'Format specifier p only supported for a dimension 2 {type(self).__name__}')
        return str(self)

    # Dynamic attributes .x, .y, .z and .t for the first 4 elements
    def __getattr__(self, name: str):
        cls = type(self)
        if len(name) == 1 and name in cls.shortcuts:
            p = cls.shortcuts.find(name)
            if 0 <= p < len(self._coords):
                return self._coords[p]
            else:
                raise AttributeError(f'{cls.__name__} object has no attribute {name}')

    # Attributes x, y, z and t are reserved and immutable
    def __setattr__(self, name: str, value) -> None:
        cls = type(self)
        if len(name) == 1 and cls.shortcuts.find(name) >= 0:
            raise AttributeError(f'{cls.__name__} object attribute {name} is immutable')
        super.__setattr__(self, name, value)

    def __bytes__(self):
        from array import array
        return bytes([ord(self.typecode)])+bytes(array(self.typecode, self._coords))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._coords[index])
        elif isinstance(index, numbers.Integral):
            return self._coords[index]
        else:
            raise(TypeError(f'{cls.__name__} indices must be integers'))

    # Unitary operators (__abs__ already defined, returns a scalar)
    def __pos__(self) -> Vector:
        return Vector(self)

    def __neg__(self) -> Vector:
        return Vector(-x for x in self)

    # Don't define __invert__(self) since there is no obvious use for a Vector

    # Infix operators

    # Addition, do not check type of other, as long it's iterable, it's Ok so we can add Vector and tuples, lists, ranges...
    # If an error is raised because other is not iterable, or other iterable item type doesn't support addition to float,
    # return special singleton value NotImplemented so that Python will try other.__radd__
    # This way we get a clean error msg 'unsupported operand...' instead of a cryptic error raised by zip_longest or +
    def __add__(self, other) -> Vector:
        try:
            return Vector(a+b for a, b in itertools.zip_longest(self, other, fillvalue=0.0))
        except TypeError:
            return NotImplemented       # Do not confuse with NotImplementedError

    # Reverse add  delegates to forward method, since vector addition is commutative, that's easy
    def __radd__(self, other) -> Vector:
        return self.__add__(other)      # or self+other, same thing


    # Infix -
    def __sub__(self, other) -> Vector:
        return self+(-other)        # To keep it simple, but cloning __add__ code is more efficient

    def __rsub__(self, other) -> Vector:
        return self-other


    # * is for Scalar multiplication
    def __mul__(self, scalar) -> Vector:
        # Multiplication by complex will work, but not allowed
        if isinstance(scalar, numbers.Real) and not isinstance(scalar, bool):
            return Vector(x * scalar for x in self)
        else:
            return NotImplemented

    def __rmul__(self, scalar) -> Vector:
        return self.__mul__(scalar)

    # @ is for dot product
    def __matmul__(self, other) -> float:
        try:
            return sum(a*b for a, b in itertools.zip_longest(self, other, fillvalue=0.0))
        except TypeError:
            return NotImplemented

    def __rmatmult(self, other) -> float:
        return self@other

    # ** is for cross product, but in ℝ³ and between vectors only
    def __pow__(self, other) -> Vector:
        if isinstance(other, Vector):
            if len(self) != 3 or len(other) != 3:
                raise ArithmeticError('cross product only supported between 3-divension Vectors')
            else:
                return Vector(self.y*other.z-self.z*other.y, self.z*other.x-self.x*other.z, self.x*other.y-self.y*other.x)
        else:
            return NotImplemented

    # No need to define reverse version actually since cross product is only supported between Vector object,
    # and reverse method is only called when other is not a vector
    # def __rpow__(self, other) -> Vector:
    #     return self**other


    # Inplace method, returning self for a mutable object, or a new object that will be rebound for immutable classes such as Vector
    # Actually inplace method should only be implemented for mutable objects; for immutable objects it's useless
    def __iadd__(self, other):
        if isinstance(other, Vector):
            return self+other       # Which is stupid since it's default implementation anyway...
        else:
            return NotImplemented

    # Comparison
    def __eq__(self, other):
        if isinstance(other, Vector) and len(self)==len(other):
            return all(a==b for a,b in zip(self, other))
        else:
            return NotImplemented       # calls other.__eq__(self), then fallfack on oblect.__eq__ that returns id(self)==id(other)
            

    # Comparison operators do not make sense for Vector      




if __name__ == '__main__':
    v = Vector(range(3))
    print(+v)
    print(-v)
    
    print(v+[-1, -1, -1])   # __add__
    print([-1, -1, -1]+v)   # __radd__
    # print(v+4.14)         # unsupported operand type(s) for +: 'Vector' and 'float'
    # print(v+'aze')        # unsupported operand type(s) for +: 'Vector' and 'str'
    
    print(v*3)
    print(3*v)
    # print(v*'a')          # can't multiply sequence by non-int of type 'Vector'
    # print(v*False)        # bool is rejected; otherwise True=1, False=0
    
    w = Vector(1, 2, -1)
    print(v@w)
    print(v@(2, -2, 1))

    print(v**w)
    print(Vector(3, -3, 1) ** Vector(4, 9, 2))      # Expected is Vector(−15, −2, 39)

    v_alias = v
    v += w
    print(id(v_alias), id(v))   # Different values, v has been rebound
    print(v)

    print(v==w)
    print(v!=w)             # __ne__ is automatic (from object) in this case

