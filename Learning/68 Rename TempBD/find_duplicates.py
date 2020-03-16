import os
from collections import defaultdict
from typing import Iterable, List
from pprint import pprint
from common import *


#sources = [r'W:\BD\Classique', r'W:\BD\Adulte', r'W:\BD\Ancien', r'W:\BD\Extra', r'W:\BD\Comics', r'W:\TempBD\final']
sources = [r'W:\TempBD\raw', r'D:\Downloads\eMule\BD1']

DO_IT = True


def basename(filefp: str) -> str:
    _, file = os.path.split(filefp)
    basename, _ = os.path.splitext(file)
    return basename.lower()

class DefaultDictList(dict): 
    def __missing__(self, key):
        value = list()
        self[key] = value 
        return value

nf = 0
dg = defaultdict(DefaultDictList)       # defaultdict(defaultdict(list)) is illegal

def add_folder(ix:int, folderfp:str, group: str):
    global nf
    with os.scandir(folderfp) as it:
        entry: os.DirEntry
        for entry in it:
            if entry.is_file():
                nf += 1
                dg[group][entry.stat().st_size].append((ix,entry.path))
                # ds = dg[group]
                # l = ds[entry.stat().st_size]
                # l.append((ix,entry.path))

def add_source(ix:int, sourcefp:str):
    for folder in get_folders(sourcefp):
        folderfp = os.path.join(sourcefp, folder)
        add_folder(ix, folderfp, normalize_serie(folder))
    add_folder(ix, sourcefp, normalize_serie('!divers'))

for ix, sourcefp in enumerate(sources):
    add_source(ix, sourcefp)

print(f'{len(dg)} groups, {nf} files')

nd = 0
for group, ds in dg.items():
    dups = [v for v in ds.values() if len(v)>1]
    if dups:
        print(group)
        for dup in dups:
            dup.sort(key=lambda x:(x[0], basename(x[1])))
            print(' ', dup)
            nd += 1
            for ix,file in dup[1:]:
                print(f'    del "{file}"')
                if DO_IT:
                    os.remove(file)
        print()

print(f'{nd} duplicates deleted')
