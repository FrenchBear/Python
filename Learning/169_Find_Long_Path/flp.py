# flp.py
# Find files longer than lmax char and truncates them
#
# 2025-12-13    PV

from collections import defaultdict
import os
import sys
from common_fs import get_all_files

root = r'd:\Pierre\HomeShared\MusicPV'
lmax = 210

dd = defaultdict(list)
for filefp in get_all_files(root):
    path, file = os.path.split(filefp)
    basename, ext = os.path.splitext(file)

    if len(filefp) > lmax:
        itr = lmax - len(path) - 1 - len(ext)
        if itr <= 0:
            breakpoint()
        while basename[itr] != ' ':
            itr -= 1
        if itr <= 0:
            breakpoint()
        tr = os.path.join(path, basename[:itr] + ext)
        dd[tr].append((path, basename, ext))

# Check that no two truncated files would get the same name
pb = False
for tr in dd.keys():
    if len(dd[tr]) > 1:
        print("Dup trunc")
        pb = True
if pb:
    sys.exit(1)

print(len(dd), 'filename(s) to truncate')

for nn in dd.keys():
    path, basename, ext = dd[nn][0]
    on = os.path.join(path, basename + ext)
    print(on)
    print(nn)
    print()
    os.rename(on, nn)
