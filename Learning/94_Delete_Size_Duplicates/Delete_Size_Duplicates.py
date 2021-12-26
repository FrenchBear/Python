# New version of Delete Size Duplicates, different from the one in 68_Rename_Temp_BD
# More complete
# 2021-12-16    PV

from collections import defaultdict
from typing import Iterable, List
from common_fs import *

# class DefaultDictList(dict): 
#     def __missing__(self, key):
#         value = list()
#         self[key] = value 
#         return value

dic: defaultdict[int, list[str]] = defaultdict(list)

source = r'W:\Livres'

for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    basename, ext = os.path.splitext(file)
    if ext.casefold() in ['.pdf', '.epub']:
        s = os.path.getsize(filefp)
        dic[s].append(filefp)

dups = [v for v in dic.values() if len(v)>1]
print(f'{len(dups)} size duplicates group(s) found.')
for lst in dups:
    print()
    for file in lst:
        #if 'a_trier' in file.casefold():
            #os.remove(file)
            print(f'del "{file}"')
