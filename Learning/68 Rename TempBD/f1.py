import os
import re

file = r'Krän - 07a - La princesse viagra.pdf'
basename, _ = os.path.splitext(file)

if ma:=re.fullmatch(r".* - ((\d\d)[a-zA0-9]?|Pub|HS|HS \d+|BO)( - .*)?", basename):
    print("match")
    n = int(ma.group(2))
    print(n)
    
