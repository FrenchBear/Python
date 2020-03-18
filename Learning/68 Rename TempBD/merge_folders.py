import os
from typing import List

from common import *


source = r'W:\TempBD\archives\cbr1.pdf'
target = r'W:\TempBD\final'
DO_IT = True


folders: List[str]
_1, folders, _2 = next(os.walk(source))

nf = 0
nmove = nmerge = 0
tfm = tfdn = tfds = 0

# Merge subfolders
for sourcefolder in folders:
    nf += 1
    sourcefolderfp = os.path.join(source, sourcefolder)
    targetfolderfp = os.path.join(target, sourcefolder)
    print(f'{sourcefolder} ', end='')
    if not os.path.exists(targetfolderfp):
        nmove += 1
        print('Move')
        if DO_IT:
            os.rename(sourcefolderfp, targetfolderfp)
    else:
        nmerge += 1
        print('Merge')
        nfm, ndn, nds = merge_folders(sourcefolderfp, targetfolderfp, DO_IT)
        tfm += nfm
        tfdn += ndn
        tfds += nds

# Merge individual files at top level
nfm, ndn, nds = merge_folders(source, target, DO_IT)
tfm += nfm
tfdn += ndn
tfds += nds


print(f'{nf} dossiers, {nmove} déplacés, {nmerge} fusionnés')
print(f'{tfm} fichiers déplacés, {tfdn} renommés, {tfds} doublons ignorés')
