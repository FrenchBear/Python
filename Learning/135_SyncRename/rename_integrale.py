# rename_integrale.py
#
# 2024-02-29    PV

import shutil
import os
from common_fs import file_exists, get_all_folders, get_files, file_part

source = r"W:\BD\Ancien"

for folderfp in get_all_folders(source):
    base = file_part(folderfp)
    i = os.path.join(folderfp, base + ' Intégrale') + '.pdf'
    i2 = (base + ' Intégrale').casefold()
    for file in get_files(folderfp):
        if file.casefold().startswith(i2) and file.casefold() != i2 + '.pdf':
            print(file)
            file2 = file.replace('Intégrale', '- Intégrale')
            shutil.move(os.path.join(folderfp, file), os.path.join(folderfp, file2))
