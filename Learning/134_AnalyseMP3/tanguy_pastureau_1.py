# tanguy_pastureau_1.py
# Renomme les MP3 de Tanguy Pastureau
#
# 2023-12-19    PV

import re
import os
from common_fs import get_all_files, file_part, stem_part, folder_part

FILE = re.compile(r'Tanguy_Pastureau_maltraite_l_info_(\d\d\d\d-\d\d-\d\d)_(.*)')

root = r"C:\Temp\A_Trier\mp3-128\Tanguy Pastureau maltraite l'info"

def clean(s: str) -> str:
    s = s.replace('-', ' ')
    s = s[0].upper() + s[1:]
    s = s.replace("J ai", "J'ai").replace(" l ", " l'")
    return s

for filefp in list(get_all_files(root)):
    file = file_part(filefp)
    bn = stem_part(file)
    ma = FILE.match(bn)
    if not ma:
        print(filefp)
    else:
        nn = 'Tanguy Pastureau - ' + ma.group(1) + ' - ' + clean(ma.group(2)) + '.mp3'
        print(nn)
        os.rename(filefp, os.path.join(folder_part(filefp), nn))
