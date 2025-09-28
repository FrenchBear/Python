# rename_BD.py
# Renomme les BD à partir de deux listes de fichiers (originale et corrigée)
#
# 2025-09-28    PV

import os
#from common_fs import file_exists

with open(r"C:\Temp\bdclassique.txt", "r") as f:
    old = f.readlines()

with open(r"C:\Temp\bdclassique fixed.txt", "r") as f:
    new = f.readlines()

assert len(old) == len(new)

for i in range(len(old)):
    o = old[i].strip()
    n = new[i].strip()
    if o != n:
        print(o)
        print(n)
        print()
        os.rename(o, n)
