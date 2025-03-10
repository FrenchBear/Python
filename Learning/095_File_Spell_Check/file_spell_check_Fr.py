# file_spell_check_Fr.py
# Tentative de correction automatique de fautes d'accents sur des noms de fichiers en français
#
# 2021-12-16    PV
# 2022-01-03    PV      Fusionne les mots de mots_fr.txt avec ceux de mots_fr2.txt (typiquement les nom propres); Mots en anglais
# 2022-06-04    PV      Nettoyage et correction d'erreurs pour renommer des ebooks
# 2023-12-19    PV      Modifie le 3è segment d'un fichier
# 2024-03-17    PV      Break_words ne coupe plus sur -; expressions.fr.txt
# 2024-09-18    PV      Constante SEGMENT

from collections import defaultdict
from collections import Counter
from common_fs import get_all_files
import unicodedata
import os

SEGMENT = 0     # index du segment séparé par " - " sur lequel porte la correction
source = r"C:\Downloads\A_Trier\!A_Trier_Livres"
#source = r"U:\Pierre\A_Trier\A_Trier Brut\Tanguy Pastureau maltraite l'info 2023"          # Use segment=2
doit = True

# dmf est l'ensemble des mots français accentués, indexé par la version casefold() du mot
dmf: dict[str, str] = {}

print("Chargement des mots Fr")

# words1.fr.txt est un dico complet plus long à charger, words2.fr.txt est plus simple.  Pas de majuscules (ex: japon)
with open(r'words\words1.fr.txt', 'r', encoding='UTF-8') as f:
    dmf |= dict((mot.casefold(), mot) for mot in f.read().splitlines())
with open(r'words\words2.fr.txt', 'r', encoding='UTF-8') as f:
    dmf |= dict((mot.casefold(), mot) for mot in f.read().splitlines() if ' ' not in mot and mot.casefold() not in dmf)
with open(r'words\extra.fr.txt', 'r', encoding='UTF-8') as f:
    dmf |= dict((mot.casefold(), mot) for mot in f.read().splitlines() if mot.casefold() not in dmf)

# dme est l'ensemble des mots anglais
# with open(r'words\words.en.txt', 'r', encoding='UTF-8') as f:
#     dme = dict((mot.casefold(), mot) for mot in f.read().splitlines())
# with open(r'words\extra.en.txt', 'r', encoding='UTF-8') as f:
#     dme |= dict((mot.casefold(), mot) for mot in f.read().splitlines() if mot.casefold() not in dme)

# dmx est l'ensemble des mots ni français ni anglais
with open(r'words\extra.xx.txt', 'r', encoding='UTF-8') as f:
    dmx = dict((mot.casefold(), mot) for mot in f.read().splitlines())

# Certaines expressions ont une casse spécifique différente des mots qui la composent (ex: Nouveau Testament ou Alexandre le Grand)
with open(r'words\expressions.fr.txt', 'r', encoding='UTF-8') as f:
    dic_expressions = dict((expression.casefold(), expression) for expression in f.read().splitlines())

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

with open(r'words\specialcasing.txt', 'r', encoding='UTF-8') as f:
    set_casefix = set(mot for mot in f.read().splitlines())
dic_casefix = dict([(mot.casefold(), mot) for mot in set_casefix])

avectirets = ['Aide-mémoire', 'peuvent-elles', 'Libérez-vous', 'Entraînez-vous']
dic_avectirets = dict([(mot.casefold(), mot) for mot in avectirets])

print("Traitement des fichiers")

def fixcase(before: str, after: str, first: bool) -> str:
    '''Si le mot d'origine commence par une majuscule, alors on force le remplacement à commencer par une majuscule'''
    #beforemaj = before[0] == before[0].upper()
    aftermaj = after[0] == after[0].upper()
    if first or aftermaj:
        return after[0].upper()+after[1:]
    else:    
        return after

uw: Counter[str] = Counter()


def fixwordbase(word: str, first: bool) -> str:
    if word.casefold() in dmf:
        return fixcase(word, dmf[word.casefold()], first)      # fix case if needed
    if word.casefold() in mfsa:
        return fixcase(word, mfsa[word.casefold()][0], first)  # fix accent and case

    # print('«'+word+"»", first)

    # Fix full UPPERCASE words
    if word==word.upper():
        word = word.lower()
    if first:
        word=word[0].upper()+word[1:]

    if "'" in word:
        p = word.find("'")
        prefix = word[:p+1]
        word2 = word[p+1:]
        if word2.casefold() in dmf:
            return prefix+dmf[word2.casefold()]         # fix case if needed
        if word2.casefold() in mfsa:
            return prefix+mfsa[word2.casefold()][0]     # fix accent and case

    if word[0] in 'lLdD' and ("'" not in word) and word.casefold() != 'lte':
        prefix = word[0]+"'"
        word2 = word[1:]
        if word2.casefold() in dmf:
            return prefix+dmf[word2.casefold()]         # fix case if needed
        if word2.casefold() in mfsa:
            return prefix+mfsa[word2.casefold()][0]     # fix accent and case

    if len(word) > 1 and word.casefold() not in dic_casefix:
        uw.update([word])
    return word


def break_word(word: str) -> tuple[str, str, str]:
    i = 0
    prefix = ''
    w = ''
    
    while i < len(word):
        c = word[i]
        if unicodedata.category(c) in ['Ll', 'Lm', 'Lo', 'Lt', 'Lu'] or c in ['-']:
            break
        prefix += c
        i += 1
    if i == len(word):
        return ('', word, '')       # For numeric-only words for instance
    while i < len(word):
        c = word[i]
        if unicodedata.category(c) not in ['Ll', 'Lm', 'Lo', 'Lt', 'Lu'] and c not in ['-']:
            break
        w += c
        i += 1
    if w == '':
        return (prefix, word, '')
    return (prefix, w, word[i:])

def fixwordinner(word: str, first: bool) -> str:
    '''Si le mot n'existe pas mais il existe un mot accentué unique correspondant, retourne celui-ci'''
    if word in ['The', 'the', 'Dart']:
        return word
    if word in ['2e', '3e', '4e']:
        return word[0]+'è'
    prefix, w, suffix = break_word(word)
    return prefix+fixwordbase(w, first)+suffix

def fixword(word: str, first: bool) -> str:
    ts = word.split("'")
    tsout: list[str] = []
    for w in ts:
        tsout.append(fixwordinner(w, first))
        first = False
    return "'".join(tsout)

# for w in ['pomme', 'ecs2', '3arbres', '123abc456', '1234']:
#     print(w, '->', fixword(w))
# breakpoint()


# def ireplace(text: str, old: str, new: str) -> str:
#     '''Case insensitive replacement of old by new in text'''
#     idx = 0
#     while idx < len(text):
#         index_l = text.lower().find(old.lower(), idx)
#         if index_l == -1:
#             return text
#         text = text[:index_l] + new + text[index_l + len(old):]
#         idx = index_l + len(new)
#     return text


# def guess_language(words: str) -> tuple[str, int, int]:
#     # # For just French files
#     # return('fr',1,0)

#     fr = en = 0
#     for word in words.split(' '):
#         _, w, _ = break_word(word)
#         if any(c for c in unicodedata.normalize("NFD", mot) if unicodedata.category(c) == 'Mn'):
#             fr += 1
#         else:
#             wc = w.casefold()
#             if not wc in dmx:
#                 if wc in dme:
#                     en += 1
#                 if wc in dmf:
#                     fr += 1
#     l = sorted([(fr, 'fr'), (en, 'en')], reverse=True)
#     if l[0][0] >= 3 and l[0][0]-l[1][0] >= 2:
#         return (l[0][1], fr, en)
#     return ('??', fr, en)


# def process_name_Test(name: str) -> str:
#     ts = name.split(' - ')
#     s1 = ts[0]
#     lng, fr, en = guess_language(s1)
#     print(f'{lng}\t{fr}\t{en}\t{s1}\t{name}')
#     return name

# for filefp in get_all_files(source):
#     folder, file = os.path.split(filefp)
#     bname, ext = os.path.splitext(file)
#     process_name_Test(bname)
# breakpoint()


def process_name(name: str) -> str:
    ts = name.split(' - ')
    s2 = ts[SEGMENT]
    li = []
    first = True
    for word in s2.split(' '):
        if len(word) > 0:
            nw = fixword(word, first)
            first = False
            nwcf = nw.casefold()
            if nwcf in dic_casefix:
                nw = dic_casefix[nwcf]
            li.append(nw)
    ts[SEGMENT] = ' '.join(li)
    nn = ' - '.join(ts)
    # Special cases
    nn = nn.replace('cplusplus', 'C++').replace('Cplusplus', 'C++').replace("[Oreilly]", "[O'Reilly]")
    nncf = nn.casefold()
    for expression in dic_expressions.keys():
        if expression in nncf:
            p = nncf.index(expression)
            nn = nn[:p] + dic_expressions[expression] + nn[p+len(expression):]
    return nn

#print(process_name("La convention européenne des droits de l'homme - Sudre Frédéric.epub"))
# print(process_name("Histoire de la grande-Bretagne - Que-sais-je.epub"))
# print(process_name("L'alsace-Lorraine pendant la guerre 1939-1945 - Que-sais-je"))

nd = 0
for filefp in get_all_files(source):
    folder, file = os.path.split(filefp)
    if file.lower()!='thumbs.db':
        bname, ext = os.path.splitext(file)

        newname = process_name(bname)
        if bname != newname:
            nd += 1
            print(f'{bname}{ext} -> {newname}{ext}')

            if doit:
                f1 = os.path.join(folder, bname+ext)
                f2 = os.path.join(folder, newname+ext)
                os.rename(f1, f2)

print()
print(nd, 'fichier(s) à renommer')
