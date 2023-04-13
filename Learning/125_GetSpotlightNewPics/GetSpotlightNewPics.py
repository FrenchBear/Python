# GetSpotlightNewPics
# Retrieves new Spotlight (microsoft wallpapers) pictures
#
# 2023-03-25    PV
# 2023-04-12    PV      Logfile

import datetime
import shutil
from common_fs import *

source = r'C:\Users\Pierr\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets'
dest = r'C:\Users\Pierr\OneDrive\PicturesODMisc\Papiers peints\Spotlight'
logfile = r'C:\temp\GetSpotlightNewPics-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S.log')
doit = True

dest_files = set(file.lower() for file in get_files(dest) if extension(file.lower()) == '.jpg')

print("GetSpotlightNewPics started")
with open(logfile, 'w') as log:
    copied = 0
    for filebase in get_files(source):
        file = filebase.lower()+'.jpg'
        if not file in dest_files:
            print('Add', file)
            log.write(f'Add {file}\n')
            copied += 1
            if doit:
                shutil.copyfile(os.path.join(source, filebase), os.path.join(dest, file))

    print('Copied:', copied)
    log.write(f'Copied: {copied}\n')
