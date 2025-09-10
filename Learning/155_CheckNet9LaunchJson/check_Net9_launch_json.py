# check_Net9_launch_json.py
# Check that launch.json files for Net9 do not conatin references to Net8, Net7, ...
#
# 2025-09-10    PV      First version

import codecs
import re
from myglob import MyGlobBuilder
from pathlib import Path

R = re.compile(r"net\d", re.IGNORECASE)

def process_file(path: Path):
    print(str(ma.path))

    lines: list[str]
    data = open(path, "rb").read()
    if data.startswith(codecs.BOM_UTF8):
        text = codecs.decode(data, encoding='utf_8_sig', errors='strict')
    else:
        # Either UTF-8 without BOM or ANSI
        # Since UTF-8 is strict on encoding, try it first, it it fails, then assume it's ANSI
        try:
            text = codecs.decode(data, encoding='utf_8', errors='strict')
        except:
            try:
                text = codecs.decode(data, encoding='cp1252', errors='strict')
            except:
                text = codecs.decode(data, encoding='mbcs', errors='strict')

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    updated = False
    for ix in range(len(lines)):
        l = lines[ix].lower()
        if "net8" in l or "net7" in l or "net6" in l or "net5" in l:
            print("--> ", lines[ix])
            ll = R.sub('net9', lines[ix])
            print("    ", ll)
            print()
            lines[ix] = ll
            updated = True
    if updated:
        text = "\n".join(lines)
        open(path, "w").write(text)
        pass

    
gs = MyGlobBuilder(r"C:\Development\Git*\**\Net9\**\launch.json").compile()
for ma in gs.explore():
    if ma.error:
        print(f"Error: {ma.error}")
        continue
    elif ma.is_file:
        process_file(ma.path)
