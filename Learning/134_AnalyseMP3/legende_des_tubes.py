# Renomme les fichiers de la légende des tubes au format "nn - Title..."
#
# 2025-12-08    PV

import os
from common_fs import get_all_files, file_part

source = r'C:\MusicCMPV2\Albums\La légende des tubes - 40 CD'
source = r'E:\Music\Albums\La légende des tubes - 40 CD'

for filefp in list(get_all_files(source)):
    if filefp.endswith(".mp3"):
        parent = os.path.dirname(filefp)
        file = file_part(filefp)
        if file[0] in '0123456789' and file[1] in '0123456789' and file[2]==' ' and file[3]!='-':
            newfile = file[:2] + " - " + file[3].upper() + file[4:]
            print(parent)
            print('  ', file, ' --> ', newfile)
            os.rename(os.path.join(parent, file), os.path.join(parent, newfile))