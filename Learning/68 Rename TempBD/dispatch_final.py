import os, sys, shutil
from collections import defaultdict
from typing import List

from common import *


source = r'W:\TempBD\final'
DO_IT = True


for root, folders, files in os.walk(source):
    break

series = defaultdict(set)
for folder in folders:
    serie = normalize_serie(folder)
    series[serie].add(folder)

# Folders to merge
for k in series.keys():
    if len(series[k])>1:
        print(series[k])

# Move files

# Group files
dicsf = defaultdict(list)
for file in files:
    basename, ext = os.path.splitext(file)
    segments = basename.split(' - ')
    serie = normalize_serie(segments[0])
    dicsf[serie].append(file)

print(f'Fichiers groupés en {len(dicsf)} séries')

existing = 0
newserie = 0
to_create = 0
for serie in dicsf.keys():
    files = dicsf[serie]
    if serie in series.keys():
        existing += 1
        targetfolderfp = os.path.join(source, series[serie].pop())
        print(f'Merge into {targetfolderfp}')
        for file in files:
            sourcefilefp = os.path.join(source, file)
            targetfilefp = os.path.join(targetfolderfp, file)
            to_move = True
            if os.path.exists(targetfilefp):
                if os.path.getsize(sourcefilefp) == os.path.getsize(targetfilefp):
                    to_move = False
                    os.remove(sourcefilefp)
                else:
                    basename, ext = os.path.splitext(file)
                    for suffix in ['Bis', 'Ter', 'Quater', '5', '6']:
                        targetfilefp = os.path.join(targetfolderfp, basename+' - '+suffix+ext)
                        if not os.path.exists(targetfilefp):
                            break
            if to_move:
                print(f'  {sourcefilefp}  ->  {targetfilefp}')
                if DO_IT:
                    try:
                        os.rename(sourcefilefp, targetfilefp)
                    except:
                        print(f"*** Err renaming {sourcefilefp} into {targetfilefp}")

    else:
        newserie += 1
        if len(files)>=3:
            to_create += 1
            basename, ext = os.path.splitext(files[0])
            segments = basename.split(' - ')
            newfolder = segments[0]
            newfolderfp = os.path.join(source, newfolder)
            print(f'mkdir "{newfolderfp}"')
            if DO_IT:
                os.mkdir(newfolderfp)
            for file in files:
                sourcefilefp = os.path.join(source, file)
                targetfilefp = os.path.join(newfolderfp, file)
                print(f'move "{sourcefilefp}" "{targetfilefp}"')
                if DO_IT:
                    os.rename(sourcefilefp, targetfilefp)

print(f'{existing} séries existantes, {newserie} nouvelles séries dont {to_create} à créer')
