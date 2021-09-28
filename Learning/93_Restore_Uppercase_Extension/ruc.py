# Restore uppercase extension
# After forcing lowercase extension on all files on \\teraz\system, I think it was too brutal and
# old files in Archives may keep an uppercase extension, especially files of 1-8 characters with
# no space, no lowercase, such as STARBAR3.zip, should be renamed STARBAR3.ZIP
#
# 2021-09-28    PV

import os
from common_fs import *

root = r'X:\Archives\Disquettes'

for fileFP in list(get_all_files(root)):
    folder, file = os.path.split(fileFP)
    basename, ext = os.path.splitext(file)
    if len(basename)<=8 and (not any(str.islower(c)  or c==' 'for c in basename)) and any(str.islower(c) for c in ext):
        new_name = os.path.join(folder, basename+str.upper(ext))
        print(fileFP, new_name)
        os.rename(fileFP, new_name)