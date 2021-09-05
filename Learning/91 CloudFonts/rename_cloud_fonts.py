# rename MicrosoftOffice  CloudFonts from {id}.ttf using info in ListAll.json
# json is convenient in Python since we can dynamically explore loaded structure and discover embedded dicts/list
# 2021-09-05    PV

import json
import os

with open('C:\\temp\\ListAll.json', encoding='utf8') as f:
    data = json.load(f)
ff = data['Fonts']

df: dict
for df in ff:
    family = df['f']
    print(family)
    for sf in df['sf']:
        gn = sf['gn']
        id = sf['id']
        print('  '+gn)
        p = os.path.join('C:\\temp\\CloudFonts', family, id+'.ttf')
        if os.path.exists(p):
            newp = os.path.join('C:\\temp\\CloudFonts', family, gn+'.ttf')
            os.rename(p, newp)
