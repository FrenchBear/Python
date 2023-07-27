# Add_VSCode_Files.py
# Add missing launch.json and tasks.json files in Python learning projects
#
# https://stackoverflow.com/questions/123198/how-to-copy-files
#
# 2022-03-03    PV

from common_fs import get_folders
import os
import shutil

root = r'C:\Development\GitHub\Python\Learning'
launch_ref = r'C:\Development\GitHub\Python\Learning\002_Now_10_times\.vscode\launch.json'
tasks_ref = r'C:\Development\GitHub\Python\Learning\002_Now_10_times\.vscode\tasks.json'

for folder in get_folders(root):
    vscode_folder = os.path.join(root, folder, '.vscode')
    launch_prj = os.path.join(vscode_folder, 'launch.json')
    tasks_prj = os.path.join(vscode_folder, 'tasks.json')
    if not os.path.isfile(launch_prj):
        print(launch_prj)
        shutil.copy2(launch_ref, launch_prj)
    if not os.path.isfile(tasks_prj):
        print(tasks_prj)
        shutil.copy2(tasks_ref, tasks_prj)
