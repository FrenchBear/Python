# convert1.py
# prepare conversion of .Net 4.8 projects to .Net core
# 2021-07-20    PV

from common_fs import *
import os.path

def convert_folder(folder: str):
    lf = [file for file in get_files(folder) if file.lower().endswith('.vbproj') or file.lower().endswith('.csproj')]
    if len(lf)==0:
        print(f'No .vbproj found in folder {folder}')
    elif len(lf)>1:
        print(f'More than 1 .vbproj found in folder {folder}')
    else:
        print(f'cd /D "{folder}"')
        print(f'try-convert -p "{lf[0]}"')

root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5'
root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5\WPF68 DataGrid Practical Examples'
root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5\WPF71 InkCanvas'
for folder in get_folders(root):
    if folder!='.vs':
        convert_folder(os.path.join(root, folder))
