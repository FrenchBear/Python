# file spell check.py
# Tentative de correction automatique de fautes d'accents sur des noms de fichiers en français
#
# 2021-12-16    PV

from collections import defaultdict
from os import replace
from typing import DefaultDict
from common_fs import *
import unicodedata

source = r'W:\Livres\A_Trier'

# dmf est l'ensemble des mots français accentués, indexé par la version casefold() du mot
with open('mots_fr2.txt', 'r', encoding='UTF-8') as f:
    dmf = dict([(mot.casefold(), mot) for mot in f.read().splitlines()])
# print(len(dmf))

mfsa = defaultdict(list)   # mots français sans accents -> mot accentué s'il n'y en a qu'un qui existe sans accent
for mot in dmf.values():
    # Mn = Mark, Nonspacing = combining latin characters accents
    mot_sans_accents = ''.join(c for c in unicodedata.normalize(
        "NFD", mot) if unicodedata.category(c) != 'Mn').casefold()
    if mot != mot_sans_accents:
        mfsa[mot_sans_accents].append(mot)

# On élimine les entrées comme cote -> ['côte', 'coté', 'côté'] puisqu'il on ne sais pas quelle version accentuée choisir
to_delete = []
for key, lst in mfsa.items():
    if len(lst) > 1:
        to_delete.append(key)
for mot in to_delete:
    del mfsa[mot]


def fixword(word: str) -> str:
    '''Si le mot n'existe pas mais il existe un mot accentué unique correspondant, retourne celui-ci'''
    if word.casefold() in dmf:
        return dmf[word.casefold()]        # fix case if needed
    if word.casefold() in mfsa:
        return mfsa[word.casefold()][0]    # fix accent and case

    if "'" in word:
        p = word.find("'")
        prefix = word[:p+1]
        word2 = word[p+1:]
        if word2.casefold() in dmf:
            return prefix+dmf[word2.casefold()]        # fix case if needed
        if word2.casefold() in mfsa:
            return prefix+mfsa[word2.casefold()][0]    # fix accent and case

    if word[0] in 'lLdD' and (not "'" in word) and word.casefold() != 'lte':
        prefix = word[0]+"'"
        word2 = word[1:]
        if word2.casefold() in dmf:
            return prefix+dmf[word2.casefold()]        # fix case if needed
        if word2.casefold() in mfsa:
            return prefix+mfsa[word2.casefold()][0]    # fix accent and case

    return word


casefix = ['Excel', 'Python', 'PHP', 'MySQL', 'UML', 'Matlab', 'MP', 'MPSI', 'MP2I', 'PCSI', 'PTSI', 'CPGE', 'CSS', '3D', 'SQL', 'Android', 'Windows',
           'CSharp', 'Symphony', 'WCF', 'Google', 'Maps', 'Access', 'DUT', 'GEA', 'BTS', 'SVT', 'BCPST', 'POO', 'TD', 'PSI',
           'Unity', 'MPI', 'C', 'VBA', 'ISN', 'SII', 'CRPE', 'BCSPT', 'ECE', 'SIO', 'ECS', 'XML', 'HTML', 'DSI',
           'PAO', 'ECG', 'NSI', 'PC', 'PT', 'CPST', 'ENS', 'IUT', ',TSI', 'C++', 'InDesign', 'Photoshop',
           'BCPST1', 'BCPST2', 'ECE1', 'ECS1', 'ECS2', 'ITMax', 'IP', 'Eclipse', 'NetBeans' 'Java', 'JavaScript',
           'Angular', 'UI', 'UX', 'Kotlin', 'Dax', 'Ionic', 'ee', 'Maya', 'MCSA', 'QCM', 'Web' ]

avectirets = ['Aide-mémoire', 'peuvent-elles', 'Libérez-vous', 'Entraînez-vous']

dic_casefix = dict([(mot.casefold(), mot) for mot in casefix])
dic_avectirets = dict([(mot.casefold(), mot) for mot in avectirets])


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


def process_name(name: str) -> str:
    ts = name.split(' - ')
    s1 = ts[0]
    l = []
    for word in s1.split(' '):
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
    if p1 >= 0 and p2 > p1:
        editor = nn[p1+1:p2]
        editor = ireplace(editor, 'oreilly', "O'Reilly")
        editor = editor[0].upper()+editor[1:]
        nn = nn[:p1+1]+editor+nn[p2:]

    nn = (nn[0].upper()+nn[1:]).replace('  ', ' ')
    return nn


# print(process_name("lapprentissage profond avec python"))
# breakpoint()

for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    basename, ext = os.path.splitext(file)

    #if basename=='Algèbre et geométrie mp 5ed - [Dunod] - X': breakpoint()

    newname = process_name(basename)
    if basename != newname:
        #print(f'{basename}{ext} -> {newname}{ext}')
        f1 = os.path.join(folder, basename+ext)
        f2 = os.path.join(folder, newname+ext)
        print(newname)
        os.rename(f1, f2)
