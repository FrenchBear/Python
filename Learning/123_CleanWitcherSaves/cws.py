# CleanWitcherSaves
# Keep a limited number of saves
#
# 2023-02-18    PV

from datetime import datetime, timezone, timedelta
import os
from common_fs import *

source = r'C:\Users\Pierr\Documents\The Witcher 3\gamesaves'
spacemin = timedelta(hours=1)
doit = True

# Build dic of files indexed by datetime of last modification
dicTimeFile: dict[datetime, str] = {}
for file in get_files(source):
    if file.startswith('ManualSave') and file.endswith('.sav'):
        filefp = os.path.join(source, file)
        mt = datetime.fromtimestamp(os.stat(filefp).st_mtime)  # , tz=timezone.utc)
        dicTimeFile[mt] = filefp

nskip = 0
nkeep = 0
ndel = 0
last = datetime.today() + timedelta(days=1)     # Fake last time kept, somewhere in the future
sortedTime = sorted(dicTimeFile.keys(), reverse=True)
start = sortedTime[0]-timedelta(days=1)     # From the last save, keep everything for the last 24 hours
for t in sortedTime:
    if t > start:
        status = 'Skip'
        nskip += 1
    elif last-t > spacemin:
        status = 'Keep'
        nkeep += 1
        last = t
    else:
        status = 'Delete'
        ndel += 1
        if doit:
            os.remove(dicTimeFile[t])
            os.remove(dicTimeFile[t].replace('.sav', '.png'))
    print(f'{t:%Y-%m-%d %H:%M:%S}  {dicTimeFile[t]}  {status}')

if not doit:
    print('No action mode')
print('Skip:', nskip, '  Kept:', nkeep, '  Deleted:', ndel)
