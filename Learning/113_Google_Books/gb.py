# gb.py
# Learning Python - Google Books API calls
#
# 2022-07-01    PV

import json
from typing import Any
import requests
import urllib
import urllib.parse
from common_fs import *

# https://www.googleapis.com/books/v1/volumes?q=+intitle:3D+Game+Design+with+Unreal+Engine+4+and+Blender+inpublisher:Packt&key=AIzaSyB26jpPFxSNh45t-b-rMdLB2teMzlQpFZ8

KEY = "AIzaSyB26jpPFxSNh45t-b-rMdLB2teMzlQpFZ8"
BASE_URL = "https://www.googleapis.com/books/v1/volumes?q=+intitle:{title}+inpublisher:{publisher}&key={KEY}"


def GetJsonBookInfo(title: str, publisher: str, qpublisher:str) -> Any:
    cache = ("JsonCache/" + title + " - [" + qpublisher + "].json").replace('"','_')

    if file_exists(cache):
        with open(cache, "r", encoding="utf-8") as f:
            data = json.load(f)
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


def GetBookInfo(title: str, qpublisher: str) -> list[Book]:
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
    for i in range(data['totalItems']):
        bookinfo = data['items'][i]
        dtitle: str = bookinfo['volumeInfo']['title']
        dpublisher: str = bookinfo['volumeInfo']['publisher']
        if dtitle.casefold() == title.casefold() and dpublisher.casefold() == publisher.casefold():
            dauthors: str = ', '.join(bookinfo['volumeInfo']['authors'])
            dpublishedDate: str = bookinfo['volumeInfo']['publishedDate']
            year: int = int(dpublishedDate[:4])
            assert 1950 <= year <= 2023
            if not any([True for b in answer if b.title == dtitle and b.publisher == dpublisher and b.authors == dauthors and b.year == year]):
                b = Book(title, qpublisher, dauthors, year)
                answer.append(b)
    return answer


def ProcessFile(title: str, publisher: str):
    l = GetBookInfo(title, publisher)
    if len(l) == 0:
        print(f'Not found title="{title}" publisher="{publisher}"')
    elif len(l) > 1:
        print(f'{len(l)} answers for title="{title}" publisher="{publisher}":')
        for b in l:
            print(f'  authors="{b.authors}" year={b.year}')
    else:
        authors = l[0].authors
        year = l[0].year
        print(f'One match for title="{title}" publisher="{publisher}": authors="{authors}" year={year}')


ProcessFile("3D Game Design with Unreal Engine 4 and Blender", "Packt")
ProcessFile("Advanced Algorithms and Data Structures", "Manning")
ProcessFile("A Complete Guide to Docker for Operations and Development", "Apress")
ProcessFile("Practical Simulations for Machine Learning", "O'Reilly")
