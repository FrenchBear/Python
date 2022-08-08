# Deletes/Lists files with duplicate names and page counts
#
# 2022-08-08    PV      First version

from collections import defaultdict
import shutil
import unicodedata
from common_fs import *
import json
import subprocess


source = r'W:\Livres\Informatique'
source_a_trier = r'W:\Livres\A_Trier_Packt'
cache = 'cache_Packt.json'
doit = True

target_match = source_a_trier + '\\match'
target_nomatch = source_a_trier + '\\nomatch'
target_notfound = source_a_trier + '\\notfound'
if not folder_exists(target_match):
    os.mkdir(target_match)
if not folder_exists(target_nomatch):
    os.mkdir(target_nomatch)
if not folder_exists(target_notfound):
    os.mkdir(target_notfound)

dic: defaultdict[str, list[str]] = defaultdict(list)


def lowercase_no_diacritic(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


def canonize_name(s: str) -> str:
    return lowercase_no_diacritic(s).replace("'", '').replace('-', '').replace(' ', '').replace('.', '').replace(',', '').replace('\u29f8', '')


if file_exists(cache):
    with open(cache, encoding='utf-8') as f:
        dic = json.load(f)
else:
    for filefp in get_all_files(source):
        folder, file = os.path.split(filefp)
        bname, ext = os.path.splitext(file)
        if ext.casefold() == '.pdf' and '[Packt]' in bname:
            ts = bname.split(' - ')
            title = ts[0]
            if (p := title.find('(')) >= 0:
                title = title[:p-1].strip()
            k = canonize_name(title)
            # if k in dic:
            #     print('\nDuplicate:\n', filefp+'\n', dic[k])
            dic[k].append(filefp)

    with open(cache, 'w', encoding='utf-8') as outfile:
        json.dump(dic, outfile, indent=4)

print(len(dic), 'entries in dic')


def GetPDFPageCount(file: str) -> int:
    cp = subprocess.run(['CheckPDF', '-b', file], capture_output=True, encoding='cp850')
    out = cp.stdout+cp.stderr
    ts = cp.stdout.split('\t')
    if cp.returncode != 0 or out.startswith('CheckPDF:') or len(ts) != 3 or ts[2] != 'Ok\n':
        print('Error in GetPDFPageCount:', out)
        return 0
    n = int(ts[1])
    return n

# file = 'W:\\Livres\\Informatique\\Langages\\R\\Big Data Analytics with R and Hadoop (2013) - [Packt] - Vignesh Prajapati.pdf'
# print(GetPDFPageCount(file))


nf = 0
nm = 0
for file in list(get_files(source_a_trier)):
    filefp = source_a_trier+'\\'+file
    bname, ext = os.path.splitext(file)
    if ext.casefold() == '.pdf':
        nf += 1
        ts = bname.split(' - ')
        title = ts[0]
        if (p := title.find('(')) >= 0:
            title = title[:p-1].strip()
        k = canonize_name(title)
        print("\n"+file)
        if k in dic:
            nm += 1

            np = GetPDFPageCount(filefp)
            if np == 0:
                print('Error getting page count')
                if doit:
                    shutil.move(filefp, target_nomatch)
            else:
                moved = False
                for fm in dic[k]:
                    npfm = GetPDFPageCount(filefp)
                    if npfm == np:
                        print('Found match for',np,'pages')
                        moved = True
                        if doit:
                            shutil.move(filefp, target_match)
                        break
                if not moved:
                    print('Found NO match for',np,'pages')
                    if doit:
                        shutil.move(filefp, target_nomatch)
        else:
            print('NOT FOUND!')
            if doit:
                shutil.move(filefp, target_notfound)

print('\n', nf, 'files,', nm, 'matches')
