import os, sys
from typing import List, Iterable
from shutil import copyfile


source = r'e:\eMuleTemp.bak'
target = r'e:\eMuleTemp'

def get_files(source: str) -> List[str]:
    return list([f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))])

def get_all_files(path: str) -> Iterable[str]:
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

for fullpath in get_all_files(source):
    path, file = os.path.split(fullpath)
    p = file.find('.')
    n = int(file[:p])
    if n%2==0:
        print(n, file)
        #copyfile(fullpath, os.path.join(target, file))
        os.rename(fullpath, os.path.join(target, file))
