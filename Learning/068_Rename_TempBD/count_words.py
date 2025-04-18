# Compte les mos les plus fréquents dans les noms de BD
# 2020-05-04    PV

import os
import re
import json
from collections import Counter
from typing import Counter as TCounter

from common_fs import get_all_files


source = r'W:\TempBD'


REBUILD_FILES_LIST = True

if REBUILD_FILES_LIST:
    print("Reading files hierarchy...")
    files = list(get_all_files(source))
    print(f"Wrting {len(files)} records in cache filesH.json")
    with open(r'filesH.json', 'w', encoding='utf8') as outfile:
        json.dump(files, outfile, indent=4, ensure_ascii=False)
    print("Done.")
else:
    with open(r'filesH.json', 'r', encoding='utf-8') as infile:
        files = json.load(infile)
    print(f"Loaded {len(files)} records from filesH.json")


cnt: TCounter[str] = Counter()
for fullpath in files:
    path, file = os.path.split(fullpath)
    stem, ext = os.path.splitext(file)
    s = re.findall(r"[\w']+", stem)
    cnt.update(s)

word: str
c: int
for (word, c) in cnt.most_common(200):
    if not re.fullmatch(r'''\d+''', word):
        print(f"{c:4} {word}")
#print(cnt.most_common(10))
