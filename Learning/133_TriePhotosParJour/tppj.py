# Trie photos par jour
#
# 2023-12-15    PV

# from collections import Counter
import os
import re
import shutil
from common_fs import get_files, folder_exists

source = r'C:\Users\Pierr\OneDrive\PicturesODPerso\2023\2023-12-14 Phone dump Photos'
target = r'C:\Users\Pierr\OneDrive\PicturesODPerso\2023\Temp'
doit = True

IMAGE = re.compile(r'IMG_(\d\d\d\d)(\d\d)(\d\d)_(\d\d\d\d\d\d)(_\d)?\.jpg')

nf = 0
nma = 0
for f in get_files(source):
    nf += 1
    ma = IMAGE.match(f)
    if ma:
        nma += 1
        y = ma.group(1)
        m = ma.group(2)
        d = ma.group(3)
        tf = os.path.join(target, f'{y}-{m}-{d}')
        if not folder_exists(tf):
            os.mkdir(tf)
        if doit:
            shutil.move(os.path.join(source, f), tf)
            print(f)

print(nf, nma)
