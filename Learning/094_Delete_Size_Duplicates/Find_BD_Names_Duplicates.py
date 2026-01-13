# Find_BD_Names_Duplicates.py
# Cleanup of BD pack
#
# 2026-01-12    PV

import os
import shutil
from common_fs import get_files, file_size

source_ref = r'W:\BD\Auteurs\Wolinski'
source_check = r'C:\Users\Pierr\Downloads\A_Trier\!A_Trier_BD'

ref = set(f.casefold() for f in get_files(source_ref))

ndup = 0
ndel = 0
ncp = 0
for file in list(get_files(source_check)):
    if file.casefold() in ref:
        print(file)
        ndup += 1
        if file_size(os.path.join(source_check, file)) < 1.1*file_size(os.path.join(source_ref, file)):
            os.rename(os.path.join(source_check, file), os.path.join(r'C:\Users\Pierr\Downloads\A_Trier\!A_Trier_BD\ToDel', file))
            ndel += 1
        else:
            shutil.move(os.path.join(source_ref, file), os.path.join(r'C:\Users\Pierr\Downloads\A_Trier\!A_Trier_BD\Replaced', file))
            shutil.move(os.path.join(source_check, file), os.path.join(source_ref, file))
            ncp += 1

print('dups:', ndup)
print('to del:', ndel)
print('replaced:', ncp)
