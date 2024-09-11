# find_dates.py
# Find pics names containing a date
#
# 2024-09-08    PV

import os
import re
from common_fs import extension_part, file_part

# source = r'C:\Users\Pierr\OneDrive\PicturesODPerso'
source = r'C:\PicturesPersoHR'
doit = True

fulldate_re = re.compile(r"\d{4}-\d\d-\d\d (- )? ?")

for rootSource, subsSource, filesSource in os.walk(source):
    rootSourcePrinted = False
    for fileSource in filesSource:
        # if fileSource == 'Thumbs.db' or fileSource == 'desktop.ini':
        #     filefpSource = os.path.join(rootSource, fileSource)
        #     print(filefpSource)
        #     if doit:
        #         os.remove(filefpSource)
        ma = fulldate_re.match(fileSource)
        if ma:
            if not rootSourcePrinted:
                print("")
                print(rootSource)
                rootSourcePrinted = True
            print("  " + fileSource)
