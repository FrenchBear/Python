# rename MicrosoftOffice  CloudFonts from {id}.ttf using info in ListAll.json
# Office Cloud Fonts
# json is convenient in Python since we can dynamically explore loaded structure and discover embedded dicts/list
#
# ListAll.json  C:\Users\Pierr\AppData\Local\Microsoft\FontCache\4\Catalog\ListAll.Json
# CloudFonts\   C:\Users\Pierr\AppData\Local\Microsoft\FontCache\4\CloudFonts

# 2021-09-05    PV
# 2024-07-28    PV      Refresher

import json
import os

# source = r'C:\\temp\\ListAll.json'
# source = r'C:\Users\Pierr\AppData\Local\Microsoft\FontCache\4\Catalog\ListAll.Json'

with open('C:\\temp\\ListAll.json', encoding='utf8') as f:
    data = json.load(f)
ff = data['Fonts']

df: dict
for df in ff:
    family = df['f']
    print(family)
    for sf in df['sf']:
        dn = sf['dn']
        id = sf['id']
        print('  '+dn)
        ext = '.'+sf['t']
        p = os.path.join('C:\\temp\\CloudFonts', family, id+ext)
        if os.path.exists(p):
            newp = os.path.join('C:\\temp\\CloudFonts', family, dn+ext)
            os.rename(p, newp)
