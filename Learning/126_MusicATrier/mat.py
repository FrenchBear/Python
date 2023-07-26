# Musique à trier
#
# 2023-04-07    PV

from collections import Counter
import shutil
from common_fs import *
import os

source = r'\\terazalt\books\Autres\Livres Large avant nettoyage'
doit = False

# extensions = Counter()
# extensions.update(extension_part(filefp).lower() for filefp in get_all_files(source))
# print(extensions.most_common())

files = [filefp[len(source)+1:] for filefp in get_all_files(source)]
totf = len(files)
found = 0
notfound = 0

for filer in files:
    filefp = os.path.join(r'\\terazalt\books\Livres', filer)
    if file_exists(filefp):
        found += 1
        os.remove(os.path.join(source, filer))
    else:
        notfound += 1

print('total:', totf, '  found:', found, '  not found:', notfound)
