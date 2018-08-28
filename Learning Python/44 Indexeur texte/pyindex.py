# Indexeur texte
# Variations sur le thème  du ti et de l'indexation de texte
#
# 2018-08-14    PV


import collections
import functools
import locale
import re
import unicodedata

from typing import Dict, List, Tuple, DefaultDict, Iterable

import time

# print(locale.getlocale(locale.LC_ALL))        # (None, None)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
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


class french_text_canonizer():
    # This list can be customized to fit specific needs
    # expansion_list = [('œ', 'oe'), ('Œ', 'OE'), ('æ', 'ae'), ('Æ', 'AE'),
    #                   ("‘", "'"), ("’", "'"), ("‚", "'"), ("‛", "'"), ('‹', "'"), ('›', "'"),
    #                   ('“', '"'), ('”', '"'), ('„', '"'), ('‟', '"'), ('«', '"'), ('»', '"'),
    #                   ('ø', 'o\N{COMBINING SHORT SOLIDUS OVERLAY}'), ('Ø', 'O\N{COMBINING LONG SOLIDUS OVERLAY}'),
    #                   ('‽', '?!'),  # ('¿', '?'), ('¡', '!'),
    #                   ("\N{NO-BREAK SPACE}", ' ')
    #                   ]

    # For this context
    #expansion_list = [('œ', 'oe'), ("’", "'")]
    expansion_list = [('œ', 'oe')]

    def __init__(self, case_significant: bool, accent_significant: bool):
        self.case_significant = case_significant
        self.accent_significant = accent_significant

    # def canonize_ci_ai(self, s: str) -> str:
    #     return ''.join(c for c in list(unicodedata.normalize("NFKD", s.replace('œ', 'oe').replace("’", "'").upper())) if unicodedata.category(c) != 'Mn')

    # def canonize_ci_as(self, s: str) -> str:
    #     return unicodedata.normalize("NFKD", s.replace('œ', 'oe').replace("’", "'").upper())

    def canonize(self, s: str) -> str:
        # First some expansions not managed by normalization
        for (s1, s2) in french_text_canonizer.expansion_list:
            if s1 in s:
                s = s.replace(s1, s2)

        # Enable expansion of ĳ Ĳ ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ ﬆ ‼ and others
        s = unicodedata.normalize("NFKD", s)

        if not self.case_significant:
            s = s.upper()
        if not self.accent_significant:
            s = ''.join(c for c in list(s) if unicodedata.category(c) != 'Mn')
        return unicodedata.normalize("NFC", s)

    # Default method for objets of the class
    __call__ = canonize


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
DIGITSONLY_RE = re.compile(r'\d+')


class forms_locations():
    def __init__(self):
        self.forms: DefaultDict[str, int] = collections.defaultdict(int)
        self.locations: List[Tuple[int, int]] = []

# forms_locations = collections.namedtuple("forms_locations", "forms locations")

start = time.time()
index: DefaultDict[str, forms_locations] = collections.defaultdict(forms_locations)
words_count = 0
with open("hp5.txt", "r", encoding="utf-8-sig") as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            if not DIGITSONLY_RE.fullmatch(match.group()):
                words_count += 1
                #word = match.group().lower()
                word = fr_ci_as(match.group())

                column_no = match.start()+1
                location = (line_no, column_no)

                # if not word in index:
                #     index[word] = forms_locations(collections.defaultdict(int), [])

                index[word].forms[match.group()] += 1
                index[word].locations.append(location)

print("Duration: %.3f" % (time.time()-start))
print(f"Words: {words_count}, Index size: {len(index)}")


# Helper to limit the size of an interable to the first n elements
def top(seq: Iterable, n: int):
    for item in seq:
        if n <= 0:
            return
        n -= 1
        yield item


# Reduce index to entries seen at least 10 times
ir = {key: value for (key, value) in index.items() if len(value.locations) >= 10}
print(f"Index réduit: {len(ir)}")

# Print reduced index in alphabetical order
nl = 0
print("Sorted by alphabetical order (word, frequencey) reduced index (frequency≥10)")
with open("analysis.txt", "w", encoding="utf-8") as fo:
    for word in sorted(ir, key=functools.cmp_to_key(locale.strcoll)):
        l = f"{word}\t{len(ir[word].locations)}\t{dict(ir[word].forms)}\n"
        nl += 1
        if nl<100:
            print(l, end='')
        fo.write(l)

# import json
# with open("index.txt", "w", encoding="utf-8") as fi:
#     json.dump(index, fi)


# Print top 20 by frequency descending
print("\nSorted by decreasing frequency (word, frequency) full index")
nw = 0
for word, count in sorted([(word, len(fl.locations)) for word, fl in index.items()], key=lambda tup: tup[1], reverse=True):
    print(f"{word}\t{count}")
    nw += 1
    if nw > 30:
        break

print("\nSorted be decreasing length (word, length) full index")
nw = 0
for word, l in sorted([(word, len(word)) for word in index.keys()], key=lambda tup: len(tup[0]), reverse=True):
    print(f"{word}\t{l}")
    nw += 1
    if nw > 30:
        break
