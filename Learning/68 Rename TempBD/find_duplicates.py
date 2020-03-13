
import os, sys, shutil
from collections import defaultdict
from typing import List, TextIO

from common import *


source = r'W:\TempBD\archives\cbrn'

DO_IT = True


# Chemin complet de tous les fichiers à partir d'une racine
def get_all_folders(path: str) -> Iterable[str]:
    for root, folders, _ in os.walk(path):
        for folder in folders:
            yield os.path.join(root, folder)

ds = defaultdict(set)

for folder in get_all_folders(source):
    with os.scandir(folder) as it:
        entry: os.DirEntry
        for entry in it:
            if entry.is_file():
                ds[entry.stat().st_size].add(entry.path)

dups = [(k,v) for k,v in ds.items() if len(v)>1]
print(dups)
