from typing import NamedTuple, ClassVar
from dataclasses import dataclass
from array import array

@dataclass(frozen=True)
class CoordinateDC:
    lat: float
    lon: float
    typecode: ClassVar[str] = 'd'

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'CDC: {abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}° {we}'

    def __add__(self, other) -> 'CoordinateDC':
        if isinstance(other, CoordinateDC):
            return CoordinateDC(self.lat + other.lat, self.lon + other.lon)
        raise TypeError('Can only add a CoorinateDC to a CoorinateDC')

    def __iter__(self):
        return (f for f in (self.lat, self.lon))

    # def __getitem__(self, index):
    #     if index == 0:
    #         return self.lat
    #     if index == 1:
    #         return self.lon
    #     raise IndexError

    def __bytes__(self):
        b = (bytes([ord(self.typecode)]) + bytes(array(self.typecode, self)))
        return b

class CoordinateNT(NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f'CNT: {abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}° {we}'


print(set(dir(CoordinateNT)) - set(dir(CoordinateDC)))

cdc1 = CoordinateDC(1.0, 2.0)
cdc2 = CoordinateDC(3.0, 4.0)
cdc3 = cdc1 + cdc2
print(cdc3)
print(bytes(cdc3))

cnt1 = CoordinateNT(1.0, 2.0)
cnt2 = CoordinateNT(3.0, 4.0)
cnt3 = cnt1 * 2
print(cnt3)
print(cnt1[1])
