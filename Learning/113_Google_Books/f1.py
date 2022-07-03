from collections import defaultdict
from common_fs import *
ds: dict[int, str] = {}
s = r'\\terax\books\Livres\A_Trier'
for filefp in get_all_files(s):
    size = file_size(filefp)
    if size in ds:
        print(f'\nSize {size} dup:\n{filefp}\n{ds[size]}')
    else:
        ds[size] = filefp

print(len(ds), 'files on source')

d = r'\\teraz\books\Livres\A_Trier'
for filefp in get_all_files(d):
    size = file_size(filefp)
    if size in ds:
        del ds[size]
    else:
        print(f'Size not fount do target: {size} {filefp}')

print('\nMissing books on dest:')
for k, v in ds.items():
    print(v)
    
