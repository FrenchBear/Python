# strandbyte.py
# Learning python, strings and bytes
#
# 2018-09-21    PV

s = "café ♫ 𝄞"
print(s, len(s))
b = s.encode('utf8')
print(b, len(b))

s2 = b.decode('utf8')
print(s2)

cafe = bytes('café', encoding='utf_8')
print(cafe)
# cafe[0] = 67              Error: bytes do not support assignment
cafe_arr = bytearray(cafe)  # But a bytearray does
cafe_arr[0] = 67
print(cafe_arr)

# Note that for str type, s[0]==s[:1], that's the only sequence with this behavior.
# For all other sequences, s[0] is one item (an integer for instance for bytes), where
# s[:1] returns a sequence containing only the first element

print(s[0], s[:1])  # c c
print(b[0], b[:1])  # 99 b'c'

# Both bytes and bytearray support every str method except those that do formatting
# (format, format_map) and a few others that depend on Unicode data, including case
# fold, isdecimal, isidentifier, isnumeric, isprintable, and encode. This means that
# you can use familiar string methods like endswith, replace, strip, translate, upper,
# and dozens of others with binary sequences—only using bytes and not str arguments.


# Convert from/to hex string
print(bytes.fromhex('31 4B CE A9'))
print(bytes.fromhex('314BCEA9'))

tb = bytes.fromhex("BADC0FFE")
print(tb.hex())

# Initializing bytes from the raw data of an array
import array
numbers = array.array('h', [-2, -1, 0, 1, 2])
octets = bytes(numbers)
print(octets)


# Using memoryview and struct to inspect a GIF image header
import struct
fmt = '<3s3sHH'  # 1
with open('skull.gif', 'rb') as fp:
    img = memoryview(fp.read())  # 2
header = img[:10]  # 3
print(bytes(header))  # 4       # b'GIF89a\xe2\x00\xb5\x00'
s = struct.unpack(fmt, header)  # 5
print(s)   # (b'GIF', b'89a', 226, 181)
del header  # 6
del img

# 1: struct format: < little-endian; 3s3s two sequences of 3 bytes; HH two 16-bit integers.
# 2: Create memoryview from file contents in memory…
# 3: …then another memoryview by slicing the first one; no bytes are copied here.
# 4: Convert to bytes for display only; 10 bytes are copied here.
# Unpack memoryview into tuple of: type, version, width, and height.
# Delete references to release the memory associated with the memoryview instances.


# Encoding
# latin_1 = iso8859_1
# cp1252 = latin_1 + curly quotes and € sign, "ANSI"
# cp437, cp850: MS-Dos encodings

for codec in ['latin_1', 'utf_8', 'utf_16', 'cp850']:
    print(codec, 'El Niño'.encode(codec), sep='\t')

# encoding errors, simple (can also register an error handling function)
city = 'São Paulo'
print(city.encode('utf_8'))     # b'S\xc3\xa3o Paulo'
print(city.encode('utf_16'))    # b'\xff\xfeS\x00\xe3\x00o\x00 \x00P\x00a\x00u\x00l\x00o\x00'
print(city.encode('iso8859_1'))  # b'S\xe3o Paulo'
# print(city.encode('cp437'))  --> UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in position 1: character maps to <undefined>
print(city.encode('cp437', errors='ignore'))    # b'So Paulo'
print(city.encode('cp437', errors='replace'))   # b'S?o Paulo'
print(city.encode('cp437', errors='xmlcharrefreplace'))  # b'S&#227;o Paulo'


# Exploring locales
import sys
import locale
expressions = """
locale.getpreferredencoding()
type(my_file)
my_file.encoding
sys.stdout.isatty()
sys.stdout.encoding
sys.stdin.isatty()
sys.stdin.encoding
sys.stderr.isatty()
sys.stderr.encoding
sys.getdefaultencoding()
sys.getfilesystemencoding()
"""
my_file = open('dummy', 'w')
for expression in expressions.split():
    value = eval(expression)
    print(expression.rjust(30), '->', repr(value))

"""
 locale.getpreferredencoding() -> 'cp1252'
                 type(my_file) -> <class '_io.TextIOWrapper'>
              my_file.encoding -> 'cp1252'
           sys.stdout.isatty() -> True
           sys.stdout.encoding -> 'utf-8'
            sys.stdin.isatty() -> True
            sys.stdin.encoding -> 'utf-8'
           sys.stderr.isatty() -> True
           sys.stderr.encoding -> 'utf-8'
      sys.getdefaultencoding() -> 'utf-8'
   sys.getfilesystemencoding() -> 'utf-8'
"""

# If the value of sys.stdout.isatty() becomes False, and sys.stdout.encoding is set by locale.getpreferredencoding()

# If you omit the encoding argument when opening a file, the default is given by locale.getpreferredencoding()

# The encoding of sys.stdout/stdin/stderr is given by the PYTHONIOENCODING environment variable, if present, otherwise
# it is either inherited from the console or defined by locale.getpreferredencoding() if the output/input is redirected
# to/from a file.

# sys.getdefaultencoding() is used internally by Python to convert binary data to/from str; this happens less often in Python 3, but still happens.

# sys.getfilesystemencoding() is used to encode/decode filenames (not file contents). It is used when open() gets a str
# argument for the filename; if the filename is given as a bytes argument, it is passed unchanged to the OS API. The
# Python Unicode HOWTO says: “on Windows, Python uses the name mbcs to refer to whatever the currently configured
# encoding is.” The acronym MBCS stands for Multi Byte Character Set, which for Microsoft are the legacy variable-width
# encodings like gb2312 or Shift_JIS, but not UTF-8.


# Case folding
# Case folding is essentially converting all text to lowercase, with some additional transformations.

# For any string s containing only latin1 characters, s.casefold() produces the same result as s.lower(), with only two
# exceptions—the micro sign 'μ' is changed to the Greek lowercase mu (which looks the same in most fonts) and the German
# Eszett or“sharp s” (ß) becomes “ss”

from unicodedata import normalize, name
ohm = '\u2126'
print(name(ohm))        # OHM SIGN
ohm_c = normalize('NFC', ohm)
print(name(ohm_c))      # GREEK CAPITAL LETTER OMEGA

s1 = "µßœ"
s2 = s1.casefold()
print(s1, s2, name(s1[0]), name(s2[0]), sep='   ')

