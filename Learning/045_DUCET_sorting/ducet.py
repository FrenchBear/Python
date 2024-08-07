# ducet-stype sorting
# Proof of concept
#
# 2018-08-25    PV
# 2018-09-22    PV      pyuca module (pip install pyuca)


import unicodedata
import locale


# lf = ['déjà', 'Deja', 'Meme', 'deja', 'même', 'dejà', 'bpef', 'bœg', 'Boef', 'Mémé',
#        'bœf', 'boef', 'bnef', 'pêche', 'pèché', 'pêché', 'pêche', 'pêché', 'boeh']


def pregenerate_dic():
    charset = set()
    for word in lf:
        for char in word:
            charset.add(char)

    for char in sorted(charset):
        W1 = ord(char)
        s = unicodedata.normalize("NFD", char)
        if len(s) == 1:
            W2 = 0
        else:
            W2 = ord(s[1])
        W3 = 1 if char.isupper() else 0

        print("'%s': [0x%04x, 0x%04x, 0x%04x]," % (char, W1, W2, W3))


# [letter, accent, case]
dic: dict[str, list[int]] = {
    "A": [0x0061, 0x0000, 0x0001],
    "Â": [0x0061, 0x0302, 0x0001],
    "B": [0x0062, 0x0000, 0x0001],
    "D": [0x0064, 0x0000, 0x0001],
    "E": [0x0065, 0x0000, 0x0001],
    "M": [0x006D, 0x0000, 0x0001],
    "a": [0x0061, 0x0000, 0x0000],
    "b": [0x0062, 0x0000, 0x0000],
    "c": [0x0063, 0x0000, 0x0000],
    "d": [0x0064, 0x0000, 0x0000],
    "e": [0x0065, 0x0000, 0x0000],
    "f": [0x0066, 0x0000, 0x0000],
    "g": [0x0067, 0x0000, 0x0000],
    "h": [0x0068, 0x0000, 0x0000],
    "i": [0x0069, 0x0000, 0x0000],
    "j": [0x006A, 0x0000, 0x0000],
    "m": [0x006D, 0x0000, 0x0000],
    "n": [0x006E, 0x0000, 0x0000],
    "o": [0x006F, 0x0000, 0x0000],
    "p": [0x0070, 0x0000, 0x0000],
    "q": [0x0071, 0x0000, 0x0000],
    "r": [0x0072, 0x0000, 0x0000],
    "s": [0x0073, 0x0000, 0x0000],
    "t": [0x0074, 0x0000, 0x0000],
    "â": [0x0061, 0x0302, 0x0000],
    "à": [0x0061, 0x0300, 0x0000],
    "è": [0x0065, 0x0300, 0x0000],
    "é": [0x0065, 0x0301, 0x0000],
    "É": [0x0065, 0x0301, 0x0001],
    "ê": [0x0065, 0x0302, 0x0000],
    "œ": [0x006F, 0x0000, 0x0000, 0x0065, 0x0000, 0x0000],
}

"""
l: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(0, len(l), 3):
    print(l[i], l[i+1], l[i+2])
"""


class sorter:
    def __init__(self, L1: int, L2: int, L3: int):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3

    def greeting(self, name: str) -> str:
        return "Hello " + name

    # Wrong: sorting words in a, all words starting with a accent such as âge will be at the end of a
    # instead of being between agent and agir
    # -> Need to sort on all L1 keys first, then on all L2, then on all L3, done in weights2
    def weigths(self, s: str) -> str:
        w = ""
        for c in s:
            ws = dic[c]
            for i in range(0, len(ws), 3):
                w += f"{ws[i+self.L1]:04x}"
                w += f"{ws[i+self.L2]:04x}"
                w += f"{ws[i+self.L3]:04x}"
        # print(f"weights${self.L1}{self.L2}{self.L3}('{s}') -> '{w}'")
        return w

    def weigths2(self, s: str) -> str:
        w = ""
        for c in s:
            ws = dic[c]
            for i in range(0, len(ws), 3):
                w += f"{ws[i+self.L1]:04x}"
        w += " "
        for c in s:
            ws = dic[c]
            for i in range(0, len(ws), 3):
                w += f"{ws[i+self.L2]:04x}"
        w += " "
        for c in s:
            ws = dic[c]
            for i in range(0, len(ws), 3):
                w += f"{ws[i+self.L3]:04x}"
        # print(f"weights2_${self.L1}{self.L2}{self.L3}('{s}') -> '{w}'")
        return w


s012 = sorter(0, 1, 2)
s021 = sorter(0, 2, 1)
# for wf in lf:
#     print(wf, s012.weigths(wf))
#     print(wf, s021.weigths(wf))
#     print()

lf = ["e", "é", "E", "É"]
lf = ["déjà", "Deja", "deja", "dejà"]
lf = ["âge", "Âge", "age", "agé", "Age", "âgé", "âger", "agent", "agir"]

print("Lettre, accent, case (weights)")
print(sorted(lf, key=s012.weigths))
print()
print("Lettre, case, accent (weights)")
print(sorted(lf, key=s021.weigths))
print()
print("Lettre, accent, case (weights2)")
print(sorted(lf, key=s012.weigths2))
print()
print("Lettre, case, accent (weights2)")
print(sorted(lf, key=s021.weigths2))
print()
print("Locale défaut")
print(sorted(lf, key=locale.strxfrm))
locale.setlocale(locale.LC_ALL, "en-US")
print()
print("Locale en-US")
print(sorted(lf, key=locale.strxfrm))


# Finally discovered pyuca module
# pip install pyuca
# https://github.com/jtauber/pyuca

import pyuca  # type: ignore

coll = pyuca.Collator()
print("\npyuca:")
print(sorted(lf, key=coll.sort_key))
