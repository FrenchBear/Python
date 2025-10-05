# rename_BD.py
# Renomme les BD à partir de deux listes de fichiers (originale et corrigée)
#
# 2025-09-28    PV

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

        ofp = r"C:\MusicOD\Humour\Matthieu Noël" + os.sep + o + ".mp3"
        nfp = r"C:\MusicOD\Humour\Matthieu Noël" + os.sep + n + ".mp3"
        if not file_exists(ofp):
            breakpoint()
            pass
            
        os.rename(ofp, nfp)
