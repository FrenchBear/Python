# clean_files.py
# Remove unsuppportyed/hidden characters from BD files names
# 2020-03-05    PV

import os
import sys
import re
from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict, Iterable
import json
import re
import unicodedata

from common import *

DO_IT = False

source = r'D:\Downloads\eMule\BD1'
#source = r'W:\TempBD'

def clean_files():
    nf = 0
    nr = 0
    with open(r'cleaning.txt', mode='w', encoding='utf-8') as out:
        for fullpath in get_all_files(source):
            nf += 1
            path, file = os.path.split(fullpath)
            basename, ext = os.path.splitext(file)
            clean_name = clean_file_name(file)
            if file!=clean_name:
                nr += 1
                print(f'{file:<100} -> {clean_name}')
                out.write(f'{file:<100} -> {clean_name}\n')
                if DO_IT:
                    try:
                        os.rename(fullpath, os.path.join(path, clean_name))
                    except:
                        print("*** Err in folder "+path)
    if not DO_IT:
        print("No action: ", end='')
    print(f'{nf} fichiers analysés, {nr} renommé(s)')

clean_files()
