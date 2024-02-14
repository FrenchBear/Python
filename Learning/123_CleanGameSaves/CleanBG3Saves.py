# CleanBG3Saves.py
# Keep a limited number of saves for Baldur's Gate 3
#
# 2024-02-14    PV

from datetime import datetime, timedelta
import os
import shutil
from common_fs import folder_exists, get_folders

source = r"C:\Users\Pierr\AppData\Local\Larian Studios\Baldur's Gate 3\PlayerProfiles\Public\Savegames\Story"
source2 = r'C:\Users\Public\Documents\Steam\RUNE\1086940\remote\_save_public\savegames\story'       # Empty folders
spacemin = timedelta(hours=1)       # Keep one save per spacemin
doit = True

# Build dic of files indexed by datetime of last modification
dicTimeFile: dict[datetime, str] = {}
for folderfp in get_folders(source, True):
    mt = datetime.fromtimestamp(os.stat(folderfp).st_mtime)
    dicTimeFile[mt] = folderfp

print(len(dicTimeFile))

nskip = 0
nkeep = 0
ndel = 0
last = datetime.today() + timedelta(days=1)     # Fake last time kept, somewhere in the future
sortedTime = sorted(dicTimeFile.keys(), reverse=True)
start = sortedTime[0] - timedelta(days=1)     # From the last save, keep everything for the last 24 hours
for t in sortedTime:
    if t > start:
        status = 'Skip'
        nskip += 1
    elif last - t > spacemin:
        status = 'Keep'
        nkeep += 1
        last = t
    else:
        status = 'Delete'
        ndel += 1
        if doit:
            shutil.rmtree(dicTimeFile[t])
            # file2 = dicTimeFile[t].replace(source, source2)
            # if file_exists(file2):
            #     os.remove(file2)
            #     status = 'Delete+2'
    print(f'{t:%Y-%m-%d %H:%M:%S}  {dicTimeFile[t]}  {status}')

print()
ndel2 = 0
for folder in get_folders(source2):
    folderfp_source = os.path.join(source, folder)
    if not folder_exists(folderfp_source):
        print('rmdir', folder)
        ndel2 += 1
        if doit:
            folderfp = os.path.join(source2, folder)
            shutil.rmtree(folderfp)

if not doit:
    print('No action mode')
print('Skip:', nskip, '  Kept:', nkeep, '  Deleted:', ndel, '  Del2', ndel2)
