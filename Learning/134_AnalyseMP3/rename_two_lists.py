# rename_two_lists.py
# Renomme des fichiers à partir de deux listes de fichiers (originale et corrigée)
#
# 2025-09-28    PV
# 2025-10-21    PV      Rename and cleanup

import os
from common_fs import file_exists

with open(r"C:\Temp\original.txt", "r", encoding="utf-8") as f:
    old = f.readlines()

with open(r"C:\Temp\fixed.txt", "r", encoding="utf-8") as f:
    new = f.readlines()

assert len(old) == len(new)

for i in range(len(old)):
    o = old[i].strip()
    n = new[i].strip()
    if o != n:
        print("old:", o)
        print("new:", n)
        print()

        if not file_exists(o):
            breakpoint()
            pass
            
        os.rename(o, n)
