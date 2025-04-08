# CheckMissingSummaries.py
# Find movies without summary and summaries without movies
#
# 2023-12-07    PV

import os
from common_fs import get_all_files

source = r'V:\Films'
movies = set()
summaries = set()

print('Analyzing files')

for fullpath in get_all_files(source):
    path, file = os.path.split(fullpath.casefold())
    stem, ext = os.path.splitext(file)
    if ext in ['.mkv', '.avi', '.mp4']:
        stem = stem.split(' - ')[0]
        stem = stem.split(' (')[0]
        movies.add(os.path.join(path, stem))
    elif ext=='.txt':
        summaries.add(os.path.join(path, stem))

print(f'{len(movies)} movies, {len(summaries)} summaries')

header = False
for m in movies:
    if m not in summaries:
        if not header:
            print('\nMovies without summary')
            header = True
        print(m)

header = False
for s in summaries:
    if s not in movies:
        if not header:
            print('\nSummaries without movie')
            header = True
        print(s)
