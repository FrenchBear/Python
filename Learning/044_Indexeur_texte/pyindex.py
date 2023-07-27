# Indexeur texte
# Variations sur le thème  du ti et de l'indexation de texte
#
# 2018-08-14    PV
# 2018-09-01    PV      Tried collections.Counter, replaced my own top function by itertools.islice


import collections
import functools
import itertools
import locale
import re
import unicodedata
import time

from typing import DefaultDict


# print(locale.getlocale(locale.LC_ALL))        # (None, None)
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
# print(locale.getlocale(locale.LC_ALL))        # ('en_US', 'UTF-8')


"""
l = ['a', 'à', 'A', 'Â', 'b', 'c', 'ç', 'C', 'Ç', 'd', 'boeuf', 'bœuf', 'boev']
l.sort(key=functools.cmp_to_key(locale.strcoll))
print(l)
"""

"""
# Dictionary filtering
d = {'trois':3, 'quatre':4, 'cinq':5, 'six':6}
print(list(filter(lambda key: d[key]>=5, d)))
e = {key: value for (key, value) in d.items() if value>=5}
print(e)
"""


class french_text_canonizer:
    # This list can be customized to fit specific needs
    # expansion_list = [('œ', 'oe'), ('Œ', 'OE'), ('æ', 'ae'), ('Æ', 'AE'),
    #                   ("‘", "'"), ("’", "'"), ("‚", "'"), ("‛", "'"), ('‹', "'"), ('›', "'"),
    #                   ('“', '"'), ('”', '"'), ('„', '"'), ('‟', '"'), ('«', '"'), ('»', '"'),
    #                   ('ø', 'o\N{COMBINING SHORT SOLIDUS OVERLAY}'), ('Ø', 'O\N{COMBINING LONG SOLIDUS OVERLAY}'),
    #                   ('‽', '?!'),  # ('¿', '?'), ('¡', '!'),
    #                   ("\N{NO-BREAK SPACE}", ' ')
    #                   ]

    # For this context
    # expansion_list = [('œ', 'oe'), ("’", "'")]
    expansion_list = [("œ", "oe")]

    def __init__(self, case_significant: bool, accent_significant: bool):
        self.case_significant = case_significant
        self.accent_significant = accent_significant

    # def canonize_ci_ai(self, s: str) -> str:
    #     return ''.join(c for c in list(unicodedata.normalize("NFKD", s.replace('œ', 'oe').replace("’", "'").upper())) if unicodedata.category(c) != 'Mn')

    # def canonize_ci_as(self, s: str) -> str:
    #     return unicodedata.normalize("NFKD", s.replace('œ', 'oe').replace("’", "'").upper())

    # Previously:
    # def canonize(self, s: str) -> str:
    # __call__=canonize

    # Default method for objets of the class
    def __call__(self, s: str) -> str:
        # First some expansions not managed by normalization
        for s1, s2 in french_text_canonizer.expansion_list:
            if s1 in s:
                s = s.replace(s1, s2)

        # Enable expansion of ĳ Ĳ ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ ﬆ ‼ and others
        s = unicodedata.normalize("NFKD", s)

        if not self.case_significant:
            s = s.upper()
        if not self.accent_significant:
            s = "".join(c for c in list(s) if unicodedata.category(c) != "Mn")
        return s  # unicodedata.normalize("NFC", s)


# Create all combinations for tests
fr_ci_ai = french_text_canonizer(False, False)
fr_ci_as = french_text_canonizer(False, True)
fr_cs_ai = french_text_canonizer(True, False)
fr_cs_as = french_text_canonizer(True, True)


# s = "Où ça? Écoute ‘ton’ cœur‼ «Dĳsktra» Søråñ “ÆØRÅÑ”"
# print(s)
# print(fr_ci_ai.canonize(s))
# print(fr_ci_as.canonize(s))
# print(fr_cs_ai.canonize(s))
# print(fr_cs_as.canonize(s))


WORD_RE = re.compile(r"[\w]+")
WORD_QUOTE_RE = re.compile(r"[\w’]+")
DIGITS_ONLY_RE = re.compile(r"\d+")


# Tried to use a collections.Counter() instead of a collections.defaultdict(int)
# but performance is very bas (3.4s execution instead of 1.8s)
# Probable cause: collections.Counter() only support update(iterable) updte
# and has no single Add(item) method, so there is too much overhead building an
# iterable from a single element just to add one item to a counter.


class forms_locations:
    def __init__(self):
        self.forms: DefaultDict[str, int] = collections.defaultdict(int)
        # self.forms: collections.Counter() = collections.Counter()
        self.locations: list[tuple[int, int]] = []

    def __str__(self):
        # return self.forms.most_common(1)[0][0]
        m = -1
        s = ""
        for form, count in self.forms.items():
            if count > m:
                m = count
                s = form
        return s

    def count(self):
        return sum(c for c in self.forms.values())


def index_file(
    file: str, wordre, canonize
) -> tuple[DefaultDict[str, forms_locations], int]:
    index: DefaultDict[str, forms_locations] = collections.defaultdict(forms_locations)
    words_count = 0
    with open(file, "r", encoding="utf-8-sig") as fp:
        for line_no, line in enumerate(fp, 1):
            for match in wordre.finditer(line):
                if not DIGITS_ONLY_RE.fullmatch(match.group()):
                    words_count += 1
                    # word = match.group().lower()
                    word = canonize(match.group())
                    column_no = match.start() + 1
                    location = (line_no, column_no)
                    index[word].forms[match.group()] += 1
                    # index[word].forms.update([match.group()])
                    index[word].locations.append(location)
    return index, words_count


def test_indexer():
    # file = "hp5.txt"
    file = "sda2.txt"

    ix1 = fr_ci_as  # Duration: 1.165

    def ix2(s):
        return locale.strxfrm(
            unicodedata.normalize("NFKD", s).upper()
        )  # Duration: 1.106

    """
    locale sort keys a à âge agit...
    fr_ci_as sorts keys a agit... à âge 
    """

    start = time.time()
    index, words_count = index_file(file, WORD_RE, ix2)
    print("Duration: %.3f" % (time.time() - start))
    print(f"Words: {words_count}, Index size: {len(index)}")

    # Reduce index to entries seen at least 10 times
    ir = {key: value for (key, value) in index.items() if len(value.locations) >= 10}
    print(f"Index réduit: {len(ir)}")

    # Print reduced index in alphabetical order
    nl = 0
    print(
        "Sorted by alphabetical order (word, frequencey) reduced index (frequency≥10)"
    )
    with open("analysis.txt", "w", encoding="utf-8") as fo:
        for key in sorted(ir):
            l = f"{ir[key]}\t{len(ir[key].locations)}\t{dict(ir[key].forms)}\n"
            nl += 1
            if nl < 150:
                print(l, end="")
            fo.write(l)

    # Print top 20 by frequency descending
    print("\nSorted by decreasing frequency (word, frequency) full index")
    nw = 0
    for word, count in sorted(
        [(str(fl), fl.count()) for fl in index.values()],
        key=lambda tup: tup[1],
        reverse=True,
    ):
        print(f"{word}\t{count}")
        nw += 1
        if nw > 20:
            break

    print("\nSorted be decreasing length (word, length) full index")
    nw = 0
    for word, count in sorted(
        [(str(fl), len(str(fl))) for fl in index.values()],
        key=lambda tup: tup[1],
        reverse=True,
    ):
        print(f"{word}\t{count}")
        nw += 1
        if nw > 20:
            break


def search_quote(file: str):
    # Recherche les formes avec apostrophes identiques à un mot sans apostrophe
    # comme d'écrire/décrire, l'éviter/léviter, l'aide/laide, d'avantage/davantage, l'imiter/limiter...

    index, _ = index_file(file, WORD_RE, fr_ci_as)
    index_quote, _ = index_file(file, WORD_QUOTE_RE, fr_ci_as)

    for word in [w for w in index_quote.keys() if "’" in w]:
        if word.replace("’", "") in index.keys():
            print(word)


def count_letters(file: str):
    dic: DefaultDict[str, int] = collections.defaultdict(int)
    with open(file, "r", encoding="utf-8-sig") as fp:
        for line in fp:
            for char in line:
                dic[char] += 1
    for letter, count in sorted(dic.items(), key=lambda tup: tup[1], reverse=True):
        print(f"{letter}\t{count}")


# count_letters("sda.txt")
test_indexer()
