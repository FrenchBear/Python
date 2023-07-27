# Delete_Size_Duplicates_2_Sources.py
# New version of Delete Size Duplicates, different from the one in 68_Rename_Temp_BD
# More complete
#
# 2021-12-26    PV
# 2021-12-28    PV      Keep at least 1 version
# 2022-06-20    PV      Print delete count
# 2023-01-24    PV      Version 2_Sources

from collections import defaultdict
#from typing import Iterable, List
from common_fs import get_all_files
import os

source1 = r'W:\Livres'
source2 = r'C:\Temp\A_Trier'
doit = True

dic: defaultdict[int, list[str]] = defaultdict(list)

# First index source1
# No attempt is made to delete duplicates in source1
print('Indexing', source1)
for filefp in get_all_files(source1):
    folder, file = os.path.split(filefp)
    _, ext = os.path.splitext(file)
    if ext.casefold() in ['.pdf', '.epub']:
        s = os.path.getsize(filefp)
        dic[s].append(filefp)

# Then index source2
ndel = 0
print('Comparing ', source2)
allfiles2 = list(get_all_files(source2))
for filefp in allfiles2:
    folder, file = os.path.split(filefp)
    _, ext = os.path.splitext(file)
    if ext.casefold() in ['.pdf', '.epub']:
        s = os.path.getsize(filefp)
        if s in dic:
            print('Size', s, 'dup:\n  '+str(dic[s]))
            print('  '+filefp)
            if doit:
                os.remove(filefp)
                print(f'del "{filefp}"')
                ndel += 1
            print()

print(ndel, 'fichier(s) effacé(s)')
