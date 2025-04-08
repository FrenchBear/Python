# renYggPack.py
# Reformat book names of ygg packs where editor is put first
# "deboeck Biochimie 3ed.pdf" -> "Biochimie (3rd ed, X) - [Deboeck] - X.pdf"
#
# In regex, .+? is the non-greedy form of .+
#
# 2022-06-15    PV
# 2022-06-30    PV      Accept any char but space in editor name; replace _ by space in editor name
# 2023-01-22    PV      lang variable

from common_fs import get_files
import os
import re

source = r"C:\Downloads\A_Trier\!A_Trier_Livres"
lang = "Fr"  # Fr or En
doit = True

ED = re.compile(r"^([^ ]+) (.+?)( (\d+)ed)?\.pdf$")


def FirstUpper(s: str) -> str:
    return s[0].upper() + s[1:]


def ireplace(text: str, old: str, new: str) -> str:
    """Case insensitive replacement of old by new in text"""
    idx = 0
    while idx < len(text):
        index_l = text.lower().find(old.lower(), idx)
        if index_l == -1:
            return text
        text = text[:index_l] + new + text[index_l + len(old) :]
        idx = index_l + len(new)
    return text


rencount = 0
for file in list(get_files(source)):
    if file.lower().endswith(".pdf"):
        stem, ext = os.path.splitext(file)
        ma = ED.match(file)
        if ma:
            # print(f'«{ma.group(1)}» «{ma.group(2)}» «{ma.group(3)}» «{ma.group(4)}»')
            nn: str = FirstUpper(ma.group(2))
            if ma.group(4):
                if lang == "En":
                    match ma.group(4):
                        case "1":
                            sed = "1st"
                        case "2":
                            sed = "2nd"
                        case "3":
                            sed = "3rd"
                        case _:
                            sed = ma.group(4) + "th"
                elif lang == "Fr":
                    match ma.group(4):
                        case "1":
                            sed = "1ère"
                        case _:
                            sed = ma.group(4) + "è"
                else:
                    breakpoint()
                nn += f" ({sed} ed, X)"
            nn += (
                " - ["
                + ireplace(
                    FirstUpper(ma.group(1)).replace("_", " "), "oreilly", "O'Reilly"
                )
                + "] - X.pdf"
            )
            nn = ireplace(ireplace(nn, "csharp", "C#"), "cplusplus", "C++")
            print(file, " -> ", nn)
            rencount += 1
            if doit:
                os.rename(os.path.join(source, file), os.path.join(source, nn))
        else:
            breakpoint()
            pass

print(rencount, " fichier(s) renommé(s)")
