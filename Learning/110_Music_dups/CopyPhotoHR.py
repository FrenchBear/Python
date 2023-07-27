# CopyPhotoHR
# Retrieve HR version of some photos
# 2022-06-05    PV

import os
import shutil
from common_fs import get_all_files, file_part, file_exists

root = r'C:\Users\Pierr\OneDrive\PicturesODPerso\2022\2022'
root_hr = r'\\teraz\photo\Pierre\PicturesSkull\2022\2022-05 Pyrénées PV HR'
l = list(get_all_files(root))
for file_fp in l:
    file = file_part(file_fp)
    file_hr_fp = os.path.join(root_hr, file)
    if file_exists(file_hr_fp):
        print("Copy HR ", file)
        shutil.copyfile(file_hr_fp, file_fp)

print('Done.')
