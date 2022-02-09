# spell_variant.py
# Recherche si un mot est dans le dictionnaire, sinon des mots proches
#
# 2022-01-10    PV      D'après 'Programmation efficace'

from collections import defaultdict
from collections import Counter
from typing import DefaultDict, Tuple, Counter
from common_fs import *

class Trie:
    def __init__(self) -> None:
        self.is_word = False
        self.s: DefaultDict[str, Trie] = defaultdict(Trie)

    def add_word(self, word: str):
        if len(word)==0:
            self.is_word = True
            return
        self.s[word[0]].add_word(word[1:])

    def find_word(self, word: str) -> bool:
        if len(word)==0:
            return self.is_word
        if not word[0] in self.s:
            return False
        return self.s[word[0]].find_word(word[1:])

# smf = ensemble des mots français
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    smf = set(f.read().splitlines())
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    smf |= set(mot for mot in f.read().splitlines() if ' ' not in mot and mot not in smf)
with open(r'words\extra.fr.txt', 'r', encoding='UTF-8') as f:
    smf |= set(mot for mot in f.read().splitlines() if mot not in smf)

print(len(smf))

T = Trie()
for word in smf:
    T.add_word(word)

def spell_check(T: Trie, w: str) -> str:
    dist = 0
    while True:
        u = search(T, dist, w)
        if u is not None:
            return u
        dist += 1

def search(T: Trie, dist: int, w: str, i=0):
    if i==len(w):
        if T is not None and T.is_word and dist==0:
            return ''
        else:
            return None
    if T is None or w[i] not in T.s:
        return None
    f = search(T.s[w[i]], dist, w, i+1)
    if f is not None:
        return w[i]+f
    if dist==0:
        return None
    # insertion/substitution
    for c in T.s.keys():
        f = search(T.s[c], dist-1, w, i)
        if f is not None:
            return c+f
        f = search(T.s[c], dist-1, w, i+1)
        if f is not None:
            return c+f
    # suppression
    return search(T, dist-1, w, i+1)


for m in ['pome', 'pOmme', 'poomme']:
    print(m, spell_check(T, m))
