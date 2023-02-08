# pc14h
# Récupère les images des caméras à 14h

# 2023-02-08    PV

import re
from common_fs import *

source = r'C:\Users\Pierr\OneDrive\PicturesODMisc\snapshots\tapocam2'

repic = re.compile(r'tapocam[12]-(\d{4})-(\d\d)-(\d\d)_(\d\d)-(\d\d)\.jpg')

for filename in get_files(source):
    ma = repic.fullmatch(filename)
    if ma:
        h = int(ma.group(4))
        m = int(ma.group(5))
        print(filename,h,m)
