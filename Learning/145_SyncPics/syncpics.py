# syncpics.py
# Copy pic (and pdf) files from source to destination
#
# 2025-03-04    PV

import os
import shutil
from common_fs import extension_part, folder_part, folder_exists

doit = True

source = r"U:\Pierre\A_Trier\A_Trier Brut\!192"
destination = r"C:\Temp\MP3192"

def sync_pics() -> None:
    for dirpath, _, filenames in os.walk(source):
        for file in filenames:
            match extension_part(file).lower():
                # Ignore music files and thumbs.db and various text files
                case '.mp3' | '.flac' | '.wav' | '.m4a' | '.db' | '.ini' | '.nfo' | '.txt' | '.torrent':
                    pass

                case '.pdf' | '.jpg' | '.png':
                    sfp = os.path.join(dirpath, file)
                    dfp = os.path.join(dirpath.replace(source, destination), file)
                    print(f'Copy «{sfp}» -> «{dfp}»')
                    if doit:
                        df = folder_part(dfp)
                        if not folder_exists(df):
                            os.makedirs(df)
                        shutil.copy(sfp, dfp)
                    pass

                case _:
                    print(f'*** Unknown extension {file}')

sync_pics()
