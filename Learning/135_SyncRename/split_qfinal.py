# split_qfinal.py
# Moves BD2 folder with no match to QFinal.New
#
# 2024-02-02    PV

import re
import os
import shutil
from common_fs import get_folders, get_all_folders, file_part

# with open(r'c:\Temp\all_folders.txt', "w", encoding='UTF-8') as out:
#     for ffp in  get_all_folders(r'W:\BD'):
#         f = file_part(ffp)
#         out.write(f+'\n')

existing_folders = set()
with open(r'c:\Temp\all_folders.txt', "r", encoding='UTF-8') as inp:
    for f in inp:
        existing_folders.add(f.strip('\n').casefold())

nn = 0
for f in get_folders(r'W:\BD2\QFinal'):
    if f.casefold() not in existing_folders:
        print(f)
        nn += 1
        shutil.move(os.path.join(r'W:\BD2\QFinal', f), os.path.join(r'W:\BD2\QFinal.New', f))
print(nn)
