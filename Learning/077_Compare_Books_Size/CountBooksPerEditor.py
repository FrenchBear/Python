# CountBooksPerEditor.py
# Just count files per editor
# For a more cmplete code, see project 047_Check_Books_Editors
#
# 2022-07-14    PV

from collections import Counter
from common_fs import *
from typing import Dict
import os

source = r'W:\Livres\A_Trier\Misc'

d = Counter()
for filefp in list(get_all_files(source)):
    if filefp.lower().endswith('.pdf'):
        folder, file = os.path.split(filefp)
        basename, ext = os.path.splitext(file)
        ts = basename.split(' - ')
        if ts[1].startswith('['):
            ed = ts[1][1:-1]
            d.update([ed])

print(d.most_common(10))
