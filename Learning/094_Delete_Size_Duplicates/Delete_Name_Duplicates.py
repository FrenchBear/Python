# Deletes/Lists files with duplicate names
#
# 2021-12-28    PV      First version

from collections import defaultdict
from typing import Iterable, List
from common_fs import *

source = r'W:\Livres'
doit = False

dic: defaultdict[str, list[str]] = defaultdict(list)

def filtername(name: str) -> str:
    s1 = name.casefold().split(' - ')[0]
    # p1 = s1.find('(')
    # if p1>=0:
    #     p2 = s1.find(')', p1+1)
    #     if p2>p1: s1=s1[:p1].strip()
    return s1

for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    if not 'petit futé' in folder.casefold():
        basename, ext = os.path.splitext(file)
        if ext.casefold()=='.pdf':       # '.epub'
            dic[filtername(basename)].append(filefp)

dups = [v for v in dic.values() if len(v)>1]
print(f'{len(dups)} name duplicates group(s) found.')
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
            if len(d)==1: break

    # Thene delete extra copies in a_trier, keep at least 1
    if len(d)>1:
        for file in lst:
            if 'a_trier' in file.casefold():
                if doit:
                    os.remove(file)
                print(f'del2 "{file}"')
                d.remove(file)
            if len(d)==1: break

    # Then delete any extra remaining copies, keep at least 1
    while len(d)>1:
        if doit:
            os.remove(d[0])
        print(f'del3 "{d[0]}"')
        d.remove(d[0])

    print(f'keep "{d[0]}"')
