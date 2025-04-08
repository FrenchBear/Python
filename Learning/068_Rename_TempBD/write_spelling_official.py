
import os
import json
from collections import defaultdict, Counter
from typing import DefaultDict, Counter as CounterType

from common import normalize_serie

sources = [r'W:\BD\Classique', r'W:\BD\Adulte', r'W:\BD\Ancien', r'W:\BD\Extra', r'W:\BD\Comics', r'W:\TempBD\final']
output = r'spellings_officiel_temp.json'

series: DefaultDict[str, CounterType] = defaultdict(Counter)

for source in sources:
    print(source)
    root, folders, files = next(os.walk(source))

    for folder in folders:
        if folder.endswith(" ꜰ"):
            folder = folder[:-2]
        folder = folder.split(" - ")[0]
        serie = normalize_serie(folder)
        series[serie].update({folder:1})

    for file in files:
        stem, ext = os.path.splitext(file)
        segments = stem.split(' - ')
        serie = normalize_serie(segments[0])
        series[serie].update({segments[0]:1})

final = sorted([x.most_common(1)[0][0] for x in series.values()])
with open(output, 'w', encoding='utf8') as outfile:
    json.dump(final, outfile, indent=4, ensure_ascii=False)

print(f'{len(final)} générées dans {output}')
