# GetMovieSummary.py
# Simple app using TheMovieDb.org to retrieve movie information
# pip install tmdbsimple
#
# 2020-07-15    PV
# 2023-01-03    PV      Added .mp4 suffix
# 2023-12-17    PV      use common_fs version of get_all_files

import os
import tmdbsimple as tmdb       # type: ignore
from common_fs import get_all_files

source = r'V:\Films\# A_Trier'
#"source = r'V:\Animations\# A_Trier'

tmdb.API_KEY = 'ecdd67089c844d17e9f72a053609ed9f'
search = tmdb.Search()

processed = []
for fullpath in get_all_files(source):
    path, file = os.path.split(fullpath)
    basename, ext = os.path.splitext(file)
    if ext.lower() in ['.mkv', '.avi', '.mp4', '.iso']:
        segments = basename.split(' - ')
        title = segments[0]
        s2 = title.split(' (')
        title = s2[0]
        if not title in processed:
            processed.append(title)
            print(title)
            textfile = os.path.join(path, title+'.txt')
            if not os.path.exists(textfile):
                with open(textfile, mode='w', encoding='utf-8') as out:
                    response = search.movie(query=title)
                    s:dict
                    for s in search.results:
                        out.write(s['title']+'\n')
                        out.write(s.get('release_date','')+'\n')
                        out.write(s['overview']+'\n\n')
                

# #response = search.movie(query='A Few Good Men')
# #response = search.movie(query='The Black Hole')
# response = search.movie(query='La vie de Brian')
# for s in search.results:
#     print(s['title'], s['release_date'], s['overview'])
#     #print(s['title'], s['id'], s['release_date'], s['popularity'])
