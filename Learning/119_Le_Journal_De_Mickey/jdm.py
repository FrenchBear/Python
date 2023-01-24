# jdm.py
# Find missing issues of Le Journal de Mickey
#
# 2023-01-24    PV

from common_fs import *
import re

source = r'W:\BD\Revues\Le Journal de Mickey'
ED = re.compile(r"Le Journal de Mickey n°(\d+)(-(\d+))? - .*\.pdf")
dicFound = {}

print("Scanning", source)
for file in list(get_files(source)):
    if file.lower().endswith('.pdf'):
        base, ext = os.path.splitext(file)
        ma = ED.fullmatch(file)
        if ma:
            dicFound[ma.group(1)] = True
            if ma.group(3):
                dicFound[ma.group(3)] = True

nm = 0
for i in range(3000, 3683):
    si = str(i)
    if not si in dicFound:
        print(si)
        nm += 1

print('Missing:', nm)
