>>> from coordinates import Coordinate
>>> moscow = Coordinate(55.76, 37.62)
>>> moscow
<coordinates.Coordinate object at 0x107142f10>
>>> location = Coordinate(55.76, 37.62)
>>> location == moscow
False
>>> (location.lat, location.lon) == (moscow.lat, moscow.lon)
True
