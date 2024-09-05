# cmp_photos.py
# Compare pics folders
#
# 2024-09-09    PV

from common_fs import get_folders, file_exists, extension_part
import os
import shutil

folder = '2012'
source = os.path.join(r'C:\PicturesODPerso', folder)
dest = os.path.join(r'C:\PicturesPersoHR', folder)

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def compareFoldersList() -> bool:
    sourceFolders = set(get_folders(source))
    destFolders = set(get_folders(dest))

    d1 = sourceFolders - destFolders
    if len(d1) > 0:
        print(f'{RED}Folders on source but not on dest{RESET}')
        print(d1)
        print()

    d2 = destFolders - sourceFolders
    if len(d2) > 0:
        print(f'{RED}Folders on dest but not on source{RESET}')
        print(d2)
        print()

    if len(d1) == 0 and len(d2) == 0:
        print(f"{GREEN}List of folders identical{RESET}")
        return True
    return False

def compareTwoFolders(folderSource: str, folderDest: str):
    for rootSource, subsSource, filesSource in os.walk(folderSource):
        for fileSource in filesSource:
            if fileSource != 'Thumbs.db' and fileSource != 'desktop.ini':
                filefpSource = os.path.join(rootSource, fileSource)
                filefpDest = filefpSource.replace(source, dest)
                if not file_exists(filefpDest):
                    print(f"{RED}*** Source file {filefpSource} not found on dest{RESET}")
                    if "PANO" in filefpSource or "MOTION" in filefpSource or extension_part(filefpSource).lower() in ['.avi', '.mov', '.mpg']:
                        shutil.copyfile(filefpSource, filefpDest)
                        print("  -> copied")

    for rootDest, subsDest, filesDest in os.walk(folderDest):
        for fileDest in filesDest:
            if fileDest != 'Thumbs.db' and fileDest != 'desktop.ini':
                filefpDest = os.path.join(rootDest, fileDest)
                filefpSource = filefpDest.replace(dest, source)
                if not file_exists(filefpSource):
                    print(f"{RED}*** Dest file {filefpDest} not found on source{RESET}")
                    if "PANO" in filefpDest or "MOTION" in filefpDest or extension_part(filefpDest).lower() in ['.avi', '.mov', '.mpg']:
                        shutil.copyfile(filefpDest, filefpSource)
                        print("  -> copied")

def compareFoldersContent():
    folders = get_folders(source)
    for folder in folders:
        #if folder=='2006-08-25 Pics CR':
            print("\n------------------------------------------\n", folder, sep='')
            compareTwoFolders(os.path.join(source, folder), os.path.join(dest, folder))


if compareFoldersList():
    compareFoldersContent()
print()
