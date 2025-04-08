# Search_Missing_Elektor.py
# Vérifie que la numérotation des Elektor est continue
#
# 2022-06-21    PV

import re
from common_fs import get_files

source = r'W:\Revues\Électronique\Elektor'

# Elektor n°37-38 - 1981-07..08
NAME = re.compile(r"Elektor n°(\d+)(-(\d+))? - (.*)\.pdf", re.IGNORECASE)

ns = 0
nums = set()
for file in get_files(source):
    ma = NAME.fullmatch(file)
    if ma:
        n1 = int(ma.group(1))
        nums.add(n1)
        if ma.group(3):
            n2 = int(ma.group(3))
            nums.add(n2)
        ns += 1
#print(nums)

print(ns, 'matches')
nmi = min(nums)
nma = max(nums)
print('N°s found from', nmi, 'to', nma)
print('Missing: ', end='')
for i in range(nmi,nma+1):
    if i not in nums:
        print(i, end=' ')
print()
