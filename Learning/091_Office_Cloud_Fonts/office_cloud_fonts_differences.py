# office_cloud_fonts_differences.py
# Shows delta (directories) between two versions of Office cloud fonts
# See C:\Development\GitHub\Python\Learning\091_Cloud_Fonts for generation
#
# 2023-08-04    PV
# 2024-07-28    PV      Version 2024-08 and pprint
# 2026-02-04    PV      Version 2026-02

from pprint import pprint
from common_fs import get_folders, get_all_files

# r22 = r'C:\Users\Pierr\OneDrive\DocumentsOD\Main Fonts\Office CloudFonts 2022-09'
# r23 = r'C:\Users\Pierr\OneDrive\DocumentsOD\Main Fonts\Office CloudFonts 2023-08'
r24 = r'D:\Pierre\HomeShared\DocumentsPV\Main Fonts\Office CloudFonts 2024-08'
r26 = r'D:\Pierre\HomeShared\DocumentsPV\Main Fonts\Office CloudFonts 2026-02'

# s22 = set(get_folders(r22))
# s23 = set(get_folders(r23))
s24 = set(get_folders(r24))
s26 = set(get_folders(r26))

print('Directories added to 2026-02 that did not exist in 2024-08')
pprint(s26-s24)
print()

print('Directories removed from 2026-02 that existed in 2024-08')
pprint(s24-s26)
print()

# Now with files
f24 = set(f.replace(r24+'\\', '') for f in get_all_files(r24))
f26 = set(f.replace(r26+'\\', '') for f in get_all_files(r26))
print('Files added to 2026-02 that did not exist in 2024-08')
pprint(f26-f24)
print()

print('Files removed from 2026-02 that existed in 2024-08')
pprint(f24-f26)
print()
