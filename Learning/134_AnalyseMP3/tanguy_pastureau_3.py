# tanguy_pastureau_3.py
# Détecte les doublons des MP3 de Tanguy Pastureau
#
# 2023-12-19    PV

import re
import os
import winshell     # type: ignore
from common_fs import get_all_files
from Levenshtein import LevenshteinDistance, Lowercase_no_diacritic

FILE = re.compile(r'Tanguy Pastureau - \d\d\d\d-\d\d-\d\d - (.*)\.mp3')
do_it = False

root = r"C:\MusicOD\Humour\Tanguy Pastureau"
d:dict[str,str] = {}

for filefp in list(get_all_files(root)):
    file = os.path.basename(filefp)
    if m := FILE.match(file):
        title = m[1]
        key = Lowercase_no_diacritic(title).replace(' ', '').replace("'", '').replace('-', '')
        if key!='tanguypastureaumaltraitelinfo':
            if key in d:
                f2 = d[key]
                todel = max(filefp, f2)
                print(f"Doublon: {filefp}", '=> à supprimer' if todel==filefp else '')
                print(f"         {d[key]}", '=> à supprimer' if todel==d[key] else '')
                print()
                if do_it:
                    winshell.delete_file(todel, allow_undo=True, silent=True)
            else:
                for k in d.keys():
                    if LevenshteinDistance(k, key, 3) <= 3:
                        f2 = d[k]
                        print(f"Doublon probable: {filefp}")
                        print(f"                  {d[k]}")
                        print()

                d[key] = filefp



