# Unicode in Python
# A é ♫ 𝄞 🐗 🧔 🧔🏻 🧝 🧝‍♂️ 🧝‍♀️ 🧝🏽 🧝🏽‍♂️ 🧝🏽‍♀️
# 2018-08-20    PV

import unicodedata


# Simple characters
# A Latin Capital Letter A, U+0041, UTF-8: 0x41, UTF-16: 0x0041, UTF-32: 0x00000041
# é Latin Small Letter E with Acute, U+00E9, UTF-8: 0xC3 0xA9, UTF-16: 0x00E9, UTF-32: 0x000000E9.  Decomposition: U+0301-U+0065.  Uppercase: É U+00C9
# ♫ Beamed eighth notes, U+266B, UTF-8: 0xE2 0x99 0xAB, UTF-16: 0x266B, UTF-32: 0x0000266B
# 𝄞 Musical symbol G clef, U+1D11E, UTF-8: 0xF0 0x9D 0x84 0x9E, UTF-16: 0xD834 0xDD1E, UTF-32: 0x0001D11E
s = "Aé♫𝄞"

"""
# Len is 4 characters, since s contains 4 codepoints
print("len =", len(s))

print('\tutf-8  -> ', [hex(c) for c in list(bytearray(s, "utf-8"))])

# Note that conversions to utf-16 and utf-32 add a BOM
ba16 = bytearray(s, "utf-16")
# print('\tutf-16 -> ', list(ba16))
m16 = memoryview(ba16).cast('H')    # H = 16-bit unsigned
print('\tutf-16 -> ', [hex(c) for c in m16.tolist()])

ba32 = bytearray(s, "utf-32")
# print('\tutf-32 -> ', list(ba32))
m32 = memoryview(ba32).cast('L')    # L = 32-bit unsigned
print('\tutf-32 -> ', [hex(c) for c in m32.tolist()])


# Normalization of composition/decomposition of accents
s1 = "à"   # Not normalized
s2 = "à"   # Normalized
print("len(s1):", len(s1))
print("len(s2):", len(s2))
print("s1==s2 :", s1==s2)

print("comparizon s1==s2 after NFC normalization: ", unicodedata.normalize("NFC", s1)==unicodedata.normalize("NFC", s2) )
print("comparizon s1==s2 after NFKC normalization: ", unicodedata.normalize("NFKC", s1)==unicodedata.normalize("NFKC", s2) )

# Normalization of compatible codepoints
# n1 = "Ⅷ"    # Numeral Roman VIII U+2167
# n2 = "VIII"   # 4 uppercase letters
n1 = "œ"
n2 = "oe"
print("n1==n2:", n1==n2)
print("comparizon n1==n2 after NFC normalization: ", unicodedata.normalize("NFC", n1)==unicodedata.normalize("NFC", n2) )
print("comparizon n1==n2 after NFKC normalization: ", unicodedata.normalize("NFKC", n1)==unicodedata.normalize("NFKC", n2) )
print("comparizon n1==n2 after NFD normalization: ", unicodedata.normalize("NFD", n1)==unicodedata.normalize("NFD", n2) )
print("comparizon n1==n2 after NFKD normalization: ", unicodedata.normalize("NFKD", n1)==unicodedata.normalize("NFKD", n2) )

# But beware, similar glyphs may not be compatible
g1 = "A"    # Uppercase A = U+0041
g2 = "Α"    # Uppercase greek α = U+0391
print("g1==g2: ", g1==g2)
print("comparizon g1==g2 after NFC normalization: ", unicodedata.normalize("NFC", g1)==unicodedata.normalize("NFC", g2) )
print("comparizon g1==g2 after NFKC normalization: ", unicodedata.normalize("NFKC", g1)==unicodedata.normalize("NFKC", g2) )

print("\tNFC\tNFKC\tNFD\tNFKD")
for s in ["Ⅷ", "œ", "Œ", "æ", "Æ", "ĳ", "Ĳ", "ﬀ", "ﬁ", "ﬂ", "ﬃ", "ﬄ", 'ß', 'é', 'ø']:
    print(s, end='\t')
    for form in ["NFC", "NFKC", "NFD", "NFKD"]:
        print(unicodedata.normalize(form, s), end='\t')
    print()
"""

# All 5 followinf forms are canonical equivalences
cc1 = "\N{LATIN SMALL LETTER U WITH HORN AND DOT BELOW}"
cc2 = "\N{LATIN SMALL LETTER U WITH DOT BELOW}\N{COMBINING HORN}"
cc3 = "\N{LATIN SMALL LETTER U}\N{COMBINING HORN}\N{COMBINING DOT BELOW}"
cc4 = "\N{LATIN SMALL LETTER U WITH HORN}\N{COMBINING DOT BELOW}"
cc5 = "\N{LATIN SMALL LETTER U}\N{COMBINING DOT BELOW}\N{COMBINING HORN}"
form = "NFD"
print(unicodedata.normalize(form, cc1) == unicodedata.normalize(form, cc2) == unicodedata.normalize(form, cc3) == unicodedata.normalize(form, cc4) == unicodedata.normalize(form, cc5))

"""
# Emoji
# 🐗  Boar, U+1F417, UTF-8: 0xF0 0x9F 0x90 0x97, UTF-16: 0xD83D 0xDC17, UTF-32: 0x0001F417
# 🧔  Bearded Person, U+1F9D4
# 🧔🏻  Bearded Person+Light Skin Tone, U+1F9D4 U+1F3FB
# 🧝  Elf, U+1F9DD
# 🧝‍♂️ Man Elf, U+1F9DD(🧝) U+200D(ZWJ) U+2642(♂) U+FE0F(VS-16)
# 🧝‍♀️	Woman Elf =  U+1F9DD(🧝) U+200D(ZWJ) U+2640(♀) U+FE0F(VS-16)
# 🧝🏽	Elf: Medium Skin Tone, U+1F9DD (🧝) U+1F3FD (🏽) 
# 🧝🏽‍♂️ Man Elf: Medium Skin Tone, U+1F9DD (🧝) U+1F3FD (🏽) U+200D(ZWJ) U+2642(♂) U+FE0F(VS-16)
# 🧝🏽‍♀️ Woman Elf: Medium Skin Tone U+1F9DD (🧝) U+1F3FD (🏽) U+200D(ZWJ) U+2640(♀) U+FE0F(VS-16)

e = [ '🐗', '🧔', '🧔🏻', '🧝', '🧝‍♂️', '🧝‍♀️', '🧝🏽', '🧝🏽‍♂️', '🧝🏽‍♀️' ]
for c in e:
    print("%s\t%d\t" % (c, len(c)), [hex(ord(z)) for z in list(c)])
"""

# Use of names
char = u"\N{MUSICAL SYMBOL G CLEF}"
print(len(char))        # 1

# Use of aliases
s3 = "\N{SHY}"                  # U+00AD
print(unicodedata.name(s3))     # SOFT HYPHEN


print(u'ß'.upper())     #  SS


l = ['déjà', 'Meme', 'deja', 'même', 'dejà', 'bpef', 'bœg', 'Boef', 'Mémé', 'bœf', 'boef', 'bnef', 'pêche', 'pèché', 'pêché', 'pêche', 'pêché', 'boeh']

print(l)
print(sorted(l))
print(sorted(l, key=str.upper))
print(sorted(l, key=lambda s: unicodedata.normalize("NFKD", s)))
print(sorted(l, key=lambda s: unicodedata.normalize("NFKD", s.lower())))

