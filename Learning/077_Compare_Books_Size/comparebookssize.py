# comparebookssize.py
# Eliminates duplicated books
# 2021-01-09    PV

from common_fs import *
from typing import Dict

doit = False

def isSameName1(file1: str, file2: str) -> bool:
    return file_part(file1).lower()==file_part(file2).lower()

def isSameName2(file1: str, file2: str) -> bool:
    (file1, file2) = (file_part(file1).lower(), file_part(file2).lower())
    if len(file1)>len(file2): (file1, file2) = (file2, file1)
    return file1 == file2[len(file2)-len(file1):]

source = r'W:\Livres\Informatique'
allfiles = list(get_all_files(source))
lref: Dict[int, list[str]] = {}
for file in allfiles:
    if not '!a_trier' in file.lower() and not 'Thumbs.db' in file:
        size = os.stat(file).st_size
        if size in lref:
            print(f'dup size {size}:\n  {lref[size][0]}\n  {file}\n')
            lref[size].append(file)
        else:
            lref[size] = [file]

# for file in allfiles:
#     if not '!a_trier' in file.lower() and not 'Thumbs.db' in file:
#         size = os.stat(file).st_size
#         if size in lref: # and isSameName2(file, lref[size]):
#             print(f'dup size and name {size}:\n  {lref[size]}\n  {file}\n')
#             print('del "'+file+'"')
#             if doit:
#                 os.remove(file)
