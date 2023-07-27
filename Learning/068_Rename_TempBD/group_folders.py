import os
import re

from common_fs import get_folders
from common import merge_folders

source = r"W:\TempBD\archives"
# source = r'W:\TempBD\archives\hybrid.pdf'
DO_IT = True


# TO_RENAME_RE = re.compile(r'(.*) - \d\d( |-)\d\d.*')
TO_RENAME_RE = re.compile(r"(.*?) - (.*)")

nf = 0  # Number of folders
nfm = 0  # Number of files moved
ndn = 0  # Number of duplicates name, renamed
nds = 0  # number of duplicates name+size, not moved
for sourcefolder in get_folders(source):
    if ma := TO_RENAME_RE.fullmatch(sourcefolder):
        nf += 1
        sourcefolderfp = os.path.join(source, sourcefolder)
        targetfolder = ma.group(1)
        if " - " in targetfolder:
            breakpoint()
        print(f"{sourcefolder:<80} {targetfolder}")
        targetfolderfp = os.path.join(source, targetfolder)
        if not os.path.exists(targetfolderfp):
            if DO_IT:
                os.mkdir(targetfolderfp)
        nfm1, ndn1, nds1 = merge_folders(sourcefolderfp, targetfolderfp, DO_IT)
        nfm += nfm1
        ndn += ndn1
        nds += nds1

print(
    f"{nf} dossiers groupés, {nfm} fichiers traités, {ndn} doublons de noms, {nds} doublons de nom+taille"
)
