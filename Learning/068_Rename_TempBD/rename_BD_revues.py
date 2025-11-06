# rename_BD_revues.py
# Make sute that each segment starts with an uppercase
# In case of dup size, only keep the largest
#
# 2025-11-06    PV

# BEWARE - DON'T RUN ON FOLDER WHERE NUM DUPLICATES CAN BE JUSTIFIED

import os
from collections import defaultdict

from common_fs import get_files, file_size

source = r"W:\BD\Revues\Panache"
do_it = True

# Find issues dups
def delete_dup_issues():
    issueDic = defaultdict(list)
    files = [f for f in get_files(source) if f.casefold()!=("thumbs.db")]
    for file in files:
        ts = file.split(" - ")
        entry = issueDic[ts[1]].append(file)

    duplists = [dups for dups in issueDic.values() if len(dups) > 1]
    for dups in duplists:
        size_dup = []
        for dup in dups:
            l = file_size(os.path.join(source, dup))
            size_dup.append((l, dup))
        size_dup.sort(reverse=True)
        # print(size_dup)
        for l, dup in size_dup[1:]:
            print(f'del "{os.path.join(source, dup)}"')

def rename_segments():
    files = [f for f in get_files(source) if f.casefold()!=("thumbs.db")]
    for file in files:
        ts = file.split(" - ")

        updated = False
        for i in range(len(ts)):
            if 'a' <= ts[i][0] <= 'z':
                ts[i] = ts[i][0].upper() + ts[i][1:]
                updated = True
        if updated:
            newname = " - ".join(ts)
            print(file,"  ->  ", newname)
            if do_it:
                os.rename(os.path.join(source, file), os.path.join(source, newname))

rename_segments()
