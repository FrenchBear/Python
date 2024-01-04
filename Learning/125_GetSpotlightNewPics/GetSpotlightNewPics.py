# GetSpotlightNewPics
# Retrieves new Spotlight (microsoft wallpapers) pictures
#
# 2023-03-25    PV
# 2023-04-12    PV      Logfile
# 2023-07-19    PV      Added missing 
# 2023-12-31    PV      Also look for Kaforas spotlight pictures

import datetime
import shutil
import os
from common_fs import get_files, extension_part

source1 = r'C:\Users\Pierr\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
source2 = r'C:\Users\Kafor\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
dest = r'C:\Users\Pierr\OneDrive\PicturesODMisc\Papiers peints\Spotlight'
logfile = r'C:\temp\GetSpotlightNewPics-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.log')
doit = True

dest_files = set(file.lower() for file in get_files(dest) if extension_part(file.lower()) == '.jpg')

print("GetSpotlightNewPics started")
with open(logfile, 'w') as log:
    copied = 0
    for source in [source1, source2]:
        for filebase in get_files(source):
            file = filebase.lower()+'.jpg'
            if file not in dest_files:
                print('Add', file)
                log.write(f'Add {file}\n')
                copied += 1
                if doit:
                    shutil.copyfile(os.path.join(source, filebase), os.path.join(dest, file))

    print('Copied:', copied)
    log.write(f'Copied: {copied}\n')
