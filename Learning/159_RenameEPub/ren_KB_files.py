from collections import defaultdict
import os
from common_fs import get_all_files

source = r"D:\Kaforas\HomeSharedKB"

df = defaultdict(list)
nlf = 0
lfl = 100
for filefp in get_all_files(source):
    path, file = os.path.split(filefp)
    basename, ext = os.path.splitext(file)

    if len(basename) > lfl:
        nlf += 1
        #print(f"{len(file):>3}:",filefp)
        tr = basename[:lfl]
        com = os.path.join(path, tr)
        df[com].append((path, basename, ext))

pb = False
for com in df.keys():
    if len(df[com])>1:
        pb = True
        print()
        print(len(df[com]),'truncated:')
        for (path, basename, ext) in df[com]:
            print("  ", os.path.join(path, basename+ext))
        print()
if pb:
    breakpoint()

def qp(s: str) -> str: return '"'+s+'"'

for com in df.keys():
    (path, basename, ext) = df[com][0]
    on = os.path.join(path, basename+ext)
    nb = com.rstrip()
    while nb[-1]==',' or nb[-1]=='.' or nb[-1]=='-':
        nb = nb[:-1]
    nn = nb+ext
    print("ren", qp(on), qp(nn))
    os.rename(on, nn)

print()
print('Files with', lfl, 'chars or more:', nlf)
