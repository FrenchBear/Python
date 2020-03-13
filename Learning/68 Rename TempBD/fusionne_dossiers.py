
import os, sys, shutil
import re
from typing import List, TextIO

from common import *


source = r'W:\TempBD\archives\archiven.pdf'
target = r'W:\TempBD\final'

DO_IT = True


nf = 0
nmove = 0
nmerge = 0
for sourcefolder in get_folders(source):
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
        merge_folders(sourcefolderfp, targetfolderfp, DO_IT)

print(f'{nf} dossiers, {nmove} déplacés, {nmerge} fusionnés')
