# Musique à trier
#
# 2023-04-07    PV

from collections import Counter
import shutil
from common_fs import *

source = r'C:\Temp\LP'
doit = True

# extensions = Counter()
# extensions.update(extension_part(filefp).lower() for filefp in get_all_files(source))
# print(extensions.most_common())

files = [filefp for filefp in get_all_files(source)]
for filefp in files:
    path, file = os.path.split(filefp)
    if file[0] != file[0].upper():
        print(file)
        newfile = file[0].upper()+file[1:]
        if doit:
            os.rename(filefp, os.path.join(path, newfile))
