# RemoveSAK
# Remove useless lines in .csproj files
#
# 2023-01-15    PV

from common_fs import get_all_files, extension
import codecs
import re
import os

root = r'C:\Development\GitVSTS\WPF\Net7\Learning'
files = [f for f in get_all_files(root) if extension(f.lower()) in ['.csproj']]

L1 = re.compile(r'\s*<SccProjectName>SAK</SccProjectName>\s*')
L2 = re.compile(r'\s*<SccLocalPath>SAK</SccLocalPath>\s*')
L3 = re.compile(r'\s*<SccAuxPath>SAK</SccAuxPath>\s*')
L4 = re.compile(r'\s*<SccProvider>SAK</SccProvider>\s*')
L5 = re.compile(r'\s+')

def ProcessFile(filefp: str):
    path, file = os.path.split(filefp)
    base, ext = os.path.splitext(file)

    lines: list[str]
    data = open(filefp, "rb").read()
    if data.startswith(codecs.BOM_UTF8):
        lines = codecs.decode(data, encoding='utf_8_sig', errors='strict').split('\r\n')
    else:
        # Either UTF-8 without BOM or ANSI
        # Since UTF-8 is strict on encoding, try it first, it it fails, then assume it's ANSI
        try:
            lines = codecs.decode(data, encoding='utf_8', errors='strict').split('\r\n')
        except Exception:
            lines = codecs.decode(data, encoding='mbcs', errors='strict').split('\r\n')

    found = False
    for line in lines:
        if L1.fullmatch(line):
            print(filefp, "L1 found")
            found = True
        elif L2.fullmatch(line):
            print(filefp, "L2 found")
            found = True
        elif L3.fullmatch(line):
            print(filefp, "L3 found")
            found = True
        elif L4.fullmatch(line):
            print(filefp, "L4 found")
            found = True
        elif L5.fullmatch(line):
            print(filefp, "L5 found")
            found = True

    if found:        
        with open(filefp, 'w', encoding='utf_8_sig') as fout:
            for line in lines:
                if not L1.fullmatch(line) and not L2.fullmatch(line) and not L3.fullmatch(line) and \
                   not L4.fullmatch(line) and not L5.fullmatch(line):
                    fout.write(line+'\n')

    print("Cleaned\n")

for file in files:
    ProcessFile(file)

#ProcessFile(r'C:\Development\GitVSTS\WPF\Net7\Learning\WPF70 Drag and Drop\WPF70 Drag and Drop.csproj')
