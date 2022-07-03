# gb.py
# Learning Python - Google Books API calls
#
# 2022-07-01    PV

import json
import re
import shutil
import time
from typing import Any, Optional
import requests
import urllib
import urllib.parse
from common_fs import *

doit = True

# https://www.googleapis.com/books/v1/volumes?q=+intitle:3D+Game+Design+with+Unreal+Engine+4+and+Blender+inpublisher:Packt&key=AIzaSyB26jpPFxSNh45t-b-rMdLB2teMzlQpFZ8
KEY = "AIzaSyB26jpPFxSNh45t-b-rMdLB2teMzlQpFZ8"
BASE_URL = "https://www.googleapis.com/books/v1/volumes?q=+intitle:{title}+inpublisher:{publisher}&key={KEY}"


def GetJsonBookInfo(title: str, publisher: str, qpublisher: str) -> Any:
    cache = ("JsonCache/" + title + " - [" + qpublisher + "].json").replace('"', '_')

    if file_exists(cache):
        with open(cache, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Service error?
            err = ''
            try:
                err = data['error']['message']
            except:
                pass
            if err == '':
                return data

    title = title.replace("-", " ").replace(",", " ").replace("  ", " ")

    title = urllib.parse.quote_plus(title)
    publisher = urllib.parse.quote_plus(publisher)
    url = BASE_URL.format(title=title, publisher=publisher, KEY=KEY)
    # print(url)

    data = None
    time.sleep(0.2)
    data = requests.get(url).json()
    with open(cache, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)
    return data


class Book:
    def __init__(self, title: str, publisher: str, authors: str, year: int) -> None:
        self.title = title
        self.publisher = publisher
        self.authors = authors
        self.year = year

    def __repr__(self) -> str:
        return f"Book({repr(self.title)}, {repr(self.publisher)},{repr(self.authors)}, {repr(self.year)})"


def clean_title(t: str) -> str:
    return t.replace('-', ' ').replace(':', ' ').replace('.', ' ').replace('\u2013', ' ').replace('  ', ' ').strip().casefold()


def GetBookInfo(title: str, qpublisher: str) -> Optional[list[Book]]:
    match qpublisher.lower():
        case "packt":
            publishers = ['Packt Publishing Ltd', 'Packt Publishing']
        case "manning":
            publishers = ['Simon and Schuster']
        case "o'reilly":
            publishers = ['"O\'Reilly Media, Inc."']
        case _:
            publishers = [qpublisher]

    data = GetJsonBookInfo(title, publishers[0], qpublisher)
    answer: list[Book] = []

    # Service error?
    err = ''
    try:
        err = data['error']['message']
    except:
        pass
    if err != '':
        print("Error: "+err)
        return None

    # Found nothing?
    if data['totalItems'] == 0:
        return answer

    title = clean_title(title)
    for bookinfo in data['items']:
        try:
            dtitle: str = clean_title(bookinfo['volumeInfo']['title'])
            dpublisher: str = bookinfo['volumeInfo']['publisher']
            if dtitle == title and dpublisher in publishers:
                dauthors: str = ', '.join(bookinfo['volumeInfo']['authors']).replace('"', "'")
                dpublishedDate: str = bookinfo['volumeInfo']['publishedDate']
                year: int = int(dpublishedDate[:4])
                assert 1950 <= year <= 2023
                if not any([True for b in answer if b.title == dtitle and b.publisher == qpublisher and b.authors.casefold() == dauthors.casefold() and b.year == year]):
                    b = Book(title, qpublisher, dauthors, year)
                    answer.append(b)
        except:
            pass
    return answer


def shutil_move(src: str, dst: str):
    base, ext = os.path.splitext(dst)
    n = 1
    while file_exists(dst):
        n = n+1
        dst = base + f' FILECOPY{n}' + ext
    if n>1:
        print('Target already exists, renamed '+dst)
    shutil.move(src, dst)


source = r'W:\Livres\A_Trier\Apress'
clean = os.path.join(source, "Clean")
if not folder_exists(clean):
    os.mkdir(clean)
zero = os.path.join(source, "Zero")
if not folder_exists(zero):
    os.mkdir(zero)
trop = os.path.join(source, "Trop")
if not folder_exists(trop):
    os.mkdir(trop)

nf = 0
nr = 0
listfiles = [f for f in get_files(source) if f.casefold().endswith('.pdf')]
listfiles.sort()
print(len(listfiles),' file(s) to process\n')
for file in listfiles:
    nf += 1
    base, ext = os.path.splitext(file)
    segments = base.split(' - ')
    if len(segments) == 3 and segments[2] == "X":
        print(file, ' -> ', end='')
        title = segments[0]
        bp = ''
        ed = 0
        #edyear = 0
        try:
            pp = title.index('(')
            bp = title[pp:]
            title = title[:pp].strip()
            if ma:=re.match("\((\d+)\)", bp):
                ed = 1
                #edyear = int(ma.groups[1])
            elif ma:=re.match("\((\d+)(1st|nd|rd|th) ed, (\d+|X)\)", bp):
                ed = int(ma.group(1))
                #edyear = int(ma.groups[3])
            else:
                breakpoint()
                pass
        except:
            pass

        publisher = segments[1][1:-1]
        zlb = GetBookInfo(title, publisher)
        if zlb == None:
            # Error message has already been printed
            breakpoint()
            continue

        lb: list[Book] = zlb    # type: ignore
        if len(lb) == 1:
            b = lb[0]
            nr += 1
            if ed==0 or ed==1:
                nbp =f" ({b.year})"
            elif ed==2:
                nbp =f" (2nd ed, {b.year})"
            elif ed==3:
                nbp =f" (3rd ed, {b.year})"
            else:
                nbp =f" ({ed}th ed, {b.year})"

            segments[0] = title + nbp
            segments[2] = b.authors
            newfile = ' - '.join(segments)+ext
            print(newfile)
            if doit:
                shutil_move(os.path.join(source, file), os.path.join(clean, newfile))
        elif len(lb) == 0:
            print('Not found')
            if doit:
                shutil_move(os.path.join(source, file), os.path.join(zero, file))
        else:
            print(len(lb), 'answers\n')
            newfiles: list[str] = []
            
            ch = 0
            # for b in lb:
            #     segments[0] = title + f" ({b.year})"
            #     segments[2] = b.authors
            #     newfile = ' - '.join(segments)+ext
            #     newfiles.append(newfile)
            #     print(f"  {len(newfiles)}: {newfile}")

            # tch = input("Choice: ").split()
            # ch = int(tch[0])
            # if 1 <= ch <= len(newfiles):
            #     newfile = newfiles[ch-1]
            #     if len(tch) > 1:
            #         ed = int(tch[1])
            #         pp = newfile.index('(')+1
            #         if ed == 2:
            #             newfile = newfile[:pp] + "2nd ed, " + newfile[pp:]
            #         elif ed == 3:
            #             newfile = newfile[:pp] + "3rd ed, " + newfile[pp:]
            #         elif ed > 3:
            #             newfile = newfile[:pp] + f"{ed}th ed, " + newfile[pp:]

            if doit:
                if 1 <= ch <= len(newfiles):
                    print(f'Renamed "{newfile}" and moved to Clean subfolder\n')
                    shutil_move(os.path.join(source, file), os.path.join(clean, newfile))
                else:
                    print("Moved to Trop subfolder\n")
                    shutil_move(os.path.join(source, file), os.path.join(trop, file))

print()
print(nf, 'files, ', nr, 'renamed')
