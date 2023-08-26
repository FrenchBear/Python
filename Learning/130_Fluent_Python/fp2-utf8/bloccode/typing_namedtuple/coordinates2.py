# Example 5-8. typing_namedtuple/coordinates2.py

from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = 'WGS84'
