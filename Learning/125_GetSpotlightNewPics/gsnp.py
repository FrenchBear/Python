# GetSpotlightNewPics
# Retrieves new Spotlight (microsoft wallpapers) pictures
#
# 2023-03-25    PV

import shutil
from common_fs import *

source = r'C:\Users\Pierr\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
dest = r'C:\Users\Pierr\OneDrive\PicturesODMisc\Papiers peints\Spotlight'
doit = True

dest_files = set(file.lower() for file in get_files(dest) if extension(file.lower())=='.jpg')

copied = 0
for filebase in get_files(source):
    file=filebase.lower()+'.jpg'
    if not file in dest_files:
        print('Add', file)
        copied += 1
        if doit:
            shutil.copyfile(os.path.join(source, filebase), os.path.join(dest, file))

print('Copied:', copied)
