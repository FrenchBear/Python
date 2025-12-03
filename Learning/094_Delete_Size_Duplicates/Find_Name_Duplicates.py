# Find book files with duplicate names
#
# 2023-01-20    PV      First version
# 2025-12-30    PV      Better cleaning of names using unicodedata to remove accents, and sophisticated is_edition_compatible

from common_fs import folder_exists, get_all_files
import re
import unicodedata
import shutil
import os

source1 = r'W:\Livres'         # Reference
source2 = r'C:\Users\Pierr\Downloads\A_Trier\!Large'  # Books to check
trash = r'C:\Users\Pierr\Downloads\A_Trier\Trash'

doit = True

sourcelist = []
bookname = re.compile(r"([^)]*)( \([^)]+\))? - \[([^]]+)\] - (.*)")

if doit:
    if not folder_exists(trash):
        os.mkdir(trash)

def lower_no_accent(to_translate: str) -> str:
    return ''.join(
        c for c in list(unicodedata.normalize('NFD', to_translate.lower())) if unicodedata.category(c) != 'Mn')

def clean(name: str) -> str:
    return lower_no_accent(name.replace(',', ' ').replace(',', ' ').replace('  ', ' ')).strip()


print('Indexing source books from', source1)
for filefp in get_all_files(source1):
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)

    if ext.casefold() == '.pdf':
        ma1 = bookname.fullmatch(bname)
        if ma1:
            ed = ma1.group(2)
            if ed:
                ed = ed.strip()
            b = (clean(ma1.group(1)), ed, clean(ma1.group(3)), clean(ma1.group(4)), folder, file)
            sourcelist.append(b)
            # auth:str = ma.group(4)
            # if ' and ' in auth.lower():
            #     print(filefp)

def val(s):
    """
    Converts a string to an integer, stopping at the first non-numeric character.
    Similar to Visual Basic's Val() function but returns an integer.
    """
    if not isinstance(s, str):
        try:
            s = str(s)
        except:
            return 0

    leading_num_str = ""
    temp_s = s.lstrip()  # Remove leading whitespace

    # Check for optional sign
    if temp_s.startswith(('+', '-')):
        leading_num_str += temp_s[0]
        temp_s = temp_s[1:]

    for char in temp_s:
        if char.isdigit():
            leading_num_str += char
        else:
            break

    if leading_num_str and (leading_num_str not in ['+', '-']):
        return int(leading_num_str)
    else:
        return 0


re_block_par_book = re.compile(r"^((1ère|[12]?\dè|[2-9]?1st|[2-9]?2nd|[2-9]?3rd|\d?[04-9]th|11th|12th|13th) ed, )?(\d{4}|X)$", re.IGNORECASE)

def version_year(ed: str):
    assert (ed.startswith('(') and ed.endswith(')'))
    ed = ed[1:-1].strip()

    ma: re.Match
    ma = re_block_par_book.fullmatch(ed)            # type: ignore

    ver = val(ma.group(1))           # Just the edition number
    year = val(ma.group(3))          # Year X is 0

    return ver, year

def is_edition_compatible(ed1: str | None, ed2: str | None) -> bool:
    if ed1 is None or ed2 is None:
        return True
    if ed1 == ed2:
        return True
    v1, y1 = version_year(ed1)
    v2, y2 = version_year(ed2)
    return v1 == v2 or (y1 == y2 or y1 == 0 or y2 == 0)


print('Checking folder', source2)
l2 = list(get_all_files(source2))
for filefp in l2:
    folder, file = os.path.split(filefp)
    bname, ext = os.path.splitext(file)

    if ext.casefold() == '.pdf':
        ma2: re.Match | None = bookname.fullmatch(bname)
        if ma2:
            title = clean(ma2.group(1))
            ed = ma2.group(2)
            if ed:
                ed = ed.strip()
            editor = clean(ma2.group(3))
            authors = clean(ma2.group(4))

            for b in sourcelist:
                if b[0] == title and is_edition_compatible(ed, b[1]) and b[2] == editor:
                    print(b[5])
                    print(file)
                    print()
                    if doit:
                        try:
                            shutil.move(filefp, os.path.join(trash, file))
                        except:
                            pass
