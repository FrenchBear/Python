
import os, sys, shutil
from collections import defaultdict
from typing import List

source = r'W:\TempBD\final'
DO_IT = True

folders = set()
series = defaultdict(set)
for root, subs, files in os.walk(source):
    for folder in subs:
        folders.add(folder.lower())
    for file in files:
        segments = file.split(' - ')
        serie = segments[0].lower()
        series[serie].add(file)
    break

for serie in series.keys():
    to_move = False
    if serie in folders:
        to_move = True
    else:
        to_move = len(series[serie])>=3
    if to_move:
        for file in series[serie]:
            segments = file.split(' - ')
            folder = segments[0]
            if not folder.lower() in folders:
                print(f'mkdir "{folder}"')
                if DO_IT:
                    os.mkdir(os.path.join(source, folder))
                folders.add(folder.lower())
            print(f'move "{file}" "{folder}"')
            if DO_IT:
                os.rename(os.path.join(source, file), os.path.join(source, folder, file))
