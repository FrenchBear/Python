# checkisolated.py
# Chcek if one-shot BD files in W:\BD2\ZZZ Misc are also found in Divers folders
#
# 2024-02-12    PV

import re
import os
import shutil
from typing import Tuple
from common_fs import get_files, file_size, folder_exists, file_exists

FROMSERIES = re.compile(r'(.*) - (\d{2,3}[ABCDTabcdt]?)(?: - (.+))?\.pdf')

d: dict[str, tuple[int, str]] = {}

def AddOS(folder: str):
    print('Adding', folder)
    for file in get_files(folder):
        if file != 'Thumbs.db':
            filefp = os.path.join(folder, file)
            print('.', end='')
            if file.casefold() in d:
                print('Dup', file)
            d[file.casefold()] = (file_size(filefp), folder)
    print()


sources = [r'W:\BD\Adulte', r'W:\BD\Ancien', r'W:\BD\Classique', r'W:\BD\Extra']
for source in sources:
    AddOS(os.path.join(source, '!Divers'))

def copy_file(filefp: str, folder: str):
    if not folder.startswith(r'W:\BD'):
        breakpoint()
    folder = folder.replace(r'W:\BD', r'W:\BD3')
    if not folder_exists(folder):
        os.makedirs(folder)
    shutil.move(filefp, folder)

folder = r'W:\BD2\ZZZ Misc'
nt = 0  # number total
nn = 0  # number no match and not a series
nb = 0  # number better
ns = 0  # number smaller
nsn = 0  # number of series not found
nsf = 0  # number of series found
nsfn = 0  # number of series found, but file not found
nsfb = 0  # number of series found, file found, ZZZ Misc is better
nsfs = 0  # number of series found, file found, ZZZ Misc is smaller
for file in get_files(folder):
    if file != 'Thumbs.db':
        nt += 1
        filefp = os.path.join(folder, file)
        if file.casefold() in d:
            s2 = file_size(filefp)
            s = d[file.casefold()][0]
            if s2 > 1.05 * s:
                print('B', end='')
                nb += 1
                copy_file(filefp, d[file.casefold()][1])
            else:
                print('_', end='')
                ns += 1
                copy_file(filefp, r'W:\BD\OS_smaller')
        else:
            ma = FROMSERIES.fullmatch(file)
            if ma:
                series = ma.group(1)
                issue = ma.group(2)
                title = ma.group(3) if ma.group(3) else ''

                found = False
                for source in sources:
                    fs = os.path.join(source, series)
                    if folder_exists(fs):
                        break
                else:
                    print('_', end='')
                    nsn += 1
                    copy_file(filefp, r'W:\BD\Not_found')
                    continue

                # Series found
                nsf += 1
                if file_exists(os.path.join(fs, file)):
                    s2 = file_size(filefp)
                    s = file_size(os.path.join(fs, file))
                    if s2 > 1.05 * s:
                        print('S', end='')
                        nsfb += 1
                        copy_file(filefp, fs)
                    else:
                        print('s', end='')
                        nsfs += 1
                        copy_file(filefp, r'W:\BD\Series_found_smaller')
                else:
                    print('*', end='')
                    nsfn += 1
                    copy_file(filefp, r'W:\BD\Series_not_found')
            else:
                print('n', end='')
                nn += 1
                copy_file(filefp, r'W:\BD\OS_not_found')
                continue


print()
print('Total', nt)
print('No match', nn)
print('Better', nb)
print('Smaller', ns)
print('Not found, series not found', nsn)
print('Series found', nsf)
print('Series found, file not found', nsfn)
print('Series found, file better', nsfb)
print('Series found, file smaller', nsfs)
