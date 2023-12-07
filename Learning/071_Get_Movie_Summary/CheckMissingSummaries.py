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
    basename, ext = os.path.splitext(file)
    if ext in ['.mkv', '.avi', '.mp4']:
        basename = basename.split(' - ')[0]
        basename = basename.split(' (')[0]
        movies.add(os.path.join(path, basename))
    elif ext=='.txt':
        summaries.add(os.path.join(path, basename))

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
