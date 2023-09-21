# CleanFallout3Saves.py
# Keep a limited number of saves for Fallout 3
#
# 2023-09-21    PV

from datetime import datetime, timedelta
import os
from common_fs import get_files

source = r'C:\DocumentsOD\Doc WOTAN\My Games\Fallout3\Saves'
spacemin = timedelta(hours=1)       # Keep one save per spacemin
doit = True

# Build dic of files indexed by datetime of last modification
dicTimeFile: dict[datetime, str] = {}
for file in get_files(source):
    if file.startswith('Save') and file.endswith('.fos'):
        filefp = os.path.join(source, file)
        mt = datetime.fromtimestamp(os.stat(filefp).st_mtime)  # , tz=timezone.utc)
        dicTimeFile[mt] = filefp

print(len(dicTimeFile))

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
    print(f'{t:%Y-%m-%d %H:%M:%S}  {dicTimeFile[t]}  {status}')

if not doit:
    print('No action mode')
print('Skip:', nskip, '  Kept:', nkeep, '  Deleted:', ndel)
