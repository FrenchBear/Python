# Example 4-9. Closer inspection of Example 4-8 running on Windows reveals the bug and how to fix it

>>> fp = open('cafe.txt', 'w', encoding='utf_8')
>>> fp
<_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf_8'>
>>> fp.write('café')
4
>>> fp.close()
>>> import os
>>> os.stat('cafe.txt').st_size
5
>>> fp2 = open('cafe.txt')
>>> fp2
<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='cp1252'>
>>> fp2.encoding
'cp1252'
>>> fp2.read()
'cafÃ©'
>>> fp3 = open('cafe.txt', encoding='utf_8')
>>> fp3
<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='utf_8'>
>>> fp3.read()
'café'
>>> fp4 = open('cafe.txt', 'rb')
>>> fp4
<_io.BufferedReader name='cafe.txt'>
>>> fp4.read()
b'caf\xc3\xa9'
