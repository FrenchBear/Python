# sr.py
# SyncRename BD
#
# 2023-12-24    PV

# import re
import os
from common_fs import get_files, basename_part, extension_part

# FILE = re.compile(r'Tanguy_Pastureau_maltraite_l_info_(\d\d\d\d-\d\d-\d\d)_(.*)')

doit = True

reference = r'W:\BD\Classique\Papyrus'
arenommer = r'C:\Downloads\A_Trier\!A_Trier_BD\Papyrus Intégrale'

refDic: dict[str, str] = {}

for file in list(get_files(reference)):
    bn = basename_part(file)
    ts = bn.split(' - ')
    if len(ts) >= 3:
        refDic[ts[1]] = ' - '.join(ts[2:])

for file in list(get_files(arenommer)):
    bn = basename_part(file)
    ext = extension_part(file)
    ts = bn.split(' - ')
    if len(ts) >= 2:
        if ts[1] in refDic:
            nn = ts[0] + ' - ' + ts[1] + ' - ' + refDic[ts[1]]
            print(repr(file) + ' -> ' + repr(nn + ext))
            if doit:
                os.rename(os.path.join(arenommer, file), os.path.join(arenommer, nn + ext))
        else:
            print("file " + repr(file) + ': n° non trouvé dans le dossier de référence, ignoré')
    else:
        print("file " + repr(file) + ': moins de 2 segments, ignoré')

# ma = FILE.match(bn)
# if not ma:
#     print(filefp)
# else:
#     nn = 'Tanguy Pastureau - ' + ma.group(1) + ' - ' + clean(ma.group(2)) + '.mp3'
#     print(nn)
#     os.rename(filefp, os.path.join(folder_part(filefp), nn))
