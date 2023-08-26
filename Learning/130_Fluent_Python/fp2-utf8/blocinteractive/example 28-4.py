# Example 28-4. Using memoryview and struct to inspect a GIF image header

>>> import struct
>>> fmt = '<3s3sHH'
>>> with open('filter.gif', 'rb') as fp:
...     img = memoryview(fp.read())
...
>>> header = img[:10]
>>> bytes(header)
b'GIF89a+\x02\xe6\x00'
>>> struct.unpack(fmt, header)
(b'GIF', b'89a', 555, 230)
>>> del header
>>> del img
