# renYgg.py
# Reformat book names of ygg packs where editor is put first
# deboeck Biochimie 3ed.pdf
# ->
# Biochimie (4ed, X) - [Deboeck] - X.pdf
#
# In regex, .+? is the non-greedy form of .+
#
# 2022-06-15    PV
# 2022-06-30    PV      Accept any char but space in editor name; replace _ by space in editor name

from common_fs import *
from typing import Dict
import os
import shutil
import re

source = r'W:\Livres\A_Trier\new\Fr'
ED = re.compile(r'^([^ ]+) (.+?)( (\d+)ed)?\.pdf$')
doit = True


def FirstUpper(s: str) -> str:
    return s[0].upper() + s[1:]


rencount = 0
for file in list(get_files(source)):
    if file.lower().endswith('.pdf'):
        basename, ext = os.path.splitext(file)
        ma = ED.match(file)
        if ma:
            #print(f'«{ma.group(1)}» «{ma.group(2)}» «{ma.group(3)}» «{ma.group(4)}»')
            nn = FirstUpper(ma.group(2))
            if ma.group(4):
                match ma.group(4):
                    case '1': sed = '1st'
                    case '2': sed = '2nd'
                    case '3': sed = '3rd'
                    case _:   sed = ma.group(4) + 'th'
                nn += f" ({sed} ed, X)"
            nn += f" - [{FirstUpper(ma.group(1)).replace('_',' ')}] - X.pdf"
            print(file, ' -> ', nn)
            rencount += 1
            if doit:
                os.rename(os.path.join(source, file), os.path.join(source, nn))
        else:
            breakpoint()
            pass

print(rencount, ' fichier(s) renommé(s)')
