# Copy recent bd
# 2023-11-26    PV

from common_fs import get_all_files, folder_part, file_part
import shutil
import os
import os.path
import datetime

source = r'W:\BD'

tmin = datetime.datetime(2023,11,4)
for filefp in get_all_files(source):
    if datetime.datetime.fromtimestamp(os.path.getmtime(filefp))>tmin:
        print(filefp)
        newpath = os.path.join(r'C:\Downloads\A_Trier\!A_Trier_BD', folder_part(filefp)[6:])
        os.makedirs(newpath, exist_ok=True)
        shutil.copyfile(filefp, os.path.join(newpath, file_part(filefp)))