# syncrename.py
# Rename BD files in arenommer folder taking titles from reference folder
#
# 2023-12-24    PV
# 2024-01-06    PV      Non-numeric BD number are converted and tested using lowercase form

import os
from common_fs import get_files, basename_part, extension_part, folder_exists

doit = True
useReferenceSeries = True

reference = r"W:\BD\Ancien\Horace"
arenommer = r"C:\Users\Pierr\Downloads\A_Trier\!A_Trier_BD\Horace"

def sync_rename(reference: str, arenommer: str) -> None:
    refTitles: dict[str, str] = {}
    refSeries: dict[str, str] = {}

    for file in list(get_files(reference)):
        if file=='Thumbs.db':
            continue
        bn = basename_part(file)
        ts = bn.split(' - ')
        if len(ts) >= 3:
            refTitles[ts[1].lower()] = ' - '.join(ts[2:])
            refSeries[ts[1].lower()] = ts[0]

    if not folder_exists(reference):
        print('dossier reference inexistant ou inaccessible')
        os._exit(1)

    if not folder_exists(arenommer):
        print('dossier arenommer inexistant ou inaccessible')
        os._exit(1)

    for file in list(get_files(arenommer)):
        if file=='Thumbs.db':
            continue
        bn = basename_part(file)
        ext = extension_part(file)
        ts = bn.split(' - ')
        if len(ts) >= 2:
            n = ts[1].lower()
            if n in refTitles:
                nn = (refSeries[n] if useReferenceSeries else ts[0]) + ' - ' + n + ' - ' + refTitles[n]
                print(repr(file) + ' -> ' + repr(nn + ext))
                if doit:
                    os.rename(os.path.join(arenommer, file), os.path.join(arenommer, nn + ext))
            else:
                print("file " + repr(file) + ': n° non trouvé dans le dossier de référence, ignoré')
        else:
            print("file " + repr(file) + ': moins de 2 segments, ignoré')

if __name__=='__main__':
    sync_rename(reference, arenommer)
