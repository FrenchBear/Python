# remove_bis.py
# Eliminates unneeded bis/ter/quater from the end of files
# 2020-03-16    PV

import os
import re
from typing import List

from common import *


#source = r"D:\Downloads\eMule\BD1"
source = r"W:\TempBD\final"
DO_IT = True


FILE_BIS = re.compile(r"(.*) - Bis", flags=re.IGNORECASE)
FILE_TER = re.compile(r"(.*) - Ter", flags=re.IGNORECASE)
FILE_QUATER = re.compile(r"(.*) - Quater", flags=re.IGNORECASE)

nfiles = nfolders = 0


def attempt_rename(original: str, base: str, ext: str, *suffixes: List[str]) -> int:
    for suffix in suffixes:
        newname = base+suffix+ext
        if not os.path.exists(newname):
            _, newfile = os.path.split(newname)
            print(f'{original:<100} {newfile}')
            if DO_IT:
                try:
                    os.rename(original, newname)
                except:
                    print('   *** Err')
                    return 0
            return 1
    return 0


for filefp in get_all_files(source):
    basename, ext = os.path.splitext(filefp)
    if ma:=FILE_BIS.fullmatch(basename):
        nfiles += attempt_rename(filefp, ma.group(1), ext, '')
    else:
        if ma:=FILE_TER.fullmatch(basename):
            nfiles += attempt_rename(filefp, ma.group(1), ext, '', ' - Bis')
        else:
            if ma:=FILE_QUATER.fullmatch(basename):
                nfiles += attempt_rename(filefp, ma.group(1), ext, '', ' - Bis', ' - Ter')

print(f'{nfiles} fichiers renommés')


for folderfp in get_all_folders(source):
    if ma:=FILE_BIS.fullmatch(folderfp):
        newnamefp = ma.group(1)
        if not os.path.exists(newnamefp):
            _, newfolder = os.path.split(newnamefp)
            nfolders += 1
            print(f'{folderfp:<100} {newfolder}')
            if DO_IT:
                try:
                    os.rename(folderfp, newnamefp)
                except:
                    print('   *** Err')

print(f'{nfolders} dossiers renommés')
