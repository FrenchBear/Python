# tanguy_pastureau_2.py
# Renomme les MP3 de Tanguy Pastureau
#
# 2023-12-19    PV

import re
import os
from common_fs import get_all_files, file_part, stem_part, folder_part

FILE = re.compile(r'Tanguy_Pastureau_maltraite_l_info_(\d\d\d\d-\d\d-\d\d)_(.*)')

root = r"C:\Temp\A_Trier\mp3-128\Tanguy Pastureau maltraite l'info"

for filefp in list(get_all_files(root)):
    if ' !' in filefp:
        print(filefp)
        os.rename(filefp, filefp.replace(' !', '!'))
