# file_spell_check_En.py
# File names correction in English
#
# 2021-12-16    PV
# 2022-01-03    PV      Fusionne les mots de mots_fr.txt avec ceux de mots_fr2.txt (typiquement les nom propres); Mots en anglais
# 2022-06-04    PV      Nettoyage et correction d'erreurs pour renommer des ebooks
# 2022-07-01    PV      Version en anglais, réécriture quasi complète

from common_fs import get_all_files
from casefix_En import dic_casefix, process_exceptions_En
import os

source = r'C:\Temp\A_Trier'
doit = True

# Note that word processing should be contextual, some expressions such as 'Best Of', 'A to Z' , 'A Major', ... keep an uppercase
# But for book titles, this shouldn't be critical
def process_word(w: str, first: bool):
    # APA Style (https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case) + from with
    if (not first) and w.lower() in ['and', 'as', 'but', 'for', 'if', 'nor', 'or', 'so', 'yet', 'a', 'an', 'the', 'as', 'at', 'by', 'for', 'in', 'of', 'off', 'on', 'per', 'to', 'up', 'via', 'from', 'with']:
        return w.lower()
    if w.casefold() in dic_casefix:
        return dic_casefix[w.casefold()]
    return w[0].upper()+w[1:]


def process_segment(s):
    w = ''
    res = ''
    firstword = True
    for c in s:
        if c in [' ', '+', '.', ',', '-']:     # Simple quote is not considered a separator, maybe should only if not sandwich between letters
            # typically {'+', '#', '.', ',', ' ', '-'}
            if w != '':
                res += process_word(w, firstword)
                w = ''
                firstword = c != ' '
            res += c
        else:
            w += c
    if w != '':
        res += process_word(w, firstword)
    # Exceptions
    res = process_exceptions_En(res)
    return res


def process_name(name: str) -> str:
    ts = name.split(' - ')
    s1 = ts[0]

    bp = ''
    try:
        pp = s1.index('(')
        bp = s1[pp:]
        s1 = s1[:pp]
    except:
        pass

    ts[0] = process_segment(s1)+bp
    return ' - '.join(ts).replace('cplusplus', 'C++').replace('Cplusplus', 'C++').replace('csharp', 'C#').replace('Csharp', 'C#').replace("[Oreilly]", "[O'Reilly]")

# s = 'A beginner's the best, the follow-up And Up (2nd ed, 2003)'
# print(process_name(s))


with open(r'c:\temp\f1.txt', 'w', encoding='utf-8') as out1:
    with open(r'c:\temp\f2.txt', 'w', encoding='utf-8') as out2:
        nt = 0
        nd = 0
        for filefp in get_all_files(source):
            folder, file = os.path.split(filefp)
            bname, ext = os.path.splitext(file)
            nt += 1

            newname = process_name(bname)
            if bname != newname:
                nd += 1
                print(f'{bname}{ext} -> {newname}{ext}')
                out1.write(bname+'\n')
                out2.write(newname+'\n')
                if doit:
                    f1 = os.path.join(folder, bname+ext)
                    f2 = os.path.join(folder, newname+ext)
                    os.rename(f1, f2)

print()
print(nt, 'file(s) processed, ', nd, 'file(s) renamed')
