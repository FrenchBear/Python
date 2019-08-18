# Copy missing files after GoldWave normalization
# Goldwave does not copy .jpg or .txt files, this programs copy missing files
#
# 2019-08-12    PV      First version

import os
import shutil

def CopyMissingFiles(source, target):
    # Get files and folders in source
    source_files=[]
    source_folders=[]
    for item in os.listdir(source):
        if os.path.isfile(os.path.join(source, item)):
            source_files.append(item)
        elif os.path.isdir(os.path.join(source, item)):
            source_folders.append(item)

    target_files=[]
    target_folders=[]
    for item in os.listdir(target):
        if os.path.isfile(os.path.join(target, item)):
            target_files.append(item)
        elif os.path.isdir(os.path.join(target, item)):
            target_folders.append(item)

    # print missing files
    print_folder = False
    for item in [x for x in source_files if x not in target_files and x!='thumbs.db']:
        if not print_folder:
            print_folder=True
            print(source, ":")
        print("  ", item)
        shutil.copy2(os.path.join(source, item), target)

    # recurse for subfolders
    for subf in source_folders:
        if not subf in target_folders:
            print("**** Missing target folder ", os.path.join(target, subf))
            os.mkdir(os.path.join(target, subf))
        CopyMissingFiles(os.path.join(source, subf), os.path.join(target, subf))



source = r'U:\Pierre\A_Trier\A_Trier Brut\Georges Delerue\128'
target = r'C:\Temp\LP128'

CopyMissingFiles(source, target)