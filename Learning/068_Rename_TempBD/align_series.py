# align_series.py
# Ensure that BD series (part of name before first " - ") are homogeneous
# 2020-02-28    PV

import os
from collections import defaultdict
from typing import DefaultDict
import json
import re

from common import normalize_serie
from common_fs import get_all_files


source = r"W:\TempBD\Final"


print("Reading files hierarchy...")
files = list(get_all_files(source))

print("Grouping files...")
series: DefaultDict[str, set] = defaultdict(set)
nf = 0
for fullpath in files:
    path, file = os.path.split(fullpath)
    stem, ext = os.path.splitext(file)
    segments = stem.split(" - ")
    serie = segments[0]
    serie_lna = normalize_serie(serie)
    series[serie_lna].add(serie)
# Replace set by list to serialize
# Or check https://stackoverflow.com/questions/8230315/how-to-json-serialize-sets
series2 = {k: list(v) for (k, v) in series.items()}
# with open(r'series.json', 'w', encoding='utf8') as outfile:
#     json.dump(series2, outfile, indent=4, ensure-ascii=False)

print(f"{nf} fichiers")
print(f"{len(series)} séries")


def find_series_with_multiple_spellings() -> None:
    print("Series with multiple spellings")
    exceptions = [
        ("Jojo", "Les aventures de Jojo"),
        ("Le voyageur", "Voyageur"),
        ("L'autre monde", "Un autre monde"),
    ]

    def isException(v):
        return (v[0], v[1]) in exceptions

    seriesm: list[list[str]] = []
    with open(r"spellings.txt", mode="w", encoding="utf-8") as out:
        for k, v in series.items():
            if len(v) > 1:
                lv = sorted(list(v))
                if not ((lv[0], lv[1]) in exceptions or (lv[1], lv[0]) in exceptions):
                    seriesm.append(lv)
                    print(f"{k:<100} {len(lv)}")
                    for spelling in lv:
                        out.write(spelling + ";")
                    out.write("\n")
    with open(r"spellings.json", "w", encoding="utf8") as outfile:
        json.dump(seriesm, outfile, indent=4, ensure_ascii=False)
    print(
        f"Written {len(seriesm)} series with 2 or more spellings in spellings.txt and spellings.json"
    )


# find_series_with_multiple_spellings()


def find_series_ending_with_numbers():
    print("Series ending with numbers")
    ENDDIGITS_RE = re.compile(r".*[ 0-9]+")
    with open(r"series_avec_num.json", "r", encoding="utf8") as infile:
        series_avec_num = json.load(infile)
    snum = []
    for k, _ in series.items():
        if ENDDIGITS_RE.fullmatch(k):
            if k not in series_avec_num:
                snum.append(k)
    with open(r"seriesendnum.txt", "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(sorted(snum)))
    print(f"{len(snum)} series written in seriesendnum.txt")


# find_series_ending_with_numbers()


diffMax = 1


# Adapted from https://en.wikipedia.org/wiki/Levenshtein_distance and personal app DiffMP3Names
def levenshtein_distance(s: list, t: list):
    # Optimisation perso, j'ai pas besoin des distances supérieures à diffMax
    if abs(len(s) - len(t)) > diffMax:
        return diffMax + 1

    # degenerate cases
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)

    # # convert to lowercase, we're doing case insensitive compare here
    # s = s.lower()
    # t = t.lower()

    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    v0 = list(range(len(t) + 1))
    v1 = [0] * (len(t) + 1)

    for i in range(len(s)):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


def series_with_distance_one():
    seriesnonum = []
    for s in series.keys():
        snonnum = re.sub(r" *[0-9·]+(-[0-9·]+)? *", " ", s, flags=re.IGNORECASE).strip()
        if s != snonnum and len(snonnum) > 0:
            if snonnum not in seriesnonum:
                seriesnonum.append(snonnum)
            # print(f"{s:<80} <{snonnum}>")

    for i in range(len(seriesnonum)):
        for j in range(i + 1, len(seriesnonum)):
            if levenshtein_distance(seriesnonum[i], seriesnonum[j]) <= 1:
                print(f"{seriesnonum[i]:<80} {seriesnonum[j]}")


series_with_distance_one()
