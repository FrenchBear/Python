# analyse_mp3.py
# Analyse mp3, sorting files using bitrate
#
# 2023-12-19    PV

from collections import Counter
import eyed3    # type: ignore
import logging
import io
import os
import shutil
from common_fs import get_all_files, folder_part, extension_part

root = r'C:\Temp\A_Trier Brut'

log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO)

co: Counter = Counter()

def get_bit_rate(file: str) -> int:
    af = eyed3.core.load(file)
    br = af.info.bit_rate[1]        # type: ignore
    if br == 160:
        print(file)
    return br


nf = 0
for filefp in list(get_all_files(root)):
    nf += 1
    ext = extension_part(filefp).lower()
    if ext == '.db':
        continue
    if ext == '.mp3':
        ext = '.mp3-' + str(get_bit_rate(filefp))
    co.update([ext])

    if ext.startswith('.mp3') or ext == '.flac':
        np = filefp.replace('A_Trier Brut', 'A_Trier\\' + ext[1:])
        nd = folder_part(np)
        os.makedirs(nd, exist_ok=True)
        shutil.move(filefp, nd)
        
print(nf, 'total files')
print(co)
