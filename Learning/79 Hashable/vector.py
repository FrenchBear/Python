# vector.cls
# Playing with a good pythonic object
# 2021-03-14    PV

import functools
import math
import operator
from array import array

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

    def __eq__(self, o: object) -> bool:
        return issubclass(type(o), Vector) and len(self) == len(o) and all(map(lambda p: p[0] == p[1], zip(self._coords, iter(o))))

    def __hash__(self) -> int:
        return functools.reduce(operator.xor, map(hash, self._coords), 0)

    def __bool__(self):
        return all(map(bool, self._coords))

    def __abs__(self):
        return math.hypot(self._coords)

    def __complex__(self):
        if len(self._coords) == 2:
            return complex(self._coords)
        else:
            raise f'Complex only supported for a dimension 2 {type(self).__name__}'

    def argument(self):
        if len(self._coords) == 2:
            return math.atan2(self.__y, self.__x)
        else:
            raise f'Argument only supported for a dimension 2 {type(self).__name__}'

    def __format__(self, format_spec: str) -> str:
        if format_spec == None:
            return str(self._coords)
        if format_spec.endswith('r'):
            if len(self._coords) == 2:
                nf = '{:'+format_spec[:-1]+'f}'
                return '('+nf.format(self.x)+', '+nf.format(self.y)+')'
            else:
                raise f'Format specifier r only supported for a dimension 2 {type(self).__name__}'
        if format_spec.endswith('p'):
            if len(self._coords) == 2:
                nf = '{:'+format_spec[:-1]+'f}'
                import math
                arg = math.atan2(self.y, self.x)
                mod = math.hypot(self.x, self.y)
                return '('+nf.format(mod)+' ∠'+nf.format(arg)+')'
            else:
                raise f'Format specifier p only supported for a dimension 2 {type(self).__name__}'
        return str(self)

    def __getattr__(self, name: str):
        cls = type(self)
        if len(name) == 1 and name in cls.shortcuts:
            #p = shortcuts.index(name)      # DO NOT use index, it will throw an exception if name is not found, while find returns -1
            p = cls.shortcuts.find(name)
            if 0 <= p < len(self._coords):
                return self._coords[p]
            else:
                raise AttributeError(f'{cls.__name__} object has no attribute {name}')

    def __setattr__(self, name: str, value) -> None:
        super.__setattr__(self, name, value)

    def __bytes__(self):
        from array import array
        return bytes([ord(self.typecode)])+bytes(array(self.typecode, self._coords))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


if __name__ == '__main__':
    v = Vector(3, 4)
    print(hash(v))
