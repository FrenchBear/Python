# convert2.py
# prepare conversion of .Net 4.8 projects to .Net core
# 2021-07-21    PV

from common_fs import get_folders
import os
import os.path

def convert_folder(solution_folder: str):
    lf = [folder for folder in get_folders(solution_folder) if folder.lower()=='properties']
    if len(lf)==1:
        file = os.path.join(solution_folder, lf[0], 'AssemblyInfo.cs')
        if os.path.exists(file):
            newpath = os.path.join(solution_folder, 'AssemblyInfo.cs')
            os.rename(file, newpath)

root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5'
for folder in get_folders(root):
    if folder!='.vs':
        convert_folder(os.path.join(root, folder))
