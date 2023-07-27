# Rename retro games books
# rename a bunch of filenames without spaces inserting spaces before uppercases (= vbei auto-translate)
# 2020-12-21    PV

import os
import shutil
import unicodedata


# Juste les fichiers d'un dossier, noms sans chemins
def get_files(source: str) -> list[str]:
    # return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])
    _1, _2, files = next(os.walk(source))
    return files


source = r"D:\Downloads\A_Trier\!A_Trier_Livres\Retro Game Design and Programming Books"

listfiles = get_files(source)

for file in listfiles:
    newname = ""
    lasttrans = False
    for c in file:
        if "A" <= c <= "Z" or "0" <= c <= "9" or c == "-":
            if newname != "" and not lasttrans:
                newname += " "
                if c != "-":
                    lasttrans = True
        else:
            lasttrans = False
        newname += c
    print(newname)
    os.rename(os.path.join(source, file), os.path.join(source, newname))
