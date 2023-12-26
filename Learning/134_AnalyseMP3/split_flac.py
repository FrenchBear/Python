# split_flac.py
# Analyse music files, move .flag in a separate structure
#
# 2023-12-19    PV

import os
import shutil
from common_fs import get_all_files, folder_part, extension_part

root = r'C:\Downloads\A_Trier\!A_Trier_Audio'
flacroot = r'C:\Temp\Flac'

nf = 0
for filefp in list(get_all_files(root)):
    nf += 1
    ext = extension_part(filefp).lower()
    if ext == '.flac':
        np = filefp.replace(root, flacroot)
        nd = folder_part(np)
        os.makedirs(nd, exist_ok=True)
        shutil.move(filefp, nd)
        
print(nf, 'total files')
