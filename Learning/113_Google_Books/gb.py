# gb.py
# Learning Python - Google Books API calls
#
# 2022-07-01    PV
# 2023-02-10    PV      Code cleanup

import json
import os
import re
import shutil
import time
import urllib
import urllib.parse
from typing import Any, Optional

import requests
from common_fs import file_exists, folder_exists, get_files
from termcolor import colored

source = r"C:\Temp\A_Trier\Mercury"
doit = True
movetotrop = False

with open(r'C:\Utils\Local\googlebooks.txt', encoding='utf_8') as f:
    KEY = f.read()

BASE_URL = "https://www.googleapis.com/books/v1/volumes?q=+intitle:{title}+inpublisher:{publisher}&key={KEY}"


def GetJsonBookInfo(title: str, publisher: str, qpublisher: str) -> Any:
    cache = ("JsonCache/" + title + " - [" + qpublisher + "].json").replace('"', '_')

    if file_exists(cache):
        with open(cache, encoding="utf-8") as f:
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
        return f"Book({repr(self.title)}, {repr(self.publisher)}, {repr(self.authors)}, {repr(self.year)})"


def clean_title(t: str) -> str:
    return t.replace('-', ' ').replace(':', ' ').replace('.', ' ').replace(',', ' ').replace('\u2013', ' ').replace('  ', ' ').replace('  ', ' ').strip().casefold()


def GetBookInfo(title: str, qpublisher: str) -> list[Book] | None:
    match qpublisher.lower():
        case "packt":
            publishers = ['Packt Publishing Ltd', 'Packt Publishing']
        case "manning":
            publishers = ['Simon and Schuster']
        case "o'reilly":
            publishers = ['"O\'Reilly Media, Inc."', "O'Reilly Media"]
        case "addison-wesley":
            publishers = ['Addison-Wesley', 'Addison-Wesley Microsoft Techn', 'Addison-Wesley Longman', 'Addison-Wesley Professional',
                          'Pearson Education', 'Sams Publishing', 'Prentice Hall']
        case "crc":
            publishers = ['CRC', 'CRC Press']
        case "mercury":
            publishers = ['Mercury', 'Mercury Learning and Information', 'Stylus Publishing, LLC', 'Pocket Primer']
        case "pragmatic":
            publishers = ['Pragmatic', 'Pragmatic Bookshelf']
        case "springer":
            publishers = ['Springer', 'Springer Nature', 'Springer Science & Business Media']
        case "pearson":
            publishers = ['Pearson', 'Pearson Education India', 'Macromedia Press', 'Prentice Hall']
        case "starch":
            publishers = ['Starch', 'No Starch Press']
        case "wiley":
            publishers = ['Wiley', 'John Wiley & Sons']
        case "mcgraw-hill":
            publishers = ['McGraw-Hill', 'McGraw-Hill Education', 'McGraw Hill Professional']
        case "cengage":
            publishers = ['Cengage', 'Cengage Learning', 'South Western Educational Publishing', 'Cengage Learning Ptr', 'Course Technology']
        case "cambridge":
            publishers = ['Cambridge', 'Cambridge University Press']
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
            dsubtitle: str
            try:
                dsubtitle = clean_title(bookinfo['volumeInfo']['subtitle'])
            except:
                dsubtitle = ''
            dpublisher: str
            try:
                dpublisher = bookinfo['volumeInfo']['publisher']
            except:
                dpublisher = ''
            if (dtitle == title or dtitle+' '+dsubtitle == title) and (dpublisher in publishers or dpublisher == ''):
                if dtitle+' '+dsubtitle == title:
                    title += ' '+dsubtitle
                dauthors: str = ', '.join(bookinfo['volumeInfo']['authors']).replace('"', "'")
                dpublishedDate: str = bookinfo['volumeInfo']['publishedDate']
                year: int = int(dpublishedDate[:4])
                assert 1950 <= year <= 2023

                # for b in answer:
                #     print(b.title == dtitle and b.publisher == qpublisher and b.authors.casefold() == dauthors.casefold() and b.year == year)
                #     print(b.title, dtitle, b.title == dtitle)
                #     print(b.publisher, qpublisher, b.publisher == qpublisher)
                #     print(b.authors.casefold(), dauthors.casefold(), b.authors.casefold() == dauthors.casefold())
                #     print(b.year, year, b.year == year)
                #     print()

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
    if n > 1:
        print('Target already exists, renamed '+dst)
    shutil.move(src, dst)


#### Start
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
listfiles.sort(key=str.lower)
print(len(listfiles), ' file(s) to process\n')
for file in listfiles:
    nf += 1
    base, ext = os.path.splitext(file)
    segments = base.split(' - ')
    if len(segments) == 3 and segments[2] == "X":
        print(colored(file, 'yellow'), ' -> ', end='')
        title = segments[0]
        bp = ''
        ed = 0
        #edyear = 0
        try:
            pp = title.index('(')
            bp = title[pp:]
            title = title[:pp].strip()
            if ma := re.match(r"\((\d+)\)", bp):
                ed = 1
                #edyear = int(ma.groups[1])
            elif ma := re.match(r"\((\d+)(1st|nd|rd|th) ed, (\d+|X)\)", bp):
                ed = int(ma.group(1))
            else:
                breakpoint()
                pass
        except:
            pass

        publisher = segments[1][1:-1]
        zlb = GetBookInfo(title, publisher)
        if zlb is None:
            # Error message has already been printed
            breakpoint()
            continue

        lb: list[Book] = zlb    # type: ignore
        newfile = ''
        originaled = newed = 1

        if len(lb) == 0:
            print('No potential matches')
            pass
        if len(lb) == 1:
            b = lb[0]
            nr += 1
            if ed == 0 or ed == 1:
                nbp = f" ({b.year})"
            elif ed == 2:
                nbp = f" (2nd ed, {b.year})"
            elif ed == 3:
                nbp = f" (3rd ed, {b.year})"
            else:
                nbp = f" ({ed}th ed, {b.year})"

            segments[0] = title + nbp
            segments[2] = b.authors
            newfile = ' - '.join(segments)+ext
            print(colored(newfile, 'green'))
            if doit:
                shutil_move(os.path.join(source, file), os.path.join(clean, newfile))
        elif len(lb) == 0:
            print(colored('Not found', 'red'))
            if doit:
                shutil_move(os.path.join(source, file), os.path.join(zero, file))
        else:
            print(len(lb), 'answers\n')
            
            newfiles: list[str] = []
            tch: list[str] = []

            if movetotrop:
                ch = 0
                newfile = ''
            else:
                for b in lb:
                    segments[0] = title + f" ({b.year})"
                    segments[2] = b.authors
                    newfile = ' - '.join(segments)+ext
                    newfiles.append(newfile)
                    print(f"  {len(newfiles)}: {newfile}")

                if ma := re.search(r"\(([^ ]*) ed, (\d\d\d\d|X)\)", file):
                    match ma.group(1):
                        case '1st':
                            originaled = 1
                        case '2nd':
                            originaled = 2
                        case '3rd':
                            originaled = 3
                        case _:
                            ma = re.match(r"(\d+)th", ma.group(1))
                            if not ma:
                                breakpoint()
                            else:
                                originaled = int(ma.group(1))
                else:
                    originaled = 1
                newed = 1
                tch = input("Choice: [choice ed year] ").split()
                ch = int(tch[0])

            if 1 <= ch <= len(newfiles):
                newfile = newfiles[ch-1]
                if len(tch) > 1:
                    newed = int(tch[1])
                    pp = newfile.index('(')
                    pq = newfile.index(')', pp)
                    if ma := re.match(r"\((.* ed, )?(\d\d\d\d)\)", newfile[pp:pq+1]):
                        year = int(ma.group(2))
                    if len(tch) > 2:
                        year = int(tch[2])
                    else:
                        year = 9999
                    if newed == 1:
                        nbp = f"({year})"
                    elif newed == 2:
                        nbp = f"(2nd ed, {year})"
                    elif newed == 3:
                        nbp = f"(3rd ed, {year})"
                    elif newed > 3:
                        nbp = f"({newed}th ed, {year})"
                    else:
                        nbp = ''
                    newfile = newfile[:pp] + nbp + newfile[pq+1:]

            if doit:
                if newfile != '':
                    print(colored(newfile, 'cyan'))
                    if originaled > 1 and newed == 1:
                        print(colored(f'Attention, edition changing from {originaled} to {newed}', 'red'))
                    _ = input('(Enter to rename, Ctrl+c to stop) ')
                if 1 <= ch <= len(newfiles):
                    print(colored('Renamed and moved to Clean subfolder\n', 'green'))
                    shutil_move(os.path.join(source, file), os.path.join(clean, newfile))
                else:
                    print(colored('Moved to Trop subfolder\n', 'green'))
                    shutil_move(os.path.join(source, file), os.path.join(trop, file))

print(nf, 'files, ', nr, 'renamed')
