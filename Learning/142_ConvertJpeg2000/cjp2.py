# cjp2.py
# Convert jpeg2000 files to png
#
# 2024-11-06    PV      First version

import os.path
import subprocess
from common_fs import get_files, get_folders

magick=r'C:\Program Files\ImageMagick-7\magick.exe'
sourceFolder = r'C:\Temp\JP2'
destFolder = r'C:\Temp\PNG'
doit = True

def convert(sf:str, tf: str):
    if not os.path.exists(tf) and doit:
        os.makedirs(tf)
    for file in get_files(sf):
        sourceFile = os.path.join(sf, file)
        destFile = os.path.join(tf, file).replace('.jp2', '.png')
        print(sourceFile, ' --> ', destFile)
        if doit:
            p = subprocess.run([magick, sourceFile, destFile])
            print('subprocess ->', p)

for folder in get_folders(sourceFolder):
    convert(os.path.join(sourceFolder, folder), os.path.join(destFolder, folder))
