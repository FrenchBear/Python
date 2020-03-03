from collections import Counter

import os, sys
import re
import unicodedata
import json
from typing import List, Iterable
from collections import Counter

source = r'W:\TempBD'

def get_files(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

def get_all_files(path: str) -> Iterable[str]:
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

def clean_file_name(s: str) -> str:
    res = ''.join(c for c in s if c in " ,.%!#&@$()[]¿°·½-+'" or unicodedata.category(c) in ['Ll', 'Lu', 'Nd'])
    return res

REBUILDFILESLIST = False

if REBUILDFILESLIST:
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



cnt = Counter()
for fullpath in files:
    path, file = os.path.split(fullpath)
    basename, ext = os.path.splitext(file)
    s = re.findall(r"[\w']+", basename)
    cnt.update(s)

for (s, c) in cnt.most_common(100):
    if not re.fullmatch(r'''\d+''', s):
        print(f"{c:4} {s}")
#print(cnt.most_common(10))
