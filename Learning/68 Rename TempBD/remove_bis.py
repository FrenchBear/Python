# remove_bis.py
# Eliminates unneeded bis/ter/quater from the end of files
# 2020-03-16    PV

import os
import re
from typing import List

from common import *


source = r"W:\TempBD\final"
DO_IT = True

FILE_BIS = re.compile(r"(.*) - Bis\.pdf", flags=re.IGNORECASE)
FILE_TER = re.compile(r"(.*) - Ter\.pdf", flags=re.IGNORECASE)
FILE_QUATER = re.compile(r"(.*) - Quater\.pdf", flags=re.IGNORECASE)

nr = 0
def attempt_rename(original:str, base:str, *suffixes):
    global nr
    for suffix in suffixes:
        newname = base+suffix+'.pdf'
        if not os.path.exists(newname):
            _, newfile = os.path.split(newname)
            print(f'{original:<100} {newfile}')
            nr += 1
            if DO_IT:
                try:
                    os.rename(original, newname)
                except:
                    print('   *** Err')
            return
                

for file in get_all_files(source):
    if ma:=FILE_BIS.fullmatch(file):
        attempt_rename(file, ma.group(1), '')
    else:
        if ma:=FILE_TER.fullmatch(file):
            attempt_rename(file, ma.group(1), '', ' - Bis')
        else:
            if ma:=FILE_QUATER.fullmatch(file):
                attempt_rename(file, ma.group(1), '', ' - Bis', ' - Ter')

print(f'{nr} fichiers renommés')