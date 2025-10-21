# sync_media.py
# Golgwave crashed in the middle of conversion, so I neet to keep only the files not already converted

import os
import shutil
from common_fs import get_all_files, stem_part, extension_part, folder_part, file_exists

source = r'C:\Users\Pierr\Downloads\Podcasts'
source2 = r'C:\Users\Pierr\Downloads\Podcasts2'
dest = r'C:\Temp\LP'

nc = 0
for file in get_all_files(source):
    ext = extension_part(file).lower()
    if ext == ".mp3" or ext=='.m4a':
        conv = stem_part(file.replace(source, dest))+".mp3"
        if not file_exists(conv):
            nc += 1
            print("Copy", file)
            file2 = file.replace(source, source2)
            os.makedirs(folder_part(file2), exist_ok=True)
            shutil.copy2(file, file2)

print("copied:", nc)
