
import os
import json
from collections import defaultdict, Counter
from typing import DefaultDict, Counter as CounterType

from common import *


source = r'W:\TempBD\final'
output = r'spellings_officiel_Temp.json'

for root, folders, files in os.walk(source):
    break

series: DefaultDict[str, CounterType] = defaultdict(Counter)
for folder in folders:
    serie = normalize_serie(folder)
    series[serie].update({folder:1})

for file in files:
    basename, ext = os.path.splitext(file)
    segments = basename.split(' - ')
    serie = normalize_serie(segments[0])
    series[serie].update({segments[0]:1})

final = sorted([x.most_common(1)[0][0] for x in series.values()])
with open(output, 'w', encoding='utf8') as outfile:
    json.dump(final, outfile, indent=4, ensure_ascii=False)

print(f'{len(final)} générées dans {output}')
