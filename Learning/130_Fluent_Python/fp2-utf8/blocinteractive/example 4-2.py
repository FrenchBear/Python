# Example 4-2. A five-byte sequence as bytes and as bytearray

>>> cafe = bytes('café', encoding='utf_8')
>>> café
b'caf\xc3\xa9'
>>> cafe[0]
99
>>> cafe[:1]
b'c'
>>> cafe_arr = bytearray(cafe)
>>> cafe_arr
bytearray(b'caf\xc3\xa9')
>>> cafe_arr[-1:]
bytearray(b'\xa9')
