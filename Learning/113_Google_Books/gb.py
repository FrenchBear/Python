# gb.py
# Learning Python - Google Books API calls
#
# 2022-07-01    PV

import json
import shutil
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


def GetBookInfo(title: str, qpublisher: str) -> Optional[list[Book]]:
    match qpublisher.lower():
        case "packt":
            publisher = 'Packt Publishing Ltd'
        case "manning":
            publisher = 'Simon and Schuster'
        case "o'reilly":
            publisher = '"O\'Reilly Media, Inc."'
        case _:
            publisher = qpublisher

    data = GetJsonBookInfo(title, publisher, qpublisher)
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

    for bookinfo in data['items']:
        try:
            dtitle: str = bookinfo['volumeInfo']['title']
            dpublisher: str = bookinfo['volumeInfo']['publisher']
            if dtitle.casefold() == title.casefold() and dpublisher.casefold() == publisher.casefold():
                dauthors: str = ', '.join(bookinfo['volumeInfo']['authors']).replace('"', "'")
                dpublishedDate: str = bookinfo['volumeInfo']['publishedDate']
                year: int = int(dpublishedDate[:4])
                assert 1950 <= year <= 2023
                if not any([True for b in answer if b.title.casefold() == dtitle.casefold() and b.publisher.casefold() == qpublisher.casefold() and b.authors.casefold() == dauthors.casefold() and b.year == year]):
                    b = Book(title, qpublisher, dauthors, year)
                    answer.append(b)
        except:
            pass
    return answer


source = r'W:\Livres\A_Trier\Packt'
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
for file in get_files(source):
    nf += 1
    base, ext = os.path.splitext(file)
    segments = base.split(' - ')
    if len(segments) == 3 and segments[2] == "X":
        print(file, ' -> ', end='')
        title = segments[0]
        bp = ''
        try:
            pp = title.index('(')
            bp = title[pp:]
            title = title[:pp].strip()
        except:
            pass

        publisher = segments[1][1:-1]
        lb = GetBookInfo(title, publisher)
        if lb == None:
            # Error message has already been printed
            breakpoint()
            continue

        if len(lb) == 1:
            b = lb[0]
            nr += 1
            segments[0] = title + f" ({b.year})"
            segments[2] = b.authors
            newfile = ' - '.join(segments)+ext
            print(newfile)
            if doit:
                shutil.move(os.path.join(source, file), os.path.join(clean, newfile))
        elif len(lb) == 0:
            print('Not found')
            if doit:
                shutil.move(os.path.join(source, file), os.path.join(zero, file))
        else:
            print(len(lb), 'answers\n\nDefault:do not rename, move to Trop subfolder')
            newfiles: list[str] = []
            for b in lb:
                segments[0] = title + f" ({b.year})"
                segments[2] = b.authors
                newfile = ' - '.join(segments)+ext
                newfiles.append(newfile)
                print(f"  {len(newfiles)}: {newfile}")
            ch = int(input("Choice: "))
            if doit:
                if 1 <= ch <= len(newfiles):
                    print(f'Renamed "{newfiles[ch-1]}" and moved to Clean subfolder')
                    shutil.move(os.path.join(source, file), os.path.join(clean, newfiles[ch-1]))
                else:
                    print("Moved to Trop subfolder")
                    shutil.move(os.path.join(source, file), os.path.join(trop, file))

print()
print(nf, 'files, ', nr, 'renamed')
