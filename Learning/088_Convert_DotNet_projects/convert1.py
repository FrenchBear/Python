# convert1.py
# prepare conversion of .Net 4.8 projects to .Net core
# 2021-07-20    PV
# 2021-09-16    PV      Write an OEM850 batch file; use upgrade-assistant

from io import TextIOWrapper
from typing import TextIO
from common_fs import *
import os.path

def convert_folder(folder: str, script: TextIO|TextIOWrapper):
    lf = [file for file in get_files(folder) if file.lower().endswith('.vbproj') or file.lower().endswith('.csproj')]
    if len(lf)==0:
        print(f'No .vbproj found in folder {folder}')
    elif len(lf)>1:
        print(f'More than 1 .vbproj found in folder {folder}')
    else:
        script.write(f'cd /D "{folder}"\n')
        #script.write(f'try-convert -p "{lf[0]}"\n')
        script.write(f'upgrade-assistant upgrade --non-interactive "{lf[0]}"\n')

root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5'
root = r'C:\Development\VSTS\WPF Projects Perso\Learning Projects Net5\WPF68 DataGrid Practical Examples'
root = r'C:\Development\GitHub\Visual-Studio-Projects\Net6'

with open(r'c:\temp\conv2.bat', mode='w', encoding='cp850') as script:
    for folderFP in get_all_folders(root):
        _, folder = os.path.split(folderFP)
        if folder!='.vs' and folder!='packages' and not folder.endswith('.backup'):
            convert_folder(folderFP, script)
