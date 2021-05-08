# vector_op.py
# Play with operators
# 2021-05-09    PV

from __future__ import annotations
import functools
import math
import operator
from array import array
import numbers
import itertools


class Vector:
    typecode = 'd'
    shortcuts = 'xyzt'

    def __init__(self, *values) -> None:
        if len(values)>1:
            # Vector(1, 2)
            self._coords = array(self.typecode, values)
        else:
            try:
                it = iter(values[0])    # test if it's iterable since array contructor need an iterable
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

    def __eq__(self, o) -> bool:
        return issubclass(type(o), Vector) and len(self) == len(o) and all(a==b for a, b in zip(self, o))

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
        if format_spec == None:
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
        if len(name)==1 and cls.shortcuts.find(name)>=0:
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
    def __add__(self, other):
        try:
            return Vector(a+b for a,b in itertools.zip_longest(self, other, fillvalue=0.0))
        except TypeError:
            return NotImplemented       # Do not confuse with NotImplementedError

    # Reverse add  delegates to forward method, since vector addition is commutative, that's easy
    def __radd__(self, other):
        return self.__add__(other)      # or self+other, same thing



if __name__ == '__main__':
    v = Vector(range(3))
    print(+v)
    print(-v)
    print(v+[-1,-1,-1])     # __add__
    print([-1,-1,-1]+v)     # __radd__
    # print(v+4.14)         # unsupported operand type(s) for +: 'Vector' and 'float'
    # print(v+'aze')        # unsupported operand type(s) for +: 'Vector' and 'str'
