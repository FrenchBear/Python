# book_variants.py
# Group books per variants
#
# 2022-07-06    PV

from collections import defaultdict, namedtuple
import re
from common_fs import get_all_files
import os

source = r'W:\Livres\Informatique'

Book = namedtuple('Book', 'Title,Edition,Year,Editor,Author')

dicbooks: dict[str, list[Book]] = defaultdict(list)

for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    base, ext = os.path.splitext(file)

    if ext.lower()=='.pdf':
        ts = base.split(' - ')

        title = ts[0]
        year = None
        edition = 1
        if ma := re.search(r"\((\d+)\)", title):
            year = int(ma.group(1))
            title = title[:ma.start(0)].strip()
        elif ma := re.search(r"\((1st|1ère|2nd|3rd|(\d+)(th|è)) ed, (\d\d\d\d|X)\)", title):
            syear = ma.group(4)
            if syear == 'X':
                year = None
            else:
                year = int(syear)
            sed: str = ma.group(1)
            match sed:
                case '1st' | '1ère':    # DO NOT use , to list multiple values in a Python case !!!
                    edition = 1
                case '2nd':
                    edition = 2
                case '3rd':
                    edition = 3
                case _:
                    if sed.endswith('th'):
                        edition = int(sed[:-2])
                    elif sed.endswith('è'):
                        edition = int(sed[:-1])
                    else:
                        breakpoint()
                        pass
            title = title[:ma.start(0)-1]+title[ma.start(0)+len(ma.group(0)):]
        else:
            assert '(' not in title

        match len(ts):
            case 1:
                editor = ''
                author = ''

            case 2:
                if ts[1].startswith('['):
                    editor = ts[1]
                else:
                    author = ts[1]

            case 3:
                if not ts[1].startswith('['):
                    print(filefp)
                    #breakpoint()
                editor = ts[1]
                author = ts[2]

        b = Book(title, edition, year, editor, author)
        
        key = title.casefold()+editor.casefold()
        dicbooks[key].append(b)

nm = 0
for key in sorted(dicbooks.keys(), key=lambda k: len(dicbooks[k]), reverse=False):
    if len(dicbooks[key]) > 1:
        nm += 1
        duped = False
        led = []
        for b in dicbooks[key]:
            if b.Edition in led:
                duped = True
            else:
                led.append(b.Edition)
        if duped:
            print(dicbooks[key][0].Title + ':')
            for b in sorted(dicbooks[key], key = lambda b: b.Edition):
                print('   ', b)
            print()

print('\n', nm,'books with multiple variants\n')

#print(dicbooks['ai powered commerce'])