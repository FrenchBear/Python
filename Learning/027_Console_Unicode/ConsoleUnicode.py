# ConsoleUnicode
# 2016-08-10    PV

import sys
from os import system

system('chcp 65001 >nul')
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

print('\ntest_ascii()')
sys.stdout.write("Ûnicöde\n")
print(sys.stdout.encoding)
sys.stdout.encoding
print('\u2500\u2500')
print(chr(0x0472))
s = "Hello\nWorld \u263A\n"
print(s)

# Unicode é U+00E9, UTF-8: 0xC3 0xA9, UTF-16: 0x00E9, UTF-32: 0x000000E9.  Decomposition: U+0301-U+0065.  Uppercase: É U+00C9
# Unicode beamed eighth notes ♫ U+266B, UTF-8: 0xE2 0x99 0xAB, UTF-16: 0x266B, UTF-32: 0x0000266B
# Unicode boar 🐗 U+1F417, UTF-8: 0xF0 0x9F 0x90 0x97, UTF-16: 0xD83D 0xDC17, UTF-32: 0x0001F417

def test(s):
    print(s)
    print(len(s))
    print(hex(ord(s)))
    print()
    
test("A")
test("é")
test("♫")
test("🐗")
