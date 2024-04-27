# Rename retro games books
# Rename a bunch of filenames without spaces inserting spaces before uppercases (= vbei auto-translate)
#
# 2020-12-21    PV

import os
from common_fs import get_files


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
