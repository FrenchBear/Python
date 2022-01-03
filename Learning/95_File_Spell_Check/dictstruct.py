# dictstruct.py
# Play with data structures to represent a dictionary
#
# 2022-01-03    PV

from collections import defaultdict
from typing import DefaultDict
import psutil   # type: ignore


mem1 = psutil.Process().memory_info().rss / (1024 * 1024)

# # dmf est l'ensemble des mots français accentués, indexé par la version casefold() du mot
# print('dic version')
# with open('mots_fr2.txt', 'r', encoding='UTF-8') as f:
#     dmf = dict([(mot.casefold(), mot) for mot in f.read().splitlines()])
#     #dmf = [mot for mot in f.read().splitlines()]
# print(len(dmf))

smf = set()
# dmf est l'ensemble des mots français accentués, indexé par la version casefold() du mot
print('dic version')
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    smf = set([mot for mot in f.read().splitlines()])
print(len(smf))
with open(r'words\words2.fr.txt', 'r', encoding='UTF-8') as f:
    for mot in f.read().splitlines():
        if not mot in smf:
            print(mot)


class Arbre:
    def __init__(self) -> None:
        self.is_word = False
        self.dic: DefaultDict[str, Arbre] = defaultdict(Arbre)

    def add_word(self, word: str):
        if len(word)==0:
            self.is_word = True
            return
        self.dic[word[0]].add_word(word[1:])

    def find_word(self, word: str) -> bool:
        if len(word)==0:
            return self.is_word
        if not word[0] in self.dic:
            return False
        return self.dic[word[0]].find_word(word[1:])

def read_arbre():
    print('arbre version')
    amf = Arbre()
    with open('mots_fr2.txt', 'r', encoding='UTF-8') as f:
        for mot in f.read().splitlines():
            amf.add_word(mot)
    print(amf.find_word('pomme'))
    print(amf.find_word('astérisque'))
    print(amf.find_word('astérix'))
    with open('mots_fr2.txt', 'r', encoding='UTF-8') as f:
        for mot in f.read().splitlines():
            if not amf.find_word(mot):
                breakpoint()
                pass

mem2 = psutil.Process().memory_info().rss / (1024 * 1024)
print(f'{mem2-mem1:.3f} MB')
