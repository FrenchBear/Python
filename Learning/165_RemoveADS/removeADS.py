# removeADS.py
# Remove alternate data streams for files stored on Synology volume since deleting an ADS does nothingcd ..
#
# 2025-10-27    PV      First version

# shutil.copy(filename, r"\\terazalt\temp\out\f1.ttf")
# shutil.copyfile(filename, r"\\terazalt\temp\out\f2.ttf")
# shutil.copy2(filename, r"\\terazalt\temp\out\f3.ttf")

import os
import shutil
from common_fs import file_exists

def clean_ads(filename):
    print(filename)
    tempname = filename + "%#"
    try:
        os.rename(filename, tempname)
        shutil.copyfile(tempname, filename)
        shutil.copystat(tempname, filename)  # Copy metadata, including creation time on Windows
        os.remove(tempname)
    except Exception as e:
        print(f"  ERROR processing {filename}: {e}")
        breakpoint()
        pass


# Lancer la fonction principale
if __name__ == "__main__":
    with open(r"C:\Temp\liste.txt", "r", encoding="utf-8") as f:
        for ix, line in enumerate(f):
            print(ix + 1, end=' ')
            l = line.strip()
            if l and file_exists(l):
                clean_ads(l)
    print("Done.")
