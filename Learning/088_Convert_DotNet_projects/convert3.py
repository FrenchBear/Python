# convert3.py
# prepare conversion of .Net 4.8 projects to .Net core
# 2021-07-21    PV

from common_fs import *
import os.path
import shutil

def convert_folder(solution_folder: str):
    source = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5\WPF05 Grid Binding\AssemblyInfo.cs'
    dest = os.path.join(solution_folder, 'AssemblyInfo.cs')
    if os.path.exists(dest):
        shutil.copy(source, dest)
        print('Ok:', solution_folder)

root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5'
for folder in get_folders(root):
    if folder!='.vs' and folder!='WPF05 Grid Binding':
        convert_folder(os.path.join(root, folder))
