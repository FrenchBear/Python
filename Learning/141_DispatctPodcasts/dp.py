# dp.py
# Dispatch podcasts in a separate folder per month
#
# 2024-11-04    PV      First version

import os.path
import shutil
from common_fs import get_files

source = r'C:\MusicOD\Humour\Matthieu Noël\Matthieu Noël - France Inter - Le billet de Matthieu Noël'
dest = r'C:\Temp\MN'
doit = True

files = [filefp for filefp in get_files(source)]

for file in files:
    ts = file.split(" - ")
    assert len(ts) == 3
    month = ts[1][:7]
    print(month)
    target = os.path.join(dest, month)
    print(file, ' --> ', target)
    if doit:
        if not os.path.exists(target):
            os.makedirs(target)
        shutil.move(os.path.join(source, file), target)
