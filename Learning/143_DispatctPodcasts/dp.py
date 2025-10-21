# dp.py
# Dispatch podcasts in a separate folder per month
#
# 2024-11-04    PV      First version

import os.path
import shutil
from common_fs import get_files

# source = r"C:\Temp\LP\Lisa Delmoitiez"
# dest = r"C:\Temp\Lisa Delmoitiez\Lisa Delmoitiez - France Inter - Lisa Delmoitiez n'aurait pas fait comme ça"
# split_on_month = True

# source = r"C:\Temp\LP\Frédéric Fromet"
# dest = r"C:\Temp\Frédéric Fromet\Frédéric Fromet - France Inter - La chanson de Frédéric Fromet"
# split_on_month = False

# source = r"C:\Temp\LP\Alex Vizorek"
# dest = r"C:\Temp\Alex Vizorek\Alex Vizorek - France Inter - Le billet d'Alex Vizorek"
# split_on_month = False

# source = r"C:\Temp\LP\Daniel Morin"
# dest = r"C:\Temp\Daniel Morin\Daniel Morin - France Inter - Le billet de Daniel Morin"
# split_on_month = True

source = r"C:\Temp\LP\Charline Vanhoenacker"
dest = r"C:\Temp\Charline Vanhoenacker\Charline Vanhoenacker - France Inter - Le billet de Charline"
split_on_month = True

doit = True


files = [filefp for filefp in get_files(source) if filefp.endswith(".mp3")]     # Source is flat

for file in files:
    month = file[5:7]
    year = file[:4]

    if split_on_month:
        targetfolder = os.path.join(dest, year, year + "-" + month)
    else:
        targetfolder = os.path.join(dest, year)

    print(file, ' --> ', targetfolder)
    if doit:
        if not os.path.exists(targetfolder):
            os.makedirs(targetfolder)
        shutil.move(os.path.join(source, file), targetfolder)
