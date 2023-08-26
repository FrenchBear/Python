# Example 28-2. Reading a C struct in the Python console.

>>> from struct import unpack, calcsize
>>> FORMAT = 'i12s2sf'
>>> size = calcsize(FORMAT)
>>> data = open('metro_areas.bin', 'rb').read(size)
>>> data
b"\xe2\x07\x00\x00Tokyo\x00\xc5\x05\x01\x00\x00\x00JP\x00\x00\x11X'L"
>>> unpack(FORMAT, data)
(2018, b'Tokyo\x00\xc5\x05\x01\x00\x00\x00', b'JP', 43868228.0)
