import os
import shutil
from collections import defaultdict
from common_fs import get_files

source = r"W:\BD2\Not_found"
target = r"W:\BD2\Series"

d: dict[str, list[str]] = defaultdict(list)

for file in get_files(source):
    p = 0
    try:
        p = file.index(' - ')
    except:
        p = 0
    if p>0:
        series = file[:p]
        #print(series)
        d[series].append(file)

for k, v in d.items():
    if len(v)>1:
        print(len(v), k)
        folder = os.path.join(target, k)
        os.mkdir(folder)
        for f in v:
            shutil.move(os.path.join(source, f), folder)