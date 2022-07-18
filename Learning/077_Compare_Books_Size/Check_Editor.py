# Check_Editor.py
# JDimple ecitor check for books
# For a more cmplete code, see project 047_Check_Books_Editors
#
# 2022-07-14    PV

import shutil
from collections import Counter
from os import path
from common_fs import *

source = r'D:\A_Trier_Raw'
dest = r'D:\Sorted'

keywords = ['python',
            'c',
            'c#',
            'c++',
            'java',
            'web',
            'javascript',
            'game',
            'games',
            'machine',
            'microsoft',
            'vision',
            'excel',
            'algorithms',
            'sql',
            'azure',
            '.net',
            'html5',
            'php',
            'android',
            'patterns',
            'windows',
            'cloud',
            '3d',
            'react',
            'core',
            'mathematics',
            'asp.net',
            'css',
            'mysql',
            'unity',
            'security',
            'spring',
            'matlab',
            'arduino',
            'raspberry',
            'pi',
            'ajax',
            'bi',
            'ai',
            'rust',
            'jquery',
            'opengl',
            'kubernetes',
            'vue.js',
            'kotlin',
            'gui',
            'tensorflow',
            'linux',
            'google',
            'algebra',
            'node.js',
            'angular',
            'sharepoint',
            'devops',
            'docker',
            'typescript',
            'statistics',
            'cryptography',
            'database',
            'physics',
            'css3',
            'javafx',
            'basic',
            'exam',
            'vba',
            'powershell',
            'directx',
            'scripting',
            'xml',
            'adobe',
            'aws',
            'amazon',
            'wpf',
            'django',
            'blender',
            'finance',
            'ruby',
            'html',
            'mathematica',
            'linq', ]

d = Counter()
nb = 0
nbk = 0
for filefp in list(get_all_files(source)):
    if filefp.lower().endswith('.pdf'):
        folder, file = os.path.split(filefp)
        basename, ext = os.path.splitext(file)
        ts = basename.split(' - ')
        nb += 1
        # if len(ts) == 3:
        #     ed = ts[1]
        #     aut = ts[2]
        # elif len(ts) == 2 and not ts[1].startswith('['):
        #     aut = ts[1]
        #     ed = ''
        # else:
        #     aut = ''
        #     ed = ts[1]

        # if (' a ') in aut or ' and ' in aut:
        #     print(filefp)

        try:
            p = ts[0].index(' (')
            tit = ts[0][:p]
        except:
            tit = ts[0]

        tit = tit.replace(',', ' ').replace('-', ' ').replace('⧸', ' ').casefold()
        lk = []
        for w in tit.split(' '):
            if w=='ed,': breakpoint()
            if (len(w) >= 2 or w == 'C'):
                d.update([w])
                if w in keywords and not w in lk:
                    lk.append(w)
        if lk:
            lk.sort()
            print(lk, tit)
            nbk += 1
            folder = path.join(dest, ' '.join(lk))
            if not folder_exists(folder):
                os.mkdir(folder)
            shutil.move(filefp, folder)
            pass
        else:
            pass
            #print(tit)


l = list(d.most_common())
with open("wordsfreq.txt", "w", encoding='utf-8') as out:
    for w, f in l:
        if not w in keywords:
            out.write(f"{f}\t{w}\n")

print(len(l), 'words')
print(nb, 'books, ', nbk,'with keywords')
