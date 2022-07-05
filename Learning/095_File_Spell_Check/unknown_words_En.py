# unknown_words.py
# Find English words not in dictionary or exceptions
#
# 2022-07-04 PV

from collections import Counter
from typing import Counter
from common_fs import *
from casefix_En import *


source = r'W:\Livres\A_Trier'
doit = True

unknowns: Counter[str] = Counter()

# dme est l'ensemble des mots anglais
with open(r'words\words.en.txt', 'r', encoding='UTF-8') as f:
    sme = set(mot for mot in f.read().splitlines())
with open(r'words\extra.en.txt', 'r', encoding='UTF-8') as f:
    sme |= set(mot for mot in f.read().splitlines())


def process_word(w: str, first: bool):
    if len(w) <= 1:
        return w
    w0 = w

    while w and str.isdigit(w[0]):
        w = w[1:]
    while w and str.isdigit(w[-1]):
        w = w[:-1]
    if len(w)==0:   # Only digits
        return w0

    w=w0

    if w in sme or w in set_casefix or ('A' <= w[0] <= 'Z' and w not in set_casefix and w[0].lower()+w[1:] in sme) or w == 'js':
        return w0
    unknowns.update([w])
    # if w == 'CS':
    #     breakpoint()
    return '«'+w0+'»'


def process_segment(s):
    w = ''
    res = ''
    firstword = True
    for c in s:
        if c in [' ', '+', '.', ',', '-']:     # Simple quote is not considered a separator, maybe should only if not sandwich between letters
            # typically {'+', '#', '.', ',', ' ', '-'}
            if w != '':
                res += process_word(w, firstword)
                w = ''
                firstword = c != ' '
            res += c
        else:
            w += c
    if w != '':
        res += process_word(w, firstword)
    # Exceptions
    res = process_exceptions_En(res)
    return res


def process_name(name: str):
    ts = name.split(' - ')
    s1 = ts[0]

    bp = ''
    try:
        pp = s1.index('(')
        bp = s1[pp:]
        s1 = s1[:pp]
    except:
        pass
    process_segment(s1)


nt = 0
for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)
    nt += 1
    process_name(bname)

print()
print(nt, 'file(s) processed')
# print(unknowns.most_common(20))

with open(r'c:\temp\newwords.txt', 'w', encoding='utf-8') as out:
    for w, c in unknowns.most_common():
        if c==1: break
        print(w, c)
        out.write(w+'\n')
