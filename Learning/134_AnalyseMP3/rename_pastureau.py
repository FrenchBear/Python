# rename_pastureau.py
# Renomme les MP3 de Tanguy Pastureau à partir du fichier Titres des chroniques.txt
#
# 2025-09-28    PV

import os
import glob
from common_fs import file_part, file_exists

root = r"C:\MusicOD\Humour\Tanguy Pastureau"

ntot = 0
nren = 0
nskip = 0
with open(r"C:\MusicOD\Humour\Tanguy Pastureau\Titres des chroniques.txt") as f:
    for line in f:
        ntot += 1
        line = line.strip()
        # if line=="2019-05-10 - Robert II Le Pieux était plus défoncé qu'Amy Winehouse":
        #     breakpoint()
        #     pass
        y = line[:4]
        ym = line[:7]
        ymd = line[:10]
        filefp = rf"C:\MusicOD\Humour\Tanguy Pastureau\Tanguy Pastureau maltraite l'info {y}\{ym}\{line}.mp3"
        if file_exists(filefp):
            nskip += 1
        else:
            pattern = rf"C:\MusicOD\Humour\Tanguy Pastureau\Tanguy Pastureau maltraite l'info {y}\{ym}\{ymd}*.mp3"
            matching_files = glob.glob(pattern)
            if len(matching_files) == 1:
                print(f"{file_part(matching_files[0]):<80} => {file_part(line)}")
                nren += 1
                os.rename(matching_files[0], filefp)
            elif len(matching_files) == 0:
                print("*** Err: Can't find "+file_part(filefp))
            else:
                print("*** Err too many matches: ", matching_files) 

print(f"\n{ntot} total files, {nren} renamed, {nskip} skipped")
