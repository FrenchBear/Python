# getmaxsize.py
# From a bunch of versions of files identified by number, takes largest file
#
# 2024-01-05    PV
# 2024-01-17    PV      Optional call to syncrename

from collections import defaultdict
import re
import os
import shutil
from typing import Tuple
from common_fs import get_files, file_size, folder_exists, extension_part
from syncrename import sync_rename

NUMBER = re.compile(r'\D*(\d{2,3}[ABCDTabcdt]?)( |\.).*')

serie = "Tramp"
type = "Extra"

sources = [
    # r'C:\Downloads\A_Trier\!A_Trier_BD\dBD',
    # r'W:\BD\Revues\dBD',
    r"C:\Downloads\A_Trier\!A_Trier_BD" + '\\' + serie,
    r"\\terazalt\books\BD" + '\\' + type + '\\' + serie,
]

target = sources[-1] + '\\' + serie[0]  
series = serie
callSyncRename = True
doit = True

if doit:
    if (not folder_exists(target)):
        os.mkdir(target)
    else:
        if len([f for f in get_files(target) if extension_part(f).lower() == '.pdf']) > 0:
            print('Non-empty target folder:', target)
            os._exit(1)

issues: dict[str, list[Tuple[int, str]]] = defaultdict(list)
ln = 2
for source in sources:
    for file in get_files(source):
        filefp = os.path.join(source, file)
        ma = NUMBER.fullmatch(file)
        if not ma:
            if file.lower()!='thumbs.db':
                print('No matching number:', file)
        else:
            num = ma.group(1).lower()
            while num[0] == '0' and len(num) > 1:
                num = num[1:]
            if num.isdigit() and int(num) >= 100:
                ln = 3
            print(num, '->', file)
            issues[num].append((file_size(filefp), filefp))

for (n, l) in issues.items():
    print()
    print(n)
    for (s, f) in sorted(l, reverse=True):
        print('  ', s, f)
        if doit:
            if n.isdigit():
                ns = f'{int(n):02}' if ln == 2 else f'{int(n):03}'
            else:
                ns = n
                while len(ns) < ln + 1:
                    ns = '0' + ns
            shutil.copy(f, f'{target}\\{series} - {ns}.pdf')
        break

if callSyncRename:
    sync_rename(sources[-1], target)