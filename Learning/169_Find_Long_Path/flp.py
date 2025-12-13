import os

#!/usr/bin/env python3
"""
Find all subfolders under a root that contain exactly N files.
"""

def find_dirs_with_exact_file_count(root: str, target_count: int):
    for dirpath, dirnames, filenames in os.walk(root):
        if len(filenames) == target_count:
            print(dirpath)

find_dirs_with_exact_file_count(r"D:\Kaforas\HomeSharedKB", 58)
