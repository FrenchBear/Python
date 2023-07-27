# vector.cls
# Playing with a good pythonic object
# 2021-03-14    PV

import functools
import math
import operator
from array import array
import numbers

class Vector:
    typecode = 'd'
    shortcuts = 'xyzt'

    def __init__(self, *values) -> None:
        if len(values)>1:
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

# ToDo: vector arithmetic

if __name__ == '__main__':
    v = Vector(range(8))
    print(v[2], 2.0)
    print(v[-1], 7.0)
    print(v[2:7], Vector(2.0, 3.0, 4.0, 5.0, 6.0))
    print(v[2:7:2], Vector(2.0, 4.0, 6.0))
