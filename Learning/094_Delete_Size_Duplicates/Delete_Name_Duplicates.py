# Deletes/Lists files with duplicate names
#
# 2021-12-28    PV      First version
# 2022-06-20    PV      Ignore accents and bloc between parentheses

# DO NOT USE THIS MODULE, WAY TOO RISKY !!!!!!!!!!!

from collections import defaultdict
from typing import Iterable, List
import unicodedata
from common_fs import *
import os

source = r'W:\Livres'
doit = False                            # DO NOT USE THIS MODULE, WAY TOO RISKY !!!!!!!!!!!
doit = False
doit = False
doit = False

dic: defaultdict[str, list[str]] = defaultdict(list)


def filtername(name: str) -> str:
    s1 = name.casefold().split(' - ')[0]
    # p1 = s1.find('(')
    # if p1>=0:
    #     p2 = s1.find(')', p1+1)
    #     if p2>p1: s1=s1[:p1].strip()
    return s1


def lowercase_no_diacritic(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != 'Mn')


for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)
    if ext.casefold() == '.pdf':                               # Process .epub separately to avoid removing a file that both exist as a .pdf and a .epub
        s = lowercase_no_diacritic(filtername(bname))       # Get only the 1st segment (before ' - '), no accent, lowercase, stripped
        if not 'petit fute' in s:
            # Do not ignore part between parentheses, since many files exist in 2nd edition, 3rd
            if (p := s.find('('))>=0:
                p2 = s.find(')', p)
                s = (s[:p]+s[p2+1:]).replace('  ', ' ').strip()
            dic[filtername(s)].append(filefp)

dups = [v for v in dic.values() if len(v) > 1]
print(f'{len(dups)} name duplicates group(s) found.')
ndel = 0
for lst in dups:
    print()
    d = lst[:]

    # First delete extra copies in a_trier\new, keep at least 1
    for file in lst:
        if 'a_trier\\new' in file.casefold():
            if doit:
                os.remove(file)
            print(f'del1 "{file}"')
            d.remove(file)
            ndel += 1
            if len(d) == 1:
                break

    # Thene delete extra copies in a_trier, keep at least 1
    if len(d) > 1:
        for file in lst:
            if 'a_trier' in file.casefold():
                if doit:
                    os.remove(file)
                print(f'del2 "{file}"')
                d.remove(file)
                ndel += 1
            if len(d) == 1:
                break

    # # Then delete any extra remaining copies, keep at least 1
    # while len(d) > 1:
    #     if doit:
    #         os.remove(d[0])
    #     print(f'del3 "{d[0]}"')
    #     d.remove(d[0])
    #     ndel += 1

    print(f'keep "{d[0]}"')

print(ndel, 'fichier(s) effacé(s)')
# DO NOT USE THIS MODULE, WAY TOO RISKY !!!!!!!!!!!