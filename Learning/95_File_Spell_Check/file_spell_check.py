# file_spell_check.py
# Tentative de correction automatique de fautes d'accents sur des noms de fichiers en français
#
# 2021-12-16    PV
# 2022-01-03    PV      Fusionne les mots de mots_fr.txt avec ceux de mots_fr2.txt (typiquement les nom propres); Mots en anglais

from collections import defaultdict
from collections import Counter
from os import replace
from typing import DefaultDict, Tuple, Counter
from common_fs import *
import unicodedata

source = r'W:\Livres\A_Trier'
doit = False

# dmf est l'ensemble des mots français accentués, indexé par la version casefold() du mot
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    dmf = dict([(mot.casefold(), mot) for mot in f.read().splitlines()])
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    dmf |= dict([(mot.casefold(), mot) for mot in f.read().splitlines() if ' ' not in mot and mot.casefold() not in dmf])
with open(r'words\extra.fr.txt', 'r', encoding='UTF-8') as f:
    dmf |= dict([(mot.casefold(), mot) for mot in f.read().splitlines() if mot.casefold() not in dmf])

# dme est l'ensemble des mots anglais
with open(r'words\words.en.txt', 'r', encoding='UTF-8') as f:
    dme = dict([(mot.casefold(), mot) for mot in f.read().splitlines()])
with open(r'words\extra.en.txt', 'r', encoding='UTF-8') as f:
    dme |= dict([(mot.casefold(), mot) for mot in f.read().splitlines() if mot.casefold() not in dme])

# dmx est l'ensemble des mots ni français ni anglais
with open(r'words\extra.xx.txt', 'r', encoding='UTF-8') as f:
    dmx = dict([(mot.casefold(), mot) for mot in f.read().splitlines()])


mfsa = defaultdict(list)   # mots français sans accents -> mot accentué s'il n'y en a qu'un qui existe sans accent
for mot in dmf.values():
    # Mn = Mark, Nonspacing = combining latin characters accents
    mot_sans_accents = ''.join(c for c in unicodedata.normalize("NFD", mot) if unicodedata.category(c) != 'Mn').casefold()
    if mot != mot_sans_accents:
        mfsa[mot_sans_accents].append(mot)

# On élimine les entrées comme cote -> ['côte', 'coté', 'côté'] puisqu'on ne sait pas quelle version accentuée choisir
to_delete = []
for key, lst in mfsa.items():
    if len(lst) > 1:
        to_delete.append(key)
for mot in to_delete:
    del mfsa[mot]



casefix = ['Excel', 'Python', 'PHP', 'MySQL', 'UML', 'Matlab', 'MP', 'MPSI', 'MP2I', 'PCSI', 'PTSI', 'CPGE', 'CSS', '3D', 'SQL', 'Android', 'Windows',
           'CSharp', 'Symphony', 'WCF', 'Google', 'Maps', 'Access', 'DUT', 'GEA', 'BTS', 'SVT', 'BCPST', 'POO', 'TD', 'PSI',
           'Unity', 'MPI', 'C', 'VBA', 'ISN', 'SII', 'CRPE', 'BCSPT', 'ECE', 'SIO', 'ECS', 'XML', 'HTML', 'DSI',
           'PAO', 'ECG', 'NSI', 'PC', 'PT', 'CPST', 'ENS', 'IUT', 'TSI', 'C++', 'InDesign', 'Photoshop',
           'BCPST1', 'BCPST2', 'ECE1', 'ECS1', 'ECS2', 'ITMax', 'IP', 'Eclipse', 'NetBeans' 'Java', 'JavaScript',
           'Angular', 'UI', 'UX', 'Kotlin', 'Dax', 'Ionic', 'EE', 'Maya', 'MCSA', 'QCM', 'Web', 'XSLT',
           'CAPES', 'API', 'PowerShell', 'Core', 'Power', 'BI', 'Desktop', 'Big', 'Data', 'Science', 'JSF', 'Server',
           'Scientist', 'Visual', 'Studio', 'Django', 'Raspberry', 'Pi', 'Kids', 'Arduino', 'ECT', 'Tage',
           'AutoCAD', 'Ajax', 'SEO', 'Scilab', 'React', 'EDHEC']

avectirets = ['Aide-mémoire', 'peuvent-elles', 'Libérez-vous', 'Entraînez-vous']

dic_casefix = dict([(mot.casefold(), mot) for mot in casefix])
dic_avectirets = dict([(mot.casefold(), mot) for mot in avectirets])


def fixcase(before: str, after: str) -> str:
    '''Si le mot d'origine commence par une majuscule, alors on force le remplacement à commencer par une majuscule'''
    return after[0].upper()+after[1:] if before[0] == before[0].upper() else after

uw: Counter[str] = Counter()
def fixwordbase(word: str) -> str:
    if word.casefold() in dmf:
        return fixcase(word, dmf[word.casefold()])      # fix case if needed
    if word.casefold() in mfsa:
        return fixcase(word, mfsa[word.casefold()][0])  # fix accent and case

    if "'" in word:
        p = word.find("'")
        prefix = word[:p+1]
        word2 = word[p+1:]
        if word2.casefold() in dmf:
            return prefix+dmf[word2.casefold()]         # fix case if needed
        if word2.casefold() in mfsa:
            return prefix+mfsa[word2.casefold()][0]     # fix accent and case

    if word[0] in 'lLdD' and (not "'" in word) and word.casefold() != 'lte':
        prefix = word[0]+"'"
        word2 = word[1:]
        if word2.casefold() in dmf:
            return prefix+dmf[word2.casefold()]         # fix case if needed
        if word2.casefold() in mfsa:
            return prefix+mfsa[word2.casefold()][0]     # fix accent and case

    if len(word)>1 and not word.casefold() in dic_casefix:
        uw.update([word])
    return word

def break_word(word:str) -> Tuple[str, str, str]:
    i = 0
    prefix = ''
    w = ''
    suffix = ''

    while i < len(word):
        c = word[i]
        if unicodedata.category(c) in ['Ll', 'Lm', 'Lo', 'Lt', 'Lu']:
            break
        prefix += c
        i += 1
    if i == len(word):
        return ('', word, '')       # For numeric-only words for instance
    while i < len(word):
        c = word[i]
        if unicodedata.category(c) not in ['Ll', 'Lm', 'Lo', 'Lt', 'Lu']:
            break
        w += c
        i += 1
    if w == '':
        return (prefix, word, '')
    return (prefix, word, word[i:])


def fixword(word: str) -> str:
    '''Si le mot n'existe pas mais il existe un mot accentué unique correspondant, retourne celui-ci'''
    if word in ['The', 'the', 'Dart']:
        return word
    if word in ['2e','3e','4e']:
        return word[0]+'è'

    prefix, w, suffix = break_word(word)
    return prefix+fixwordbase(w)+suffix


# for w in ['pomme', 'ecs2', '3arbres', '123abc456', '1234']:
#     print(w, '->', fixword(w))
# breakpoint()


def ireplace(text: str, old: str, new: str) -> str:
    '''Case insensitive replacement of old by new in text'''
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old):]
        idx = index_l + len(new)
    return text

def guess_language(words: str) -> Tuple[str, int, int, int]:
    xx = fr = en = 0
    for word in words.split(' '):
        _, w, _ = break_word(word)
        if any(c for c in unicodedata.normalize("NFD", mot) if unicodedata.category(c) == 'Mn'):
            fr += 1
        else:
            wc = w.casefold()
            if wc in dmx:
                xx += 1
            else:
                if wc in dme:
                    en += 1
                if wc in dmf:
                    fr += 1
    l = sorted([(fr, 'fr'), (en, 'en'), (xx, 'xx')], reverse=True)
    if l[0][0]>=3 and l[0][0]-l[1][0]>=2:
        return (l[0][1], fr, en, xx)
    return ('??', fr, en, xx)

def process_name(name: str) -> str:
    ts = name.split(' - ')
    s1 = ts[0]
    lng,fr,en,xx = guess_language(s1)
    print(f'{lng}\t{fr}\t{en}\t{xx}\t{s1}')
    return name

# process_name("Électronique Tout le cours en fiches")
# breakpoint()

def process_name0(name: str) -> str:
    ts = name.split(' - ')
    s1 = ts[0]
    l = []
    for word in s1.split(' \''):
        if len(word) > 0:
            nw = fixword(word)
            nwcf = nw.casefold()
            if nwcf in dic_casefix:
                nw = dic_casefix[nwcf]
            l.append(nw)
    ts[0] = ' '.join(l)
    nn = ' - '.join(ts)
    for w in avectirets:
        nn = ireplace(nn, w.replace('-', ' '), w)
    nn = ireplace(nn, 'node js', 'node.js')

    p1 = nn.find('[')
    p2 = nn.find(']', p1+1)
    if p1 >= 0 and p2 > p1+1:   # p1+1 avoids [] causing problem with editor[0]
        editor = nn[p1+1:p2]
        editor = ireplace(editor, 'oreilly', "O'Reilly")
        editor = editor[0].upper()+editor[1:]
        nn = nn[:p1+1]+editor+nn[p2:]

    nn = (nn[0].upper()+nn[1:]).replace('  ', ' ')
    return nn


# Tests
# print(process_name("la france"))
# breakpoint()

nd = 0
for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    basename, ext = os.path.splitext(file)

    newname = process_name(basename)
#     if basename != newname:
#         nd += 1
#         print(f'{basename}{ext} -> {newname}{ext}')

#         if doit:
#             f1 = os.path.join(folder, basename+ext)
#             f2 = os.path.join(folder, newname+ext)
#             os.rename(f1, f2)

# print()
# print(nd, 'fichier(s) à renommer')

# for w,c in uw.items():
#     print(w,c)
