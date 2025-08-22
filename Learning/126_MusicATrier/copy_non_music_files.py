# copy_non_music_files.py
# Goldwave batch processing does not copy non-music files
#
# 2025-07-28    PV

from common_fs import get_all_files, extension_part, folder_part
import shutil
import os

source = r'\\terazalt\music\Pierre\MusicExtra\Michel Legrand - Large'
destination = r"C:\Temp\MP3320"
doit = True

for filefp in get_all_files(source):
    ext = extension_part(filefp ).casefold()
    if not ext in ['.flac', '.mp3', '.db', '.log']:
        destfp = filefp.replace(source, destination).replace('.jpeg', '.jpg')
        print(filefp, "->", destfp)
        if doit:
            os.makedirs(folder_part(destfp), exist_ok=True)
            shutil.copy2(filefp, destfp)
