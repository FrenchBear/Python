# renf.py
# Rename folders 25ExcitingComputerGamesInBasicForAllAges1983_jp22 -> 25 Exciting Computer Games In Basic For AllA ges 1983

import os
from common_fs import get_folders

source = r'C:\Temp\PNG'
doit = True

def rename(s: str) -> str:
    nn = ''
    for c in s.removesuffix('_jp22').removesuffix('_jp2'):
        if c == '1':
            nn += ' -'
        if 'A' <= c <= "Z" or c == '1':
            nn += ' '
        nn += c
    return nn


for folder in list(get_folders(source)):
    nn = rename(folder)
    print(f'{folder:<70} {nn}')
    originalName = os.path.join(source, folder)
    newName = os.path.join(source, nn)
    if doit:
        os.rename(originalName, newName)
